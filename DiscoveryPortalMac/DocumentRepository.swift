import SQLite

class DocumentRepository {
    private let db: Connection
    private let documents = Table("documents")

    // Column definitions
    private let id = Expression<Int64>("id")
    private let category = Expression<String>("category")
    private let filepath = Expression<String>("filepath")
    private let filename = Expression<String>("filename")
    private let status = Expression<String>("status")
    private let confidence = Expression<Double?>("confidence")
    private let lastModified = Expression<String>("last_modified")
    private let year = Expression<String?>("year")
    private let owner = Expression<String?>("owner")
    private let accountId = Expression<String?>("account_id")
    private let period = Expression<String?>("period")
    private let hash = Expression<String>("hash")

    init() throws {
        // Copy DB from bundle into Documents directory if needed
        let fm = FileManager.default
        let docsURL = try fm.url(for: .documentDirectory, in: .userDomainMask,
                                 appropriateFor: nil, create: true)
        let dbURL = docsURL.appendingPathComponent("dda.db")

        if !fm.fileExists(atPath: dbURL.path) {
            if let bundlePath = Bundle.main.path(forResource: "dda", ofType: "db") {
                try fm.copyItem(atPath: bundlePath, toPath: dbURL.path)
                print("Copied DB to Documents directory: \(dbURL.path)")
            } else {
                throw NSError(domain: "DB", code: 1,
                              userInfo: [NSLocalizedDescriptionKey: "Database not found in bundle"])
            }
        }

        db = try Connection(dbURL.path)

        // Ensure unique index on hash
        try db.run("CREATE UNIQUE INDEX IF NOT EXISTS idx_documents_hash ON documents(hash);")
    }

    func fetchAll() throws -> [Document] {
        var results: [Document] = []
        for row in try db.prepare(documents) {
            let doc = Document(
                id: row[id],
                category: row[category],
                filepath: row[filepath],
                filename: row[filename],
                status: row[status],
                confidence: row[confidence],
                lastModified: row[lastModified],
                year: row[year],
                owner: row[owner],
                accountId: row[accountId],
                period: row[period],
                hash: row[hash]
            )
            results.append(doc)
        }
        return results
    }

    struct CategorySummary {
        let category: String
        let inserted: Int
        let updated: Int
        let unchanged: Int
    }

    func fetchCategorySummary() throws -> [CategorySummary] {
        var summaries: [CategorySummary] = []

        let query = """
        SELECT category,
               SUM(CASE WHEN status='Inserted' THEN 1 ELSE 0 END) AS inserted,
               SUM(CASE WHEN status='Updated' THEN 1 ELSE 0 END) AS updated,
               SUM(CASE WHEN status='Unchanged' THEN 1 ELSE 0 END) AS unchanged
        FROM documents
        GROUP BY category;
        """

        for row in try db.prepare(query) {
            let category = row[0] as! String
            let inserted = row[1] as! Int64
            let updated = row[2] as! Int64
            let unchanged = row[3] as! Int64

            summaries.append(CategorySummary(
                category: category,
                inserted: Int(inserted),
                updated: Int(updated),
                unchanged: Int(unchanged)
            ))
        }
        return summaries
    }

    // Upsert helper: insert or update on conflict
    func upsertDocument(doc: Document) throws {
        let sql = """
        INSERT INTO documents (id, category, filepath, filename, status, confidence,
                               last_modified, year, owner, account_id, period, hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(hash) DO UPDATE SET
            category=excluded.category,
            filepath=excluded.filepath,
            filename=excluded.filename,
            status=excluded.status,
            confidence=excluded.confidence,
            last_modified=excluded.last_modified,
            year=excluded.year,
            owner=excluded.owner,
            account_id=excluded.account_id,
            period=excluded.period;
        """
        try db.run(sql,
                   doc.id, doc.category, doc.filepath, doc.filename, doc.status,
                   doc.confidence, doc.lastModified, doc.year, doc.owner,
                   doc.accountId, doc.period, doc.hash)
    }
}

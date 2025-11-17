import Foundation
import GRDB

class DBManager {
    static let shared = DBManager()

    private var dbQueue: DatabaseQueue?
    private(set) var isConnected: Bool = false

    private init() {
        connect()
    }

    private func connect() {
        do {
            let dbURL = AppPaths.databaseURL
            dbQueue = try DatabaseQueue(path: dbURL.path)
            isConnected = true
            migrateDatabase()
        } catch {
            print("❌ Failed to connect to database: \(error)")
            isConnected = false
        }
    }

    private func migrateDatabase() {
        guard let dbQueue = dbQueue else { return }
        var migrator = DatabaseMigrator()

        migrator.registerMigration("createFileIndex") { db in
            try db.create(table: FileIndexRow.databaseTableName) { t in
                t.autoIncrementedPrimaryKey("id")
                t.column("path", .text).notNull()
                t.column("coverage", .double).notNull()
            }
        }

        do {
            try migrator.migrate(dbQueue)
        } catch {
            print("❌ Migration failed: \(error)")
        }
    }

    func saveFileIndexRow(_ row: FileIndexRow) throws {
        guard let dbQueue = dbQueue else { throw DatabaseError(resultCode: .SQLITE_ERROR) }
        try dbQueue.write { db in
            try row.insert(db)
        }
    }

    func fetchAllFileIndexRows() throws -> [FileIndexRow] {
        guard let dbQueue = dbQueue else { throw DatabaseError(resultCode: .SQLITE_ERROR) }
        return try dbQueue.read { db in
            try FileIndexRow.fetchAll(db)
        }
    }

    func clearAllRows() throws {
        guard let dbQueue = dbQueue else { throw DatabaseError(resultCode: .SQLITE_ERROR) }
        try dbQueue.write { db in
            try db.execute(sql: "DELETE FROM \(FileIndexRow.databaseTableName)")
        }
    }
}

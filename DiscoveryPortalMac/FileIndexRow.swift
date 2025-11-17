import Foundation
import GRDB

struct FileIndexRow: Codable, FetchableRecord, PersistableRecord, Identifiable {
    var id: Int64?
    var path: String
    var coverage: Double

    static let databaseTableName = "fileIndex"

    enum Columns: String, ColumnExpression {
        case id, path, coverage
    }

    init(id: Int64? = nil, path: String, coverage: Double) {
        self.id = id
        self.path = path
        self.coverage = coverage
    }
}

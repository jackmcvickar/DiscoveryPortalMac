import Foundation

/// Represents a directory the user has chosen to include.
struct DirectoryInfo: Identifiable, Codable, Hashable {
    var id = UUID()
    var path: String
    var dateAdded: Date = Date()
}

/// Represents a summary of indexing progress.
struct IndexingProgress: Codable, Hashable {
    var totalFiles: Int
    var processedFiles: Int

    var percentage: Double {
        guard totalFiles > 0 else { return 0.0 }
        return Double(processedFiles) / Double(totalFiles)
    }
}

import Foundation

struct Document: Identifiable {
    let id: Int64
    let category: String
    let filepath: String
    let filename: String
    let status: String
    let confidence: Double?
    let lastModified: String
    let year: String?
    let owner: String?
    let accountId: String?
    let period: String?
    let hash: String
}

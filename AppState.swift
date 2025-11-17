import Foundation
import Combine

class AppState: ObservableObject {
    @Published var fileIndexRows: [FileIndexRow] = []
    @Published var isLoading: Bool = false
    @Published var errorMessage: String?
    @Published var includedDirectories: [DirectoryInfo] = []
    @Published var reindexOnLaunch: Bool = false {
        didSet {
            UserDefaults.standard.set(reindexOnLaunch, forKey: "reindexOnLaunch")
        }
    }
    @Published var progress: IndexingProgress = IndexingProgress(totalFiles: 0, processedFiles: 0)

    private let dbManager = DBManager.shared
    private let coverageBuilder = CoverageBuilder()

    init() {
        loadSavedDirectories()
        reindexOnLaunch = UserDefaults.standard.bool(forKey: "reindexOnLaunch")
        loadFileIndex()

        if reindexOnLaunch && !includedDirectories.isEmpty {
            indexIncludedDirectories()
        }
    }

    var isDBConnected: Bool {
        dbManager.isConnected
    }

    func loadFileIndex() {
        isLoading = true
        DispatchQueue.global(qos: .userInitiated).async {
            do {
                let rows = try self.dbManager.fetchAllFileIndexRows()
                DispatchQueue.main.async {
                    self.fileIndexRows = rows
                    self.isLoading = false
                }
            } catch {
                DispatchQueue.main.async {
                    self.errorMessage = "Failed to load file index: \(error)"
                    self.isLoading = false
                }
            }
        }
    }

    func addDirectory(_ path: String) {
        let dir = DirectoryInfo(path: path)
        includedDirectories.append(dir)
        saveDirectories()
    }

    func indexIncludedDirectories() {
        isLoading = true
        progress = IndexingProgress(totalFiles: 0, processedFiles: 0)

        let indexer = FileIndexer()
        let paths = includedDirectories.map { $0.path }
        indexer.indexFiles(at: paths,
                           progress: { processed, total in
                               DispatchQueue.main.async {
                                   self.progress = IndexingProgress(totalFiles: total, processedFiles: processed)
                               }
                           },
                           completion: {
                               self.loadFileIndex()
                               self.isLoading = false
                           })
    }

    func clearAll() {
        fileIndexRows.removeAll()
        includedDirectories.removeAll()
        saveDirectories()
    }

    private func saveDirectories() {
        let encoded = try? JSONEncoder().encode(includedDirectories)
        UserDefaults.standard.set(encoded, forKey: "includedDirectories")
    }

    private func loadSavedDirectories() {
        if let data = UserDefaults.standard.data(forKey: "includedDirectories"),
           let decoded = try? JSONDecoder().decode([DirectoryInfo].self, from: data) {
            includedDirectories = decoded
        }
    }
}

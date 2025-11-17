import Foundation

class FileIndexer {
    private let dbManager = DBManager.shared
    private let coverageBuilder = CoverageBuilder()

    func indexFiles(at directories: [String],
                    progress: @escaping (Int, Int) -> Void,
                    completion: @escaping () -> Void) {
        DispatchQueue.global(qos: .userInitiated).async {
            // Count total entries (files + directories) first
            let total = directories.reduce(0) { count, dir in
                count + (FileManager.default.enumerator(atPath: dir)?
                            .allObjects.compactMap { $0 as? String }.count ?? 0)
            }
            var processed = 0

            for dir in directories {
                let fileManager = FileManager.default
                let enumerator = fileManager.enumerator(atPath: dir)

                while let element = enumerator?.nextObject() as? String {
                    let fullPath = dir + "/" + element
                    var isDir: ObjCBool = false
                    if fileManager.fileExists(atPath: fullPath, isDirectory: &isDir), !isDir.boolValue {
                        let coverage = self.coverageBuilder.calculateCoverage(forFileAtPath: fullPath)
                        let row = FileIndexRow(id: nil, path: fullPath, coverage: coverage)
                        do {
                            try self.dbManager.saveFileIndexRow(row)
                        } catch {
                            print("❌ Failed to save file \(fullPath): \(error)")
                        }
                    }
                    processed += 1
                    progress(processed, total)
                }
            }

            DispatchQueue.main.async {
                completion()
            }
        }
    }
}

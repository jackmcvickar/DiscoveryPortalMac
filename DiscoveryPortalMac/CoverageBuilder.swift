import Foundation

class CoverageBuilder {
    func buildCoverage(forFiles files: [String]) -> [FileIndexRow] {
        return files.map { path in
            let coverage = calculateCoverage(forFileAtPath: path)
            return FileIndexRow(id: nil, path: path, coverage: coverage)
        }
    }

    func calculateCoverage(forFileAtPath path: String) -> Double {
        do {
            let contents = try String(contentsOfFile: path, encoding: .utf8)
            let lines = contents.split(separator: "\n", omittingEmptySubsequences: false)
            let nonEmpty = lines.filter { !$0.trimmingCharacters(in: .whitespaces).isEmpty }
            if lines.isEmpty { return 0.0 }
            return Double(nonEmpty.count) / Double(lines.count)
        } catch {
            return 0.0
        }
    }
}

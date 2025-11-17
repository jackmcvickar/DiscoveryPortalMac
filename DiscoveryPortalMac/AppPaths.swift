import Foundation

struct AppPaths {
    static var applicationSupportDirectory: URL {
        let fm = FileManager.default
        let urls = fm.urls(for: .applicationSupportDirectory, in: .userDomainMask)
        let appSupport = urls.first!.appendingPathComponent("DiscoveryPortalMac", isDirectory: true)

        if !fm.fileExists(atPath: appSupport.path) {
            try? fm.createDirectory(at: appSupport, withIntermediateDirectories: true)
        }
        return appSupport
    }

    static var databaseURL: URL {
        return applicationSupportDirectory.appendingPathComponent("app.sqlite")
    }

    static var logsURL: URL {
        return applicationSupportDirectory.appendingPathComponent("logs.txt")
    }
}

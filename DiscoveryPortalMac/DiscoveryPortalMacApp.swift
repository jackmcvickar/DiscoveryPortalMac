import SwiftUI

@main
struct DiscoveryPortalMacApp: App {
    @StateObject private var appState = AppState()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(appState)
        }
        Settings {
            PreferencesView()
                .environmentObject(appState)
        }
    }
}

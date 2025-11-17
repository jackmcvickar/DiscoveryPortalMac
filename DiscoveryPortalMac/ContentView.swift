import SwiftUI

struct ContentView: View {
    @EnvironmentObject var appState: AppState

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Discovery Portal")
                .font(.largeTitle)
                .padding(.bottom, 8)

            Text("Included Directories: \(appState.includedDirectories.count)")
                .font(.headline)

            HStack(spacing: 12) {
                Button("Add Directory") {
                    openDirectoryPicker()
                }
                Button("Index Files") {
                    appState.indexIncludedDirectories()
                }
                Button("Clear All") {
                    appState.clearAll()
                }
            }
            .padding(.vertical)

            if appState.isLoading {
                ProgressView("Indexing \(appState.progress.processedFiles) of \(appState.progress.totalFiles) files…",
                             value: appState.progress.percentage,
                             total: 1.0)
                    .padding(.bottom, 8)
            }

            IndexedFilesView()
                .environmentObject(appState)

            Spacer()
        }
        .padding()
    }

    private func openDirectoryPicker() {
        let panel = NSOpenPanel()
        panel.canChooseFiles = false
        panel.canChooseDirectories = true
        panel.allowsMultipleSelection = true

        if panel.runModal() == .OK {
            let paths = panel.urls.map { $0.path }
            for path in paths {
                appState.addDirectory(path)
            }
        }
    }
}

#Preview {
    ContentView()
        .environmentObject(AppState())
}

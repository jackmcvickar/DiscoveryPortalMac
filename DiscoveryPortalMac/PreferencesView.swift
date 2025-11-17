import SwiftUI

struct PreferencesView: View {
    @EnvironmentObject var appState: AppState

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Preferences")
                .font(.largeTitle)
                .padding(.bottom, 8)

            HStack {
                Circle()
                    .fill(appState.isDBConnected ? Color.green : Color.red)
                    .frame(width: 12, height: 12)
                Text(appState.isDBConnected ? "Database Connected" : "Database Not Connected")
                    .font(.headline)
            }

            if let error = appState.errorMessage {
                Text("Error: \(error)")
                    .foregroundColor(.red)
                    .padding(.top, 4)
            }

            VStack(alignment: .leading, spacing: 4) {
                Text("Included Directories:")
                    .font(.headline)
                if appState.includedDirectories.isEmpty {
                    Text("None")
                        .foregroundColor(.secondary)
                } else {
                    ForEach(appState.includedDirectories) { dir in
                        VStack(alignment: .leading) {
                            Text(dir.path)
                                .font(.subheadline)
                                .lineLimit(1)
                                .truncationMode(.middle)
                            Text("Added: \(dir.dateAdded.formatted(date: .abbreviated, time: .shortened))")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                    }
                }
            }

            Toggle("Re‑Index on Launch", isOn: $appState.reindexOnLaunch)
                .padding(.top, 8)

            Spacer()
        }
        .padding()
        .frame(minWidth: 400, minHeight: 300)
    }
}

#Preview {
    PreferencesView()
        .environmentObject(AppState())
}

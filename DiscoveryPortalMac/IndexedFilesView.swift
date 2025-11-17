import SwiftUI

struct IndexedFilesView: View {
    @EnvironmentObject var appState: AppState

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Indexed Files")
                .font(.title2)
                .padding(.bottom, 4)

            if appState.isLoading {
                ProgressView("Loading files...")
                    .padding()
            } else if appState.fileIndexRows.isEmpty {
                Text("No files indexed yet.")
                    .foregroundColor(.secondary)
            } else {
                List(appState.fileIndexRows, id: \.id) { file in
                    VStack(alignment: .leading) {
                        Text(file.path)
                            .font(.headline)
                            .lineLimit(1)
                            .truncationMode(.middle)

                        Text("Coverage: \(String(format: "%.2f", file.coverage))")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }
                    .padding(.vertical, 4)
                }
            }
        }
        .padding()
    }
}

#Preview {
    IndexedFilesView()
        .environmentObject(AppState())
}

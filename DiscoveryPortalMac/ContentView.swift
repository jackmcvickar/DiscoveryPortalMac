import SwiftUI
import Charts

struct ContentView: View {
    @State private var documents: [Document] = []
    @State private var summaries: [DocumentRepository.CategorySummary] = []

    var body: some View {
        VStack {
            Text("Documents: \(documents.count)")
                .font(.headline)
                .padding()

            // Stacked bar chart
            if !summaries.isEmpty {
                Chart {
                    ForEach(summaries, id: \.category) { summary in
                        BarMark(
                            x: .value("Category", summary.category),
                            y: .value("Inserted", summary.inserted)
                        )
                        .foregroundStyle(.green)

                        BarMark(
                            x: .value("Category", summary.category),
                            y: .value("Updated", summary.updated)
                        )
                        .foregroundStyle(.orange)

                        BarMark(
                            x: .value("Category", summary.category),
                            y: .value("Unchanged", summary.unchanged)
                        )
                        .foregroundStyle(.blue)
                    }
                }
                .frame(height: 300)
                .padding()
            }

            // List view
            List(summaries, id: \.category) { summary in
                VStack(alignment: .leading) {
                    Text(summary.category)
                        .font(.headline)
                    Text("Inserted: \(summary.inserted)")
                        .foregroundColor(.green)
                    Text("Updated: \(summary.updated)")
                        .foregroundColor(.orange)
                    Text("Unchanged: \(summary.unchanged)")
                        .foregroundColor(.blue)
                }
                .padding(.vertical, 4)
            }
        }
        .onAppear {
            do {
                let repo = try DocumentRepository()
                documents = try repo.fetchAll()
                summaries = try repo.fetchCategorySummary()
                print("Fetched \(documents.count) documents")
            } catch {
                print("DB error: \(error)")
            }
        }
    }
}

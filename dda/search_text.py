import sqlite3
import sys

DB_PATH = "/Users/jackmcvickar/DiscoveryPortalMac/Data/dda.db"

def search_text(query):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Use FTS5 MATCH query
    cur.execute("""
        SELECT f.path, snippet(extracts, 0, '[', ']', '...', 20)
        FROM extracts
        JOIN files f ON f.id = extracts.file_id
        WHERE extracts MATCH ?
        LIMIT 20
    """, (query,))
    results = cur.fetchall()
    conn.close()

    if not results:
        print(f"❌ No matches for '{query}'")
    else:
        print(f"🔎 Results for '{query}':")
        for path, snippet in results:
            print(f"- {path}\n  ...{snippet}...\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 search_text.py <keyword>")
    else:
        search_text(sys.argv[1])

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "Data/dda.db"

def build_expected_periods(start_period="2024-04", end_period="2025-11"):
    start_year, start_month = map(int, start_period.split("-"))
    end_year, end_month = map(int, end_period.split("-"))
    periods = []
    for y in range(start_year, end_year + 1):
        for m in range(1, 13):
            if (y == start_year and m < start_month) or (y == end_year and m > end_month):
                continue
            periods.append(f"{y}-{m:02d}")
    return periods

def run_dashboard(start_period="2024-04", end_period="2025-11"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    expected_periods = build_expected_periods(start_period, end_period)

    cursor.execute("SELECT account_name, account_number, account_type, owner, status FROM accounts_registry")
    registry_accounts = cursor.fetchall()

    dashboard_rows = []
    for account_name, account_number, account_type, owner, status in registry_accounts:
        cursor.execute(
            "SELECT period FROM documents WHERE account_id=? OR account_id LIKE ?",
            (account_name, f"%{account_number[-4:]}%")
        )
        docs = cursor.fetchall()
        found_periods = [row[0] for row in docs if row[0]]

        completeness = (len(found_periods) / len(expected_periods)) * 100 if expected_periods else 0
        status_flag = "✅ Complete" if completeness == 100 else "⚠️ Missing" if completeness > 0 else "❌ None"

        dashboard_rows.append({
            "Account": account_name,
            "Owner": owner,
            "Type": account_type,
            "Status": status,
            "Expected": len(expected_periods),
            "Found": len(found_periods),
            "Completeness": round(completeness, 1),
            "StatusFlag": status_flag,
            "FoundPeriods": found_periods
        })

    conn.close()
    return dashboard_rows, expected_periods

def export_dashboard(rows, expected_periods, start_period, end_period):
    df = pd.DataFrame(rows)
    file = f"reports/dashboard_{start_period}_to_{end_period}.csv"
    df.to_csv(file, index=False)
    print(f"📊 Dashboard exported to {file}")

    # Per-account bar chart
    plt.figure(figsize=(12, 6))
    colors = ["green" if c == 100 else "orange" if c > 0 else "red" for c in df["Completeness"]]
    plt.bar(df["Account"], df["Completeness"], color=colors)
    plt.xticks(rotation=90, fontsize=8)
    plt.ylabel("Completeness (%)")
    plt.title(f"Account Completeness {start_period} to {end_period}")
    plt.tight_layout()
    chart_file = f"reports/dashboard_chart_{start_period}_to_{end_period}.png"
    plt.savefig(chart_file)
    print(f"🎨 Chart exported to {chart_file}")

    # Trend line chart
    month_scores = []
    for month in expected_periods:
        total_accounts = len(rows)
        covered = sum(1 for r in rows if month in r["FoundPeriods"])
        completeness = (covered / total_accounts) * 100 if total_accounts else 0
        month_scores.append(completeness)

    plt.figure(figsize=(12, 6))
    plt.plot(expected_periods, month_scores, marker="o", color="blue")
    plt.xticks(rotation=90, fontsize=8)
    plt.ylabel("Completeness (%)")
    plt.title("Completeness Trend by Month")
    plt.grid(True)
    plt.tight_layout()
    trend_file = f"reports/dashboard_trend_{start_period}_to_{end_period}.png"
    plt.savefig(trend_file)
    print(f"📈 Trend chart exported to {trend_file}")

    # Stacked owner chart
    owners = df["Owner"].unique()
    owner_data = {owner: [] for owner in owners}
    for month in expected_periods:
        for owner in owners:
            total_accounts = len(df[df["Owner"] == owner])
            covered = sum(1 for r in rows if r["Owner"] == owner and month in r["FoundPeriods"])
            completeness = (covered / total_accounts) * 100 if total_accounts else 0
            owner_data[owner].append(completeness)

    plt.figure(figsize=(12, 6))
    bottom = [0] * len(expected_periods)
    for owner in owners:
        plt.bar(expected_periods, owner_data[owner], bottom=bottom, label=owner)
        bottom = [b + v for b, v in zip(bottom, owner_data[owner])]
    plt.xticks(rotation=90, fontsize=8)
    plt.ylabel("Completeness (%)")
    plt.title("Completeness by Owner (Stacked)")
    plt.legend()
    plt.tight_layout()
    stacked_file = f"reports/dashboard_owner_{start_period}_to_{end_period}.png"
    plt.savefig(stacked_file)
    print(f"👥 Owner stacked chart exported to {stacked_file}")

if __name__ == "__main__":
    start = "2024-04"
    end = "2025-11"
    rows, expected_periods = run_dashboard(start, end)

    print("\nDashboard Summary:\n")
    for r in rows:
        print(
            f"{r['Account']} ({r['Owner']}) | {r['Type']} | Status {r['Status']} | "
            f"Expected {r['Expected']} | Found {r['Found']} | Completeness {r['Completeness']}% | {r['StatusFlag']}"
        )

    export_dashboard(rows, expected_periods, start, end)

# end of script
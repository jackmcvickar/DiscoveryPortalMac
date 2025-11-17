import os, csv

def export_csv(records, outputs_path):
    os.makedirs(outputs_path, exist_ok=True)
    out_file = os.path.join(outputs_path, "final_status_summary.csv")
    with open(out_file, "w", newline="") as f:
        writer = csv.writer(f)
        for filepath, category, status, account_id in records:
            writer.writerow([filepath, category, account_id, status])
    print(f"📑 Final status summary exported to {out_file}")
# end of script
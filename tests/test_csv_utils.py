import csv, os
from dda.modules import csv_utils

def test_export_csv(tmp_path):
    records = [("/tmp/file.pdf", "general", "Processed", None)]
    out_dir = tmp_path
    csv_utils.export_csv(records, str(out_dir))

    out_file = out_dir / "final_status_summary.csv"
    assert out_file.exists()
    with open(out_file) as f:
        reader = csv.reader(f)
        rows = list(reader)
    assert rows[0][0].endswith("file.pdf")
# end of script
# log_utils.py

import os
import datetime

def get_log_file(logs_path: str) -> str:
    """Return a timestamped log file path inside logs_path."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(logs_path, f"pipeline_run_{timestamp}.log")

def write_log(logs_path: str, summary: str, details: list[str]):
    """Write summary and details to a timestamped log file."""
    log_file = get_log_file(logs_path)
    with open(log_file, "w") as f:
        f.write("=== Pipeline Run Log ===\n")
        f.write(f"Timestamp: {datetime.datetime.now().isoformat()}\n\n")
        f.write(summary + "\n\n")
        for line in details:
            f.write(line + "\n")
    print(f"Log written to {log_file}")

# end of script
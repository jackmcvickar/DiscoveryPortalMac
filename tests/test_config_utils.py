import pytest
from dda.modules import config_utils

def test_load_config_sections(tmp_path):
    # Create a temporary config.ini
    cfg = tmp_path / "config.ini"
    cfg.write_text("[paths]\ndocs_path=/tmp/docs\noutputs_path=/tmp/out\ndb_path=/tmp/db.sqlite\n")

    docs, outputs, db = config_utils.load_config(str(cfg))
    assert docs == "/tmp/docs"
    assert outputs == "/tmp/out"
    assert db == "/tmp/db.sqlite"
# end of script
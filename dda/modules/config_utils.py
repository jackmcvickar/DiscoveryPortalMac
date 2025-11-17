import configparser

def load_config(config_path="/Users/jackmcvickar/DiscoveryPortalMac/config.ini"):
    config = configparser.ConfigParser()
    config.read(config_path)

    if not config.has_section("paths"):
        raise RuntimeError(f"Config file at {config_path} missing [paths] section")

    docs_path = config.get("paths", "docs_path")
    outputs_path = config.get("paths", "outputs_path")
    db_path = config.get("paths", "db_path")

    print(f"🔎 Config loaded from {config_path}")
    print(f"📂 docs_path={docs_path}, outputs_path={outputs_path}, db_path={db_path}")

    return docs_path, outputs_path, db_path
# end of script
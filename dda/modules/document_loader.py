from dda.modules.config_utils import load_config
from dda.modules.walker import walk_documents
from dda.modules.csv_utils import export_csv
from dda.modules.db_utils import insert_into_db

def main():
    docs_path, outputs_path, db_path = load_config()
    records = walk_documents(docs_path)
    export_csv(records, outputs_path)
    insert_into_db(records, db_path)

if __name__ == "__main__":
    main()

# end of script
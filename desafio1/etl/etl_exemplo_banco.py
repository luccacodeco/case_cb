import json
import argparse
import pandas as pd
from pathlib import Path
from utils import get_engine, validate_json

BASE_DIR = Path(__file__).parent.parent
ERP_FILE = BASE_DIR / "ERP.json"
SCHEMA_FILE = BASE_DIR / "schema.json"

def extract_data():
    with open(ERP_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def transform_data(data):
    guest_checks = data.get("guestChecks", [])
    df_guest_checks = pd.json_normalize(guest_checks)
    df_taxes = pd.json_normalize(guest_checks, record_path="taxes", meta=["guestCheckId"])
    df_detail_lines = pd.json_normalize(guest_checks, record_path="detailLines", meta=["guestCheckId"])
    
    menu_items_records = []
    for gc in guest_checks:
        for dl in gc.get("detailLines", []):
            mi = dl.get("menuItem")
            if mi:
                mi["guestCheckId"] = gc["guestCheckId"]
                mi["guestCheckLineItemId"] = dl["guestCheckLineItemId"]
                menu_items_records.append(mi)
    df_menu_items = pd.DataFrame(menu_items_records)
    return df_guest_checks, df_taxes, df_detail_lines, df_menu_items

def load_to_db(dfs):
    engine = get_engine()
    dfs[0].to_sql("guest_checks", engine, if_exists="append", index=False)
    dfs[1].to_sql("taxes", engine, if_exists="append", index=False)
    dfs[2].to_sql("detail_lines", engine, if_exists="append", index=False)
    dfs[3].to_sql("menu_items", engine, if_exists="append", index=False)
    print("Dados inseridos com sucesso.")

def main(args):
    data = extract_data()
    if args.validate:
        errors = validate_json(data, SCHEMA_FILE)
        if errors:
            print("Erros encontrados no JSON:")
            for e in errors:
                print(f"- {list(e.path)}: {e.message}")
        else:
            print("JSON válido conforme o schema.")
    if args.load:
        dfs = transform_data(data)
        load_to_db(dfs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETL para ERP.json")
    parser.add_argument("--validate", action="store_true", help="Valida o JSON com base no schema.")
    parser.add_argument("--load", action="store_true", help="Carrega os dados no banco.")
    args = parser.parse_args()
    main(args)

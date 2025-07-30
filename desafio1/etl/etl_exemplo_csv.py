import json
import argparse
import pandas as pd
from pathlib import Path
from utils import get_engine, validate_json

BASE_DIR = Path(__file__).parent.parent
ERP_FILE = BASE_DIR / "ERP.json"
SCHEMA_FILE = BASE_DIR / "schema.json"


def extract_data():
    """Lê o ERP.json e retorna o dicionário."""
    with open(ERP_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def transform_data(data):
    """Normaliza o JSON em DataFrames pandas."""
    guest_checks = data.get("guestChecks", [])

    df_guest_checks = pd.json_normalize(guest_checks)

    df_taxes = pd.json_normalize(
        guest_checks,
        record_path="taxes",
        meta=["guestCheckId"]
    )

    df_detail_lines = pd.json_normalize(
        guest_checks,
        record_path="detailLines",
        meta=["guestCheckId"]
    )

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
    """Insere os DataFrames no banco de dados usando SQLAlchemy."""
    engine = get_engine()
    dfs[0].to_sql("guest_checks", engine, if_exists="append", index=False)
    dfs[1].to_sql("taxes", engine, if_exists="append", index=False)
    dfs[2].to_sql("detail_lines", engine, if_exists="append", index=False)
    dfs[3].to_sql("menu_items", engine, if_exists="append", index=False)
    print("Dados inseridos com sucesso no banco de dados.")


def save_to_csv(dfs):
    """Salva os DataFrames como arquivos CSV."""
    output_dir = BASE_DIR / "output_csv"
    output_dir.mkdir(exist_ok=True)
    dfs[0].to_csv(output_dir / "guest_checks.csv", index=False)
    dfs[1].to_csv(output_dir / "taxes.csv", index=False)
    dfs[2].to_csv(output_dir / "detail_lines.csv", index=False)
    dfs[3].to_csv(output_dir / "menu_items.csv", index=False)
    print(f"CSVs salvos em {output_dir}")


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

    if args.csv:
        dfs = transform_data(data)
        save_to_csv(dfs)

    if args.load:
        dfs = transform_data(data)
        load_to_db(dfs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETL para ERP.json")
    parser.add_argument("--validate", action="store_true", help="Valida o JSON com base no schema.")
    parser.add_argument("--csv", action="store_true", help="Exporta dados como CSV.")
    parser.add_argument("--load", action="store_true", help="Carrega os dados no banco.")
    args = parser.parse_args()

    main(args)

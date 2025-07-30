import json
import os
from jsonschema import validate, Draft7Validator
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_engine():
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL não configurado no .env")
    return create_engine(DATABASE_URL)

def validate_json(json_data, schema_file):
    with open(schema_file, "r", encoding="utf-8") as f:
        schema = json.load(f)
    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(json_data), key=lambda e: e.path)
    return errors

import streamlit as st
import requests
import json
import os

def get_secret(key, default_val=""):
    try:
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, default_val)

TURSO_DB_URL = get_secret("TURSO_DB_URL", "https://turso-db-create-architect-portfolio-abhibhdauriya.aws-ap-south-1.turso.io")
TURSO_AUTH_TOKEN = get_secret("TURSO_AUTH_TOKEN", "")

if TURSO_DB_URL.startswith("libsql://"):
    TURSO_DB_URL = TURSO_DB_URL.replace("libsql://", "https://")

HEADERS = {
    "Authorization": f"Bearer {TURSO_AUTH_TOKEN}",
    "Content-Type": "application/json"
}

def execute_query(sql: str, params: list = None):
    if params is None:
        params = []
    
    formatted_args = []
    for p in params:
        if p is None:
            formatted_args.append({"type": "null"})
        elif isinstance(p, int):
            formatted_args.append({"type": "integer", "value": str(p)})
        elif isinstance(p, float):
            formatted_args.append({"type": "float", "value": p})
        else:
            formatted_args.append({"type": "text", "value": str(p)})

    payload = {
        "requests": [
            {
                "type": "execute",
                "stmt": {
                    "sql": sql,
                    "args": formatted_args
                }
            },
            {"type": "close"}
        ]
    }

    try:
        if not TURSO_AUTH_TOKEN:
            return []
            
        response = requests.post(
            f"{TURSO_DB_URL}/v2/pipeline",
            headers=HEADERS,
            data=json.dumps(payload),
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        if "results" in data and len(data["results"]) > 0:
            res = data["results"][0].get("response", {}).get("result", {})
            if "rows" in res:
                rows = []
                for row in res["rows"]:
                    rows.append([col.get("value") for col in row])
                return rows
        return True
    except Exception as err:
        return []

def init_db():
    # Projects table with direct file payload and contact
    schema_projects = """
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        video_url TEXT,
        problem TEXT NOT NULL,
        solution TEXT NOT NULL,
        tech_stack TEXT NOT NULL,
        live_link TEXT,
        github_link TEXT,
        phone_contact TEXT,
        excel_raw_name TEXT,
        excel_raw_data TEXT,
        excel_proc_name TEXT,
        excel_proc_data TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    execute_query(schema_projects)

    # Settings table for Dynamic Password & Admin Email
    schema_settings = """
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    );
    """
    execute_query(schema_settings)

    # Initialize default admin credentials if not set
    existing_pass = execute_query("SELECT value FROM settings WHERE key = 'admin_pass'")
    if not existing_pass or len(existing_pass) == 0:
        execute_query("INSERT INTO settings (key, value) VALUES ('admin_pass', 'Abhi#Enterprise2026')")
    
    existing_email = execute_query("SELECT value FROM settings WHERE key = 'admin_email'")
    if not existing_email or len(existing_email) == 0:
        execute_query("INSERT INTO settings (key, value) VALUES ('admin_email', 'admin@example.com')")

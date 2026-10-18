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
            return None, "Turso Auth Token Missing in Secrets."
            
        response = requests.post(
            f"{TURSO_DB_URL}/v2/pipeline",
            headers=HEADERS,
            data=json.dumps(payload),
            timeout=12
        )
        response.raise_for_status()
        data = response.json()
        
        if "results" in data and len(data["results"]) > 0:
            first_res = data["results"][0]
            if "error" in first_res.get("response", {}):
                return None, first_res["response"]["error"].get("message", "Database Error")
            
            res = first_res.get("response", {}).get("result", {})
            if "rows" in res:
                rows = []
                for row in res["rows"]:
                    rows.append([col.get("value") for col in row])
                return rows, None
        return [], None
    except Exception as err:
        return None, str(err)

def init_db():
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

    # Auto Migration: Agar columns pehle se nahi hain toh add kar dega
    cols_to_add = [
        ("phone_contact", "TEXT"),
        ("excel_raw_name", "TEXT"),
        ("excel_raw_data", "TEXT"),
        ("excel_proc_name", "TEXT"),
        ("excel_proc_data", "TEXT")
    ]
    for col_name, col_type in cols_to_add:
        try:
            execute_query(f"ALTER TABLE projects ADD COLUMN {col_name} {col_type};")
        except Exception:
            pass

    schema_settings = """
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    );
    """
    execute_query(schema_settings)

    # Defaults
    execute_query("INSERT OR IGNORE INTO settings (key, value) VALUES ('admin_pass', 'Abhi#Enterprise2026')")
    execute_query("INSERT OR IGNORE INTO settings (key, value) VALUES ('admin_email', 'singha36161@gmail.com')")
    execute_query("INSERT OR IGNORE INTO settings (key, value) VALUES ('whatsapp_phone', '+918810915344')")

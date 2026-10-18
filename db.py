import streamlit as st
import requests
import json

TURSO_DB_URL = st.secrets.get("TURSO_DB_URL", "https://turso-db-create-architect-portfolio-abhibhdauriya.aws-ap-south-1.turso.io")[cite: 1]
TURSO_AUTH_TOKEN = st.secrets.get("TURSO_AUTH_TOKEN", "")

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
        response = requests.post(f"{TURSO_DB_URL}/v2/pipeline", headers=HEADERS, data=json.dumps(payload), timeout=8)
        response.raise_for_status()
        res = response.json()["results"][0]["response"]["result"]
        
        if "rows" in res:
            rows = []
            for row in res["rows"]:
                rows.append([col.get("value") for col in row])
            return rows
        return True
    except Exception as e:
        st.error(f"Database Query Error: {e}")
        return []

def init_db():
    schema = """
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
        excel_raw_link TEXT,
        excel_proc_link TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    execute_query(schema)

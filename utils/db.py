import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text

# Retrieve DB URL from Streamlit Secrets or Environment Variable
def get_db_engine():
    try:
        db_url = st.secrets["SUPABASE_URL"]
    except Exception:
        db_url = os.getenv("SUPABASE_URL", "")
    
    if not db_url:
        raise ValueError("SUPABASE_URL not found in st.secrets or environment variables.")
    
    # Ensure standard postgresql:// prefix for SQLAlchemy
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    return create_engine(db_url, pool_pre_ping=True)

def init_supabase_db():
    engine = get_db_engine()
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS ipc_invoices (
                id SERIAL PRIMARY KEY,
                ipc_number VARCHAR(100) UNIQUE NOT NULL,
                client VARCHAR(100),
                project_id VARCHAR(100),
                gross_amount DOUBLE PRECISION,
                vat_amount DOUBLE PRECISION,
                net_amount DOUBLE PRECISION,
                status VARCHAR(100),
                payment_date VARCHAR(100)
            );
        """))
        conn.commit()

def load_ipc_data():
    engine = get_db_engine()
    return pd.read_sql("SELECT * FROM ipc_invoices ORDER BY id ASC;", engine)

def insert_ipc_record(ipc_dict):
    engine = get_db_engine()
    with engine.connect() as conn:
        stmt = text("""
            INSERT INTO ipc_invoices (ipc_number, client, project_id, gross_amount, vat_amount, net_amount, status, payment_date)
            VALUES (:ipc_num, :client, :proj_id, :gross, :vat, :net, :status, :pdate)
            ON CONFLICT (ipc_number) DO UPDATE SET
                status = EXCLUDED.status,
                payment_date = EXCLUDED.payment_date;
        """)
        conn.execute(stmt, {
            "ipc_num": ipc_dict["IPC_Number"],
            "client": ipc_dict["Client"],
            "proj_id": ipc_dict["Project_ID"],
            "gross": ipc_dict["Gross_Amount_SAR"],
            "vat": ipc_dict["VAT_15_Percent"],
            "net": ipc_dict["Net_Amount_SAR"],
            "status": ipc_dict["Status"],
            "pdate": ipc_dict["Payment_Date"]
        })
        conn.commit()

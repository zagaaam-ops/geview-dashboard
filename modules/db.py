import os
import pandas as pd
from sqlalchemy import create_engine, text

def get_db_engine():
    # Fetch database URL from Streamlit secrets or environment variables
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        return None
    
    # Fix for SQLAlchemy requiring postgresql:// instead of postgres://
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    try:
        engine = create_engine(
            db_url,
            pool_pre_ping=True,  # Auto-reconnect lost pooled connections
            connect_args={"connect_timeout": 10}
        )
        return engine
    except Exception as e:
        print(f"Database connection engine error: {e}")
        return None

def init_db(engine, default_df):
    if engine is None:
        return
    
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS sites (
        site_id VARCHAR(50) PRIMARY KEY,
        name VARCHAR(100),
        region VARCHAR(50),
        contractor VARCHAR(100),
        overall_progress FLOAT,
        budget FLOAT,
        actual FLOAT,
        risk VARCHAR(20),
        start_date TIMESTAMP,
        baseline_finish TIMESTAMP,
        forecast_finish TIMESTAMP,
        lat FLOAT,
        lon FLOAT
    );
    """
    try:
        with engine.begin() as conn:
            conn.execute(text(create_table_sql))
            
            # Seed initial data if table is empty
            result = conn.execute(text("SELECT COUNT(*) FROM sites;"))
            count = result.scalar()
            if count == 0:
                db_df = default_df.copy()
                db_df.columns = [c.lower().replace(" ", "_") for c in db_df.columns]
                db_df.to_sql('sites', engine, if_exists='append', index=False)
    except Exception as e:
        print(f"Failed to initialize database tables: {e}")

def load_data_from_db(engine):
    query = "SELECT site_id AS \"Site ID\", name AS \"Name\", region AS \"Region\", contractor AS \"Contractor\", overall_progress AS \"Overall Progress\", budget AS \"Budget\", actual AS \"Actual\", risk AS \"Risk\", start_date AS \"Start Date\", baseline_finish AS \"Baseline Finish\", forecast_finish AS \"Forecast Finish\", lat, lon FROM sites ORDER BY site_id;"
    return pd.read_sql(query, engine)

def save_data_to_db(engine, df):
    if engine is None:
        return False
    db_df = df.copy()
    db_df.columns = [c.lower().replace(" ", "_") for c in db_df.columns]
    try:
        with engine.begin() as conn:
            conn.execute(text("TRUNCATE TABLE sites;"))
            db_df.to_sql('sites', conn, if_exists='append', index=False)
        return True
    except Exception as e:
        print(f"Error saving to database: {e}")
        return False

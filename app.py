import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()  # This command loads the environment variables from the .env file

def connect_db():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        st.error("Database URL is not set.")
        raise ValueError("DATABASE_URL is not set in environment variables")
    try:
        con = psycopg2.connect(database_url, cursor_factory=RealDictCursor)
        return con
    except psycopg2.OperationalError as e:
        st.error(f"Failed to connect to the database: {e}")
        raise

def setup_db():
    with connect_db() as con:
        with con.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS prompts (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    prompt TEXT NOT NULL,
                    favorite BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            con.commit()

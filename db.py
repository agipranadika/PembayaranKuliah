import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host="gondola.proxy.rlwy.net",
        port=57367,
        dbname="railway",
        user="postgres",
        password="tAwxGzaYZTkTejKfaZCsZoMHrnSOCNVk"
    )

def run_query(query, params=None, fetch=False):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    data = None
    if fetch:
        data = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return data
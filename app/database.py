import csv
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "sales.db"
CSV_PATH = BASE_DIR / "data" / "sales.csv"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_connection()

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_date TEXT NOT NULL,
            region TEXT NOT NULL,
            product TEXT NOT NULL,
            category TEXT NOT NULL,
            units INTEGER NOT NULL,
            price REAL NOT NULL
        )
        """
    )

    if not conn.execute("SELECT 1 FROM sales LIMIT 1").fetchone():
        with CSV_PATH.open("r", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            rows = [
                (
                    row["order_date"],
                    row["region"],
                    row["product"],
                    row["category"],
                    int(row["units"]),
                    float(row["price"]),
                )
                for row in reader
            ]

        conn.executemany(
            """
            INSERT INTO sales (order_date, region, product, category, units, price)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            rows,
        )

    conn.commit()
    conn.close()

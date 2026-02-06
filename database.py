import os
import pyodbc
 
def get_db_connection(access_db_path=None, driver=None):
    """
    Connect to an MS Access database file using ODBC and return a pyodbc Connection.

    - access_db_path: path to .accdb or .mdb file (defaults to 'attendance.accdb' next to this file)
    - driver: explicit ODBC driver name (optional). If omitted, common Access drivers are tried.
    """
    if access_db_path is None:
        access_db_path = os.path.join(os.path.dirname(__file__), "attendance.accdb")

    if not os.path.exists(access_db_path):
        raise FileNotFoundError(f"Access DB not found: {access_db_path}")

    drivers_to_try = [driver] if driver else [
        'Microsoft Access Driver (*.mdb, *.accdb)',
        'Microsoft Access Driver (*.accdb)',
        'Microsoft Access Driver (*.mdb)'
    ]

    last_err = None
    for drv in drivers_to_try:
        if not drv:
            continue
        conn_str = f'DRIVER={{{drv}}};DBQ={access_db_path};'
        try:
            return pyodbc.connect(conn_str, autocommit=True)
        except Exception as e:
            last_err = e

    raise RuntimeError(f"Could not connect to Access DB. Last error: {last_err}")


def test_connection(access_db_path=None, driver=None):
    """Simple connection test; returns True if a basic query succeeds."""
    conn = get_db_connection(access_db_path, driver)
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1")
        row = cur.fetchone()
        return bool(row and row[0] == 1)
    finally:
        conn.close()
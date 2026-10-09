"""
Cleanup script for Food Packaging AI test data.

Step 1 (safe preview, changes nothing):   python cleanup_test_data.py
Step 2 (apply the changes):               python cleanup_test_data.py --apply

What it does:
  - Deletes commodities named "Test Mango" and "string"
  - Renames packaging "Test Biodegradable Film" to "Biodegradable Film"
    (so the demo keeps a biodegradable option, without "Test" in the name)
"""
import sys
from pathlib import Path

from sqlalchemy import create_engine, inspect, text

APPLY = "--apply" in sys.argv

COMMODITIES_TO_DELETE = ["test mango", "string"]
PACKAGING_RENAME = ("Test Biodegradable Film", "Biodegradable Film")


def load_database_url():
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        sys.exit("Could not find .env next to this script. Put this file in the backend folder.")
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("DATABASE_URL"):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("DATABASE_URL not found in .env")


def find_table(tables, keyword, exclude=("recommend", "history")):
    matches = [t for t in tables if keyword in t.lower() and not any(x in t.lower() for x in exclude)]
    return matches[0] if matches else None


def main():
    engine = create_engine(load_database_url())
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("Tables found:", ", ".join(tables))
    print("Mode:", "APPLY (changes will be saved)" if APPLY else "PREVIEW (nothing will change)")
    print()

    commodity_table = find_table(tables, "commodit")
    packaging_table = find_table(tables, "packag")
    if not commodity_table or not packaging_table:
        sys.exit(f"Could not identify tables (commodity={commodity_table}, packaging={packaging_table}). "
                 "Send me the 'Tables found' line above.")
    for table in (commodity_table, packaging_table):
        columns = [c["name"] for c in inspector.get_columns(table)]
        if "name" not in columns or "id" not in columns:
            sys.exit(f"Table {table} has columns {columns}; expected 'id' and 'name'.")

    with engine.connect() as conn:
        print(f"Commodities table: {commodity_table}")
        for row in conn.execute(text(f"SELECT id, name FROM {commodity_table} ORDER BY id")):
            flag = "  <-- will be deleted" if str(row.name).lower() in COMMODITIES_TO_DELETE else ""
            print(f"  {row.id}: {row.name}{flag}")
        print()
        print(f"Packaging table: {packaging_table}")
        for row in conn.execute(text(f"SELECT id, name FROM {packaging_table} ORDER BY id")):
            flag = f"  <-- will be renamed to '{PACKAGING_RENAME[1]}'" if row.name == PACKAGING_RENAME[0] else ""
            print(f"  {row.id}: {row.name}{flag}")
        print()

    if not APPLY:
        print("Preview only. If this looks right, run:  python cleanup_test_data.py --apply")
        return

    try:
        with engine.begin() as conn:
            deleted = conn.execute(
                text(f"DELETE FROM {commodity_table} WHERE LOWER(name) = ANY(:names)"),
                {"names": COMMODITIES_TO_DELETE},
            ).rowcount
            renamed = conn.execute(
                text(f"UPDATE {packaging_table} SET name = :new WHERE name = :old"),
                {"new": PACKAGING_RENAME[1], "old": PACKAGING_RENAME[0]},
            ).rowcount
        print(f"Done. Commodities deleted: {deleted}. Packaging renamed: {renamed}.")
    except Exception as error:
        print("Nothing was changed because of an error:")
        print(error)
        print("Send me this message and I will fix the script.")


if __name__ == "__main__":
    main()

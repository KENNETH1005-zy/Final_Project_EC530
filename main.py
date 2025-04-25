import argparse, json, pandas as pd, logging
from messaging import MessageBroker
from database import Database
from ai_module import analyze_document

# 1) Setup logging to file
logging.basicConfig(
    filename="error_log.txt",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(message)s"
)

def main():
    parser = argparse.ArgumentParser(
        description="Analyze a text document for teaching materials."
    )
    parser.add_argument("doc_path", help="Path to a plaintext .txt document")
    args = parser.parse_args()

    # 2) Read the document
    try:
        with open(args.doc_path, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception:
        logging.exception("Failed to read document")
        print("❌ Could not read the document. See error_log.txt.")
        return

    # 3) Call the LLM
    try:
        result = analyze_document(text)
    except Exception:
        logging.exception("LLM analysis failed")
        print("❌ Analysis failed. See error_log.txt.")
        return

    # 4) Publish to Redis
    broker = MessageBroker()
    try:
        broker.publish("analysis_result", result)
    except Exception:
        logging.exception("Redis publish failed")
        print("❌ Could not publish to Redis. See error_log.txt.")

    # 5) Schema-conflict check
    db = Database()
    try:
        schema_df = db.handle_schema_conflict("analysis_results")
    except Exception:
        logging.exception("Failed to inspect existing schema")
        schema_df = pd.DataFrame()

    table_name = "analysis_results"
    if not schema_df.empty:
        print("⚠️ Table 'analysis_results' already exists with schema:")
        print(schema_df.to_string(index=False))
        choice = input("Overwrite (o), Rename (r), or Abort (a)? ").strip().lower()
        if choice == "o":
            db.conn.execute("DROP TABLE analysis_results")
            print("→ Dropped existing table.")
        elif choice == "r":
            new_name = input("Enter new table name: ").strip()
            table_name = new_name
            print(f"→ Will write to table '{table_name}'.")
        else:
            print("❌ Aborted saving to database.")
            return

    # 6) Serialize & save
    try:
        # Convert lists/dicts → JSON strings
        serial = {
            k: (json.dumps(v) if isinstance(v, (list, dict)) else v)
            for k, v in result.items()
        }
        df = pd.DataFrame([serial])
        db.create_table_dynamic(df, table_name)
    except Exception:
        logging.exception("Failed to save results to SQLite")
        print("❌ Saving to database failed. See error_log.txt.")
        return

    print("✅ Analysis complete. Published to Redis and saved to SQLite.")

if __name__ == "__main__":
    main()
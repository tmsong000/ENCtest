import os, sqlite3, shutil, tempfile

base_dir = os.path.dirname(os.path.abspath(__file__))
input_dir = os.path.join(base_dir, "export_gpkg")
output_folder = os.path.join(input_dir, "results")
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_dir):
    if not filename.endswith(".gpkg"): 
        continue

    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, filename)
    shutil.copy(os.path.join(input_dir, filename), temp_file)

    datset = os.path.splitext(filename)[0]
    escaped_value = datset.replace("'", "''")

    conn = sqlite3.connect(temp_file)
    cur = conn.cursor()

    cur.execute("""SELECT table_name FROM gpkg_contents WHERE data_type IN ('features','tiles');""")
    tables = [t[0] for t in cur.fetchall()]

    for table in tables:
        cur.execute(f"PRAGMA table_info('{table}')")
        columns = [c[1] for c in cur.fetchall()]
        if "DATSET" not in columns:
            cur.execute(f"""ALTER TABLE "{table}" ADD COLUMN DATSET TEXT DEFAULT '{escaped_value}'""")

    conn.commit()
    conn.close()

    shutil.move(temp_file, os.path.join(output_folder, filename))
    shutil.rmtree(temp_dir)

print("STEP2 complete")

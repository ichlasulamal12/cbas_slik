import os
import polars as pl

# ==========================================================
# CONFIG
# ==========================================================

SLIK_FOLDER = r"D:\Development\cbasslik\v2\Fasilitas Kredit"

PARQUET_FOLDER = r"D:\Development\cbasslik\v2\Fasilitas Kredit Parquet"

os.makedirs(PARQUET_FOLDER, exist_ok=True)

STRING_COLUMNS = [
    "npwp",
    "ktp"
]

# ==========================================================
# CONVERT
# ==========================================================

files = sorted([
    f for f in os.listdir(SLIK_FOLDER)
    if f.lower().endswith(".xlsx")
])

for i, file in enumerate(files, start=1):

    print(f"[{i}/{len(files)}] {file}")

    excel_file = os.path.join(SLIK_FOLDER, file)

    parquet_file = os.path.join(
        PARQUET_FOLDER,
        file.replace(".xlsx", ".parquet")
    )

    if os.path.exists(parquet_file):
        print("  Skip")
        continue

    # Read Excel
    df = pl.read_excel(
        excel_file,
        engine="calamine"
    )

    # Ubah kolom tertentu menjadi string
    expr = []

    for col in STRING_COLUMNS:
        if col in df.columns:
            expr.append(
                pl.col(col)
                .cast(pl.Utf8)
                .str.strip_chars()
            )

    if expr:
        df = df.with_columns(expr)

    # Simpan ke Parquet
    df.write_parquet(
        parquet_file,
        compression="snappy"
    )

    print(f"  Rows : {df.height:,}")
    print("  Selesai")

print("Done.")

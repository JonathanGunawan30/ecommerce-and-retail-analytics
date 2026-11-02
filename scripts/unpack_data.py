"""
Script otomatis untuk mengekstrak seluruh dataset terkompresi (.zip) pada folder data/.

Cara Penggunaan:
    python scripts/unpack_data.py
"""

from pathlib import Path
import zipfile


def unpack_all_data() -> None:
    project_root = Path(__file__).resolve().parent.parent
    data_dir = project_root / "data"

    zip_files = list(data_dir.rglob("*.zip"))
    if not zip_files:
        print("[Unpack] Tidak ditemukan file .zip di direktori data/.")
        return

    for zpath in zip_files:
        print(f"[Unpack] Mengekstrak {zpath.relative_to(project_root)} ...")
        with zipfile.ZipFile(zpath, "r") as zf:
            zf.extractall(zpath.parent)

    print("[Unpack] Berhasil! Seluruh dataset telah diekstrak ke bentuk file mentah aslinya.")


if __name__ == "__main__":
    unpack_all_data()

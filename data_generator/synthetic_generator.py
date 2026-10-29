"""
Synthetic Data Generator & Dirty Data Injector (Milestone 1)
Kategori 1: E-Commerce & Retail Analytics

Menghasilkan 3 entitas dataset terintegrasi:
1. transactions_dirty.csv (Fact Table, > 1.000.000 baris)
2. customers_dirty.csv (Dimension Table, > 50.000 baris)
3. clickstream_dirty.jsonl (Semi-structured JSON Lines, > 200.000 events)

Dilengkapi injeksi data kotor (Veracity Check) sebesar 8% (rentang wajib 5% - 10%):
- Missing Values pada kolom krusial
- Inconsistent Formatting pada penulisan nama kota / atribut string
- Outliers & Invalid Values (harga negatif, kuantitas negatif, tanggal di masa depan)
- Duplicate Records pada primary key (transaction_id, customer_id, event_id)
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd

SEED = 42

# Target awal dilebihkan di atas batas minimum (1M, 50k, 200k)
# agar setelah proses cleansing jumlah baris bersih tetap >= batas minimal.
DEFAULT_N_TRANSACTIONS = 1_150_000
DEFAULT_N_CUSTOMERS = 55_000
DEFAULT_N_CLICKSTREAM = 220_000
DEFAULT_DIRTY_RATE = 0.08  # 8% (sesuai ketentuan 5% - 10%)

STANDARD_CITIES = [
    "Jakarta",
    "Bandung",
    "Surabaya",
    "Medan",
    "Tangerang",
    "Yogyakarta",
    "Semarang",
]

CITY_DIRTY_VARIANTS = {
    "Jakarta": ["JKT", "jakarta", "DKI Jakarta", " jakarta ", "Jakarta Selatan"],
    "Bandung": ["bandung", "BDG", "Kota Bandung", " bandung "],
    "Surabaya": ["SURABAYA", "sby", "Kota Surabaya", " surabaya "],
    "Medan": ["medan", "MDN", "Kota Medan", " medan "],
    "Tangerang": ["tangerang", "TNG", "Kota Tangerang", " tangerang "],
    "Yogyakarta": ["Jogja", "DIY Yogyakarta", "yogyakarta", "JOG"],
    "Semarang": ["semarang", "SMG", "Kota Semarang", " semarang "],
}


def find_retail_source(project_root: Path | None = None) -> Path | None:
    """Mencari file referensi Online Retail jika tersedia di ruang kerja."""
    roots = [Path.cwd()]
    if project_root is not None and project_root not in roots:
        roots.append(project_root)

    candidates = []
    for r in roots:
        candidates.extend([
            r / "online_retail_II.xlsx",
            r / "Online Retail.xlsx",
        ])
    candidates.extend([
        Path("/mnt/data/online_retail_II.xlsx"),
        Path("/mnt/data/Online Retail.xlsx"),
    ])
    return next((p for p in candidates if p.exists()), None)


def generate_clean_base_datasets(
    n_transactions: int = DEFAULT_N_TRANSACTIONS,
    n_customers: int = DEFAULT_N_CUSTOMERS,
    n_clickstream: int = DEFAULT_N_CLICKSTREAM,
    seed: int = SEED,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Membuat 3 dataset dasar yang bersih dan saling terintegrasi melalui customer_id / user_id."""
    rng = np.random.default_rng(seed)

    # 1. Master Dimension: customers
    customer_ids = np.arange(100_001, 100_001 + n_customers)
    cities = np.array(STANDARD_CITIES)

    customers = pd.DataFrame({
        "customer_id": customer_ids,
        "age_group": rng.choice(
            ["18-24", "25-34", "35-44", "45-54", "55+"],
            size=n_customers,
            p=[0.22, 0.35, 0.23, 0.12, 0.08],
        ),
        "gender": rng.choice(
            ["Female", "Male", "Other"],
            size=n_customers,
            p=[0.49, 0.49, 0.02],
        ),
        "signup_date": pd.to_datetime("2019-01-01")
        + pd.to_timedelta(rng.integers(0, 2100, n_customers), unit="D"),
        "membership_tier": rng.choice(
            ["Bronze", "Silver", "Gold", "Platinum"],
            size=n_customers,
            p=[0.45, 0.30, 0.18, 0.07],
        ),
        "city": rng.choice(cities, size=n_customers, p=[0.32, 0.18, 0.16, 0.10, 0.10, 0.07, 0.07]),
    })

    # 2. Fact Table: transactions
    transaction_customer = rng.choice(customer_ids, size=n_transactions)
    product_ids = np.array([f"P{i:06d}" for i in range(1, 5001)])
    categories = np.array(["Fashion", "Home", "Beauty", "Electronics", "Sports", "Grocery"])
    payment_methods = np.array(["E-Wallet", "Credit Card", "Bank Transfer", "COD"])
    timestamps = pd.Timestamp("2023-01-01") + pd.to_timedelta(
        rng.integers(0, 365 * 24 * 60 * 60, n_transactions), unit="s"
    )

    transactions = pd.DataFrame({
        "transaction_id": [f"T{i:09d}" for i in range(1, n_transactions + 1)],
        "customer_id": transaction_customer,
        "timestamp": timestamps,
        "product_id": rng.choice(product_ids, size=n_transactions),
        "category": rng.choice(categories, size=n_transactions, p=[0.25, 0.15, 0.18, 0.17, 0.10, 0.15]),
        "quantity": rng.integers(1, 8, size=n_transactions),
        "price": np.round(rng.lognormal(mean=4.0, sigma=0.7, size=n_transactions), 2),
        "discount": rng.choice([0.0, 0.05, 0.10, 0.15, 0.20], size=n_transactions, p=[0.50, 0.20, 0.15, 0.10, 0.05]),
        "payment_method": rng.choice(payment_methods, size=n_transactions, p=[0.45, 0.25, 0.20, 0.10]),
        "city": rng.choice(cities, size=n_transactions, p=[0.32, 0.18, 0.16, 0.10, 0.10, 0.07, 0.07]),
    })
    transactions["revenue"] = (
        transactions["quantity"] * transactions["price"] * (1 - transactions["discount"])
    ).round(2)

    # 3. Semi-structured Table: clickstream (JSON Lines)
    clickstream = pd.DataFrame({
        "event_id": [f"E{i:09d}" for i in range(1, n_clickstream + 1)],
        "session_id": [f"S{v:08d}" for v in rng.integers(1, max(2, n_clickstream // 2), n_clickstream)],
        "user_id": rng.choice(customer_ids, size=n_clickstream),
        "timestamp": pd.Timestamp("2023-01-01") + pd.to_timedelta(
            rng.integers(0, 365 * 24 * 60 * 60, n_clickstream), unit="s"
        ),
        "page_url": rng.choice(
            ["/", "/products", "/cart", "/checkout", "/search", "/account"],
            size=n_clickstream,
            p=[0.25, 0.30, 0.15, 0.10, 0.12, 0.08],
        ),
        "action_event": rng.choice(
            ["page_view", "click", "add_to_cart", "purchase", "search"],
            size=n_clickstream,
            p=[0.40, 0.25, 0.15, 0.08, 0.12],
        ),
        "device_type": rng.choice(
            ["mobile", "desktop", "tablet"],
            size=n_clickstream,
            p=[0.65, 0.28, 0.07],
        ),
    })

    return transactions, customers, clickstream


def _corrupt_city_series(series: pd.Series, rng: np.random.Generator) -> pd.Series:
    """Mengubah nama kota standar menjadi variasi penulisan tidak konsisten secara acak."""
    values = series.to_numpy(dtype=object).copy()
    for i, val in enumerate(values):
        if pd.notna(val) and val in CITY_DIRTY_VARIANTS:
            options = CITY_DIRTY_VARIANTS[val]
            values[i] = options[rng.integers(0, len(options))]
    return pd.Series(values, index=series.index, dtype=object)


def inject_dirty_transactions(
    df: pd.DataFrame,
    rate: float = DEFAULT_DIRTY_RATE,
    seed: int = SEED,
) -> pd.DataFrame:
    """
    Menyuntikkan tepat `rate` (default 8%) baris kotor ke tabel transactions.
    Proporsi anomali dari total baris kotor (8%):
    - 25% Missing values (customer_id, timestamp, category)
    - 25% Inconsistent formatting pada kolom city (JKT, jakarta, DKI Jakarta, dll.)
    - 25% Invalid values / outliers (price < 0, quantity < 0)
    - 12.5% Future timestamps (timestamp di tahun 2035)
    - 12.5% Duplicate transaction_id
    """
    dirty = df.copy()
    dirty["customer_id"] = dirty["customer_id"].astype("Int64")
    rng = np.random.default_rng(seed)

    n = len(dirty)
    k = max(8, int(n * rate))
    dirty_indices = rng.choice(dirty.index.to_numpy(), size=k, replace=False)

    # Bagi indeks kotor ke 8 bucket sama rata (masing-masing 12.5% dari k = 1% dari total data)
    buckets = np.array_split(dirty_indices, 8)

    # Bucket 0 & 1 (25% dari k): Missing values pada customer_id, timestamp, category
    miss_sub = np.array_split(np.concatenate([buckets[0], buckets[1]]), 3)
    dirty.loc[miss_sub[0], "customer_id"] = pd.NA
    dirty.loc[miss_sub[1], "timestamp"] = pd.NaT
    dirty.loc[miss_sub[2], "category"] = np.nan

    # Bucket 2 & 3 (25% dari k): Inconsistent city formatting
    city_idx = np.concatenate([buckets[2], buckets[3]])
    dirty.loc[city_idx, "city"] = _corrupt_city_series(dirty.loc[city_idx, "city"], rng)

    # Bucket 4 (12.5% dari k): Negative price
    dirty.loc[buckets[4], "price"] = -dirty.loc[buckets[4], "price"].abs()

    # Bucket 5 (12.5% dari k): Negative quantity
    dirty.loc[buckets[5], "quantity"] = -dirty.loc[buckets[5], "quantity"].abs()

    # Bucket 6 (12.5% dari k): Future timestamp
    dirty.loc[buckets[6], "timestamp"] = pd.Timestamp("2035-01-01 00:00:00")

    # Bucket 7 (12.5% dari k): Duplicate transaction_id
    dup_idx = buckets[7]
    non_dirty_pool = np.setdiff1d(dirty.index.to_numpy(), dirty_indices)
    source_idx = rng.choice(non_dirty_pool, size=len(dup_idx), replace=False)
    dirty.loc[dup_idx, "transaction_id"] = dirty.loc[source_idx, "transaction_id"].to_numpy()

    return dirty


def inject_dirty_customers(
    df: pd.DataFrame,
    rate: float = DEFAULT_DIRTY_RATE,
    seed: int = SEED + 1,
) -> pd.DataFrame:
    """
    Menyuntikkan tepat `rate` (default 8%) baris kotor ke tabel customers.
    Proporsi anomali dari total baris kotor (8%):
    - 37.5% Missing values (age_group, gender, membership_tier, signup_date)
    - 37.5% Inconsistent formatting pada kolom city
    - 12.5% Future signup_date (tanggal di masa depan)
    - 12.5% Duplicate customer_id
    """
    dirty = df.copy()
    dirty["customer_id"] = dirty["customer_id"].astype("Int64")
    rng = np.random.default_rng(seed)

    n = len(dirty)
    k = max(8, int(n * rate))
    dirty_indices = rng.choice(dirty.index.to_numpy(), size=k, replace=False)
    buckets = np.array_split(dirty_indices, 8)

    # Bucket 0, 1, 2 (37.5% dari k): Missing values pada atribut profil & signup_date
    miss_sub = np.array_split(np.concatenate([buckets[0], buckets[1], buckets[2]]), 4)
    dirty.loc[miss_sub[0], "age_group"] = np.nan
    dirty.loc[miss_sub[1], "gender"] = np.nan
    dirty.loc[miss_sub[2], "membership_tier"] = np.nan
    dirty.loc[miss_sub[3], "signup_date"] = pd.NaT

    # Bucket 3, 4, 5 (37.5% dari k): Inconsistent city formatting
    city_idx = np.concatenate([buckets[3], buckets[4], buckets[5]])
    dirty.loc[city_idx, "city"] = _corrupt_city_series(dirty.loc[city_idx, "city"], rng)

    # Bucket 6 (12.5% dari k): Future signup_date
    dirty.loc[buckets[6], "signup_date"] = pd.Timestamp("2035-01-01")

    # Bucket 7 (12.5% dari k): Duplicate customer_id
    dup_idx = buckets[7]
    non_dirty_pool = np.setdiff1d(dirty.index.to_numpy(), dirty_indices)
    source_idx = rng.choice(non_dirty_pool, size=len(dup_idx), replace=False)
    dirty.loc[dup_idx, "customer_id"] = dirty.loc[source_idx, "customer_id"].to_numpy()

    return dirty


def inject_dirty_clickstream(
    df: pd.DataFrame,
    rate: float = DEFAULT_DIRTY_RATE,
    seed: int = SEED + 2,
) -> pd.DataFrame:
    """
    Menyuntikkan tepat `rate` (default 8%) baris kotor ke tabel clickstream.
    Proporsi anomali dari total baris kotor (8%):
    - 50% Missing values (user_id, timestamp, action_event, page_url)
    - 25% Inconsistent formatting pada device_type / action_event (huruf besar/spasi acak)
    - 12.5% Future timestamp
    - 12.5% Duplicate event_id
    """
    dirty = df.copy()
    dirty["user_id"] = dirty["user_id"].astype("Int64")
    rng = np.random.default_rng(seed)

    n = len(dirty)
    k = max(8, int(n * rate))
    dirty_indices = rng.choice(dirty.index.to_numpy(), size=k, replace=False)
    buckets = np.array_split(dirty_indices, 8)

    # Bucket 0, 1, 2, 3 (50% dari k): Missing values pada user_id, timestamp, action_event, page_url
    dirty.loc[buckets[0], "user_id"] = pd.NA
    dirty.loc[buckets[1], "timestamp"] = pd.NaT
    dirty.loc[buckets[2], "action_event"] = np.nan
    dirty.loc[buckets[3], "page_url"] = np.nan

    # Bucket 4 & 5 (25% dari k): Inconsistent formatting pada device_type & action_event
    dev_variants = {"mobile": "MOBILE", "desktop": " Desktop ", "tablet": "Tab"}
    act_variants = {
        "page_view": "PAGE_VIEW",
        "click": " Click ",
        "add_to_cart": "Add_To_Cart",
        "purchase": "PURCHASE",
        "search": " Search ",
    }
    dirty.loc[buckets[4], "device_type"] = dirty.loc[buckets[4], "device_type"].map(
        lambda x: dev_variants.get(x, x) if pd.notna(x) else x
    )
    dirty.loc[buckets[5], "action_event"] = dirty.loc[buckets[5], "action_event"].map(
        lambda x: act_variants.get(x, x) if pd.notna(x) else x
    )

    # Bucket 6 (12.5% dari k): Future timestamp
    dirty.loc[buckets[6], "timestamp"] = pd.Timestamp("2035-01-01 00:00:00")

    # Bucket 7 (12.5% dari k): Duplicate event_id
    dup_idx = buckets[7]
    non_dirty_pool = np.setdiff1d(dirty.index.to_numpy(), dirty_indices)
    source_idx = rng.choice(non_dirty_pool, size=len(dup_idx), replace=False)
    dirty.loc[dup_idx, "event_id"] = dirty.loc[source_idx, "event_id"].to_numpy()

    return dirty


def generate_and_save_raw_datasets(
    raw_dir: Path,
    n_transactions: int = DEFAULT_N_TRANSACTIONS,
    n_customers: int = DEFAULT_N_CUSTOMERS,
    n_clickstream: int = DEFAULT_N_CLICKSTREAM,
    dirty_rate: float = DEFAULT_DIRTY_RATE,
    seed: int = SEED,
) -> Dict[str, pd.DataFrame]:
    """Membuat dataset sintetis, menyuntikkan 8% data kotor, dan menyimpannya ke folder raw_dir."""
    raw_dir.mkdir(parents=True, exist_ok=True)

    print(
        f"[Generator] Membuat base dataset "
        f"(transactions={n_transactions:,}, customers={n_customers:,}, clickstream={n_clickstream:,})..."
    )
    transactions, customers, clickstream = generate_clean_base_datasets(
        n_transactions=n_transactions,
        n_customers=n_customers,
        n_clickstream=n_clickstream,
        seed=seed,
    )

    print(f"[Generator] Menyuntikkan {dirty_rate * 100:.1f}% data kotor (Veracity Check)...")
    transactions_raw = inject_dirty_transactions(transactions, rate=dirty_rate, seed=seed)
    customers_raw = inject_dirty_customers(customers, rate=dirty_rate, seed=seed + 1)
    clickstream_raw = inject_dirty_clickstream(clickstream, rate=dirty_rate, seed=seed + 2)

    tx_path = raw_dir / "transactions_dirty.csv"
    cust_path = raw_dir / "customers_dirty.csv"
    click_path = raw_dir / "clickstream_dirty.jsonl"

    print(f"[Generator] Menyimpan dataset kotor ke {raw_dir.resolve()} ...")
    transactions_raw.to_csv(tx_path, index=False)
    customers_raw.to_csv(cust_path, index=False)
    clickstream_raw.to_json(click_path, orient="records", lines=True, date_format="iso")

    print("[Generator] Selesai!")
    return {
        "transactions_raw": transactions_raw,
        "customers_raw": customers_raw,
        "clickstream_raw": clickstream_raw,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="E-Commerce & Retail Analytics Synthetic Data Generator")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/raw"),
        help="Folder tujuan penyimpanan dataset mentah (dirty)",
    )
    parser.add_argument("--n-transactions", type=int, default=DEFAULT_N_TRANSACTIONS)
    parser.add_argument("--n-customers", type=int, default=DEFAULT_N_CUSTOMERS)
    parser.add_argument("--n-clickstream", type=int, default=DEFAULT_N_CLICKSTREAM)
    parser.add_argument("--dirty-rate", type=float, default=DEFAULT_DIRTY_RATE)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()

    generate_and_save_raw_datasets(
        raw_dir=args.output_dir,
        n_transactions=args.n_transactions,
        n_customers=args.n_customers,
        n_clickstream=args.n_clickstream,
        dirty_rate=args.dirty_rate,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()

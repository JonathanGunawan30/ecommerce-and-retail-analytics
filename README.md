# E-Commerce & Retail Analytics — Big Data & Data Analytics Project

This repository contains the final project for the **Big Data & Data Analytics** course, focusing on **Category 1: E-Commerce & Retail Analytics**.

The project aims to design and implement a scalable data processing pipeline for e-commerce analytics by integrating structured and semi-structured datasets, performing data quality assessment and cleansing, and evaluating storage performance across multiple file formats.

---

## 🎥 Presentation Videos

- **Milestone 1 – Mid-Project Presentation:** [Watch on YouTube](https://youtu.be/VmfCSnNGyo4)

---

## 📋 Big Data Planning Canvas (Milestone 1)

| Component | Description |
| :--- | :--- |
| **1. Business Problem** | E-commerce companies experience rapid growth in daily transactions, generating millions of transaction records and hundreds of thousands of clickstream events. However, raw data collected from multiple channels often contains inconsistencies and anomalies (approximately 8% dirty data) and is stored in text-based formats such as CSV and JSON. These limitations increase computational overhead and reduce analytical processing efficiency. |
| **2. Analytical Goals** | 1. Clean, validate, and standardize three integrated data entities.<br>2. Evaluate storage efficiency and processing performance across CSV, JSONL, and Parquet formats to identify the most optimal storage architecture.<br>3. Establish a reliable and analytics-ready data foundation for Cohort Retention Analysis, RFM Customer Segmentation, and Conversion Funnel Analysis using **Apache Spark (PySpark)** in Milestone 2. |
| **3. Data Sources & Volume (5V – Volume & Variety)** | A combination of structured relational data and semi-structured user activity logs:<br>• **Fact Table (`transactions`)**: 1,150,000 raw records → more than 1,080,000 cleaned records.<br>• **Dimension Table (`customers`)**: 55,000 raw records → more than 52,000 cleaned records.<br>• **Semi-Structured Data (`clickstream`)**: 220,000 raw JSONL events → more than 208,000 cleaned events. |
| **4. Veracity Assessment (8% Dirty Data Injection)** | A controlled 8% data anomaly injection is implemented through `synthetic_generator.py` to simulate real-world data quality challenges:<br>• **Missing Values:** Null values in attributes such as `customer_id`, `user_id`, `timestamp`, and `category`.<br>• **Inconsistent Formatting:** Variations in city names (e.g., `Jakarta`, `JKT`, `jakarta`, `DKI Jakarta`, `BDG`, `Kota Bandung`, `SURABAYA`, and `sby`), as well as inconsistent capitalization and whitespace in string attributes.<br>• **Outliers & Invalid Values:** Negative prices (`price < 0`), negative quantities (`quantity < 0`), and invalid future dates (e.g., `2035-01-01`).<br>• **Duplicate Records:** Duplicate primary key values across `transaction_id`, `customer_id`, and `event_id`. |
| **5. Velocity & Storage Architecture** | Cleaned datasets are converted into the columnar **Apache Parquet** format. Benchmark results are used to evaluate storage size, read performance (I/O), and aggregation execution speed against CSV and JSONL formats. Parquet is expected to provide superior storage efficiency and analytical query performance. |
| **6. Value & Expected Business Impact** | Improve large-scale aggregation performance across millions of records, ensure the accuracy and reliability of revenue reporting, and provide a high-quality data foundation for customer segmentation, targeted marketing campaigns, and customer retention strategies. |

---

## 🗂️ Integrated Dataset Schema (3 Entities)

### 1. Fact Table: `transactions.csv` (> 1,000,000 Clean Records)

| Column | Data Type | Description |
| :--- | :--- | :--- |
| `transaction_id` | `string` (PK) | Unique transaction identifier (e.g., `T000000001`). |
| `customer_id` | `int64` (FK) | Customer identifier referencing the `customers` table. |
| `timestamp` | `datetime64` | Date and time when the transaction occurred. |
| `product_id` | `string` | Product identifier (`P000001` – `P005000`). |
| `category` | `string` | Product category (`Fashion`, `Home`, `Beauty`, `Electronics`, `Sports`, `Grocery`). |
| `quantity` | `int64` | Number of items purchased (`> 0`). |
| `price` | `float64` | Unit price of the product (`>= 0`). |
| `discount` | `float64` | Discount percentage (`0.00` – `0.20`). |
| `payment_method` | `string` | Payment method (`E-Wallet`, `Credit Card`, `Bank Transfer`, `COD`). |
| `city` | `string` | Standardized transaction city (`Jakarta`, `Bandung`, `Surabaya`, `Medan`, `Tangerang`, `Yogyakarta`, `Semarang`). |
| `revenue` | `float64` | Net transaction value calculated as `quantity * price * (1 - discount)`. |

### 2. Dimension Table: `customers.csv` (> 50,000 Clean Records)

| Column | Data Type | Description |
| :--- | :--- | :--- |
| `customer_id` | `int64` (PK) | Unique customer identifier (e.g., `100001`). |
| `age_group` | `string` | Customer age group (`18-24`, `25-34`, `35-44`, `45-54`, `55+`). |
| `gender` | `string` | Customer gender (`Female`, `Male`, `Other`). |
| `signup_date` | `datetime64` | Date when the customer registered for an account. |
| `membership_tier` | `string` | Customer membership level (`Bronze`, `Silver`, `Gold`, `Platinum`). |
| `city` | `string` | Customer's registered city of residence. |

### 3. Semi-Structured Table: `clickstream.jsonl` (> 200,000 Clean Events)

| Column | Data Type | Description |
| :--- | :--- | :--- |
| `event_id` | `string` (PK) | Unique event identifier (e.g., `E000000001`). |
| `session_id` | `string` | Unique identifier for a user browsing session. |
| `user_id` | `int64` (FK) | User identifier referencing `customers.customer_id`. |
| `timestamp` | `datetime64` | Timestamp indicating when the event occurred. |
| `page_url` | `string` | Website page accessed (`/`, `/products`, `/cart`, `/checkout`, `/search`, `/account`). |
| `action_event` | `string` | User interaction type (`page_view`, `click`, `add_to_cart`, `purchase`, `search`). |
| `device_type` | `string` | Device used to access the platform (`mobile`, `desktop`, `tablet`). |

---

## 📁 Project Directory Structure

```text
ecommerce-retail-analytics/
├── data_generator/
│   ├── __init__.py
│   └── synthetic_generator.py
│       # Synthetic data generator with 8% dirty data injection
│
├── notebooks/
│   └── 01_cleansing_and_storage_benchmark.ipynb
│       # Data quality assessment, cleansing, and storage benchmarking
│
├── data/
│   ├── raw/
│   │   # Raw datasets containing approximately 8% injected anomalies
│   │   # (*.csv, *.jsonl, *.zip)
│   │
│   ├── clean/
│   │   # Cleansed datasets (*.csv, *.jsonl, *.parquet, *.zip)
│   │
│   └── benchmark/
│       # Benchmark datasets, performance results, and visualizations
│       # (*.parquet, *.zip)
│
├── scripts/
│   └── unpack_data.py
│       # Utility script for automatically extracting compressed datasets
│
└── README.md
```

> [!NOTE]
> **Dataset Documentation & Evidence (Over 1 Million Records / GitHub 100 MB File Limit)**
>
> All synthetically generated datasets are included in this repository as project documentation and supporting evidence.
>
> To comply with GitHub's individual file size limit of less than 100 MB, large datasets containing over 1,000,000 records or exceeding 100 MB are compressed into ZIP archives:
>
> | Dataset | Original Size | Compressed Size |
> | :--- | ---: | ---: |
> | `data/raw/transactions_dirty.csv` | ~106 MB | ~29.5 MB |
> | `data/clean/transactions.csv` | ~100.8 MB | ~27.9 MB |
> | `data/benchmark/transactions.csv` | ~100.8 MB | ~27.9 MB |
> | `data/benchmark/transactions.jsonl` | ~262 MB | ~33.9 MB |
>
> Parquet files (`*.parquet`) and small-to-medium-sized datasets are tracked directly in the repository without ZIP compression.

---

## 🚀 Getting Started (Milestone 1)

### 1. Install Dependencies

Install the required Python libraries using pip:

```bash
pip install pandas numpy pyarrow matplotlib openpyxl jupyter
```

### 2. Extract Compressed Datasets (.zip)

To extract all compressed datasets included in the repository, execute:

```bash
python scripts/unpack_data.py
```

This script automatically extracts the available ZIP archives into their respective directories.

### 3. Generate Synthetic Datasets (Optional)

To regenerate all datasets from scratch, including the controlled injection of 8% data anomalies, execute:

```bash
python data_generator/synthetic_generator.py
```

This step is optional if the pre-generated datasets are already available in the repository.

### 4. Run the Data Cleansing & Storage Benchmark Notebook

Open the following Jupyter Notebook:

```text
notebooks/01_cleansing_and_storage_benchmark.ipynb
```

Execute all cells sequentially using **Run All**.

> **Note:** The notebook can also invoke the synthetic data generator automatically, allowing the entire data generation, cleansing, and storage benchmarking workflow to be executed end-to-end in a single run.

---

## 📌 Project Scope

This project is divided into two milestones:

**Milestone 1 – Data Engineering & Storage Benchmarking**
- Synthetic dataset generation.
- Data quality assessment and anomaly detection.
- Data cleansing and standardization.
- Storage format comparison (CSV, JSONL, and Parquet).
- Storage and I/O performance benchmarking.

**Milestone 2 – Big Data Analytics**
- Large-scale data processing using Apache Spark (PySpark).
- Cohort Retention Analysis.
- RFM Customer Segmentation.
- Conversion Funnel Analysis.
- Business insights and data-driven recommendations.

---

**Course:** Big Data & Data Analytics  
**Project Category:** E-Commerce & Retail Analytics  
**Project Type:** Academic Final Project  
**Primary Technologies:** Python, Pandas, NumPy, Apache Parquet, PyArrow, Jupyter Notebook, and Apache Spark (PySpark).

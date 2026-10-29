# E-Commerce & Retail Analytics — Big Data & Data Analytics Project

Repositori ini merupakan proyek akhir mata kuliah **Big Data & Data Analytics** dengan studi kasus **Kategori 1: E-Commerce & Retail Analytics**.

---

## 🎥 Tautan Video Presentasi
- **Video Milestone 1 (Mid Project)**: `[Masukkan Tautan YouTube Unlisted / Google Drive di sini]`
- **Video Milestone 2 (End Project)**: `[Akan ditambahkan pada Milestone 2]`

---

## 📋 Big Data Planning Canvas (Milestone 1)

| Komponen | Deskripsi |
| :--- | :--- |
| **1. Business Problem** | Perusahaan *e-commerce* mengalami pertumbuhan transaksi harian yang pesat (jutaan transaksi & ratusan ribu *event clickstream*), namun data mentah dari berbagai kanal masih mengandung anomali (~8% *dirty data*) serta disimpan dalam format teks mentah (CSV/JSON) yang membebani waktu komputasi analitik. |
| **2. Analytical Goals** | 1. Membersihkan dan menstandarisasi 3 entitas data yang saling terintegrasi.<br>2. Menguji efisiensi format penyimpanan (*CSV vs JSONL vs Parquet*) untuk menemukan arsitektur penyimpanan paling optimal.<br>3. Menyiapkan pondasi data bersih untuk *Cohort Retention Analysis*, *RFM Customer Segmentation*, dan *Conversion Funnel Analysis* menggunakan **Apache Spark (PySpark)** pada Milestone 2. |
| **3. Data Sources & Volume (5V - Volume & Variety)** | Kombinasi data relasional (*structured*) dan log aktivitas pengguna (*semi-structured*):<br>• **Fact Table (`transactions`)**: `1.150.000` baris mentah $\rightarrow$ `> 1.080.000` baris bersih.<br>• **Dimension Table (`customers`)**: `55.000` baris mentah $\rightarrow$ `> 52.000` baris bersih.<br>• **Semi-Structured (`clickstream`)**: `220.000` event JSONL mentah $\rightarrow$ `> 208.000` event bersih. |
| **4. Veracity Check (8% Dirty Data Injection)** | Disuntikkan **8%** anomali secara terukur melalui `synthetic_generator.py`:<br>• **Missing Values**: Nilai `null` pada `customer_id`, `user_id`, `timestamp`, `category`, dll.<br>• **Inconsistent Formatting**: Variasi penulisan kota (`Jakarta`, `JKT`, `jakarta`, `DKI Jakarta`, `BDG`, `Kota Bandung`, `SURABAYA`, `sby`, dll.) serta variasi huruf besar/spasi pada atribut string.<br>• **Outliers & Invalid Values**: Harga negatif (`price < 0`), kuantitas negatif (`quantity < 0`), dan tanggal masa depan (`2035-01-01`).<br>• **Duplicate Records**: Duplikasi pada *primary key* (`transaction_id`, `customer_id`, `event_id`). |
| **5. Velocity & Storage Architecture** | Data mentah yang telah dibersihkan dikonversi ke format kolumnar **Apache Parquet** yang terbukti jauh lebih hemat ruang penyimpanan dan memiliki kecepatan baca (*I/O read*) serta agregasi paling cepat dibandingkan CSV dan JSONL. |
| **6. Value & Expected Business Impact** | Mempercepat eksekusi kueri agregasi skala jutaan baris, menjamin akurasi pelaporan pendapatan (*revenue*), serta menghasilkan segmentasi pelanggan yang akurat untuk strategi promosi dan retensi pelanggan. |

---

## 🗂️ Skema 3 Entitas Dataset Terintegrasi

### 1. Tabel Fakta: `transactions.csv` (> 1.000.000 Baris Bersih)
| Kolom | Tipe Data | Deskripsi |
| :--- | :--- | :--- |
| `transaction_id` | `string` (PK) | ID unik transaksi (`T000000001`, dst.) |
| `customer_id` | `int64` (FK) | ID pelanggan yang berelasi ke tabel `customers` |
| `timestamp` | `datetime64` | Waktu terjadinya transaksi |
| `product_id` | `string` | Kode produk (`P000001` – `P005000`) |
| `category` | `string` | Kategori produk (`Fashion`, `Home`, `Beauty`, `Electronics`, `Sports`, `Grocery`) |
| `quantity` | `int64` | Jumlah barang yang dibeli (`> 0`) |
| `price` | `float64` | Harga satuan produk (`>= 0`) |
| `discount` | `float64` | Persentase diskon (`0.00` – `0.20`) |
| `payment_method` | `string` | Metode pembayaran (`E-Wallet`, `Credit Card`, `Bank Transfer`, `COD`) |
| `city` | `string` | Kota transaksi terstandarisasi (`Jakarta`, `Bandung`, `Surabaya`, `Medan`, `Tangerang`, `Yogyakarta`, `Semarang`) |
| `revenue` | `float64` | Total nilai transaksi bersih (`quantity * price * (1 - discount)`) |

### 2. Tabel Dimensi: `customers.csv` (> 50.000 Baris Bersih)
| Kolom | Tipe Data | Deskripsi |
| :--- | :--- | :--- |
| `customer_id` | `int64` (PK) | ID unik pelanggan (`100001`, dst.) |
| `age_group` | `string` | Kelompok usia (`18-24`, `25-34`, `35-44`, `45-54`, `55+`) |
| `gender` | `string` | Jenis kelamin (`Female`, `Male`, `Other`) |
| `signup_date` | `datetime64` | Tanggal pendaftaran akun pelanggan |
| `membership_tier` | `string` | Tingkat keanggotaan (`Bronze`, `Silver`, `Gold`, `Platinum`) |
| `city` | `string` | Kota domisili pelanggan |

### 3. Tabel Semi-Structured: `clickstream.jsonl` (> 200.000 Event Bersih)
| Kolom | Tipe Data | Deskripsi |
| :--- | :--- | :--- |
| `event_id` | `string` (PK) | ID unik event aktivitas (`E000000001`, dst.) |
| `session_id` | `string` | ID sesi kunjungan pengguna |
| `user_id` | `int64` (FK) | ID pengguna yang berelasi ke `customers.customer_id` |
| `timestamp` | `datetime64` | Waktu terjadinya event |
| `page_url` | `string` | Halaman yang diakses (`/`, `/products`, `/cart`, `/checkout`, `/search`, `/account`) |
| `action_event` | `string` | Jenis interaksi (`page_view`, `click`, `add_to_cart`, `purchase`, `search`) |
| `device_type` | `string` | Perangkat yang digunakan (`mobile`, `desktop`, `tablet`) |

---

## 📁 Struktur Direktori Proyek

```text
ecommerce-retail-analytics/
├── data_generator/
│   ├── __init__.py
│   └── synthetic_generator.py                  # Script pembuat data sintetis + injeksi 8% data kotor
├── notebooks/
│   └── 01_cleansing_and_storage_benchmark.ipynb # Notebook audit, data cleansing, dan benchmark format file
├── data/                                        # Dibuat otomatis saat generator/notebook dijalankan
│   ├── raw/                                     # Dataset mentah dengan 8% anomali
│   ├── clean/                                   # Dataset bersih (CSV, JSONL, dan Parquet)
│   └── benchmark/                               # File pengujian dan grafik benchmark
├── requirements/
│   └── requirements.md                          # Spesifikasi proyek akhir
└── README.md
```

---

## 🚀 Cara Menjalankan (Milestone 1)

### 1. Instalasi Dependensi
```bash
pip install pandas numpy pyarrow matplotlib openpyxl jupyter
```

### 2. Menjalankan Generator Data Sintetis (Opsional / Mandiri via CLI)
```bash
python data_generator/synthetic_generator.py
```

### 3. Menjalankan Notebook Cleansing & Storage Benchmark
Buka dan jalankan seluruh sel secara berurutan pada:
```text
notebooks/01_cleansing_and_storage_benchmark.ipynb
```
*(Catatan: Notebook juga dapat langsung memanggil fungsi generator secara otomatis sehingga dapat dieksekusi end-to-end dalam satu kali klik **Run All**).*

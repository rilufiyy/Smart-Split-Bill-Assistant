# Smart-Split-Bill-Assistant
SmartSplit Bill AI is a web-based prototype application built using Streamlit that helps users extract transaction data from shopping receipts and split bills fairly among multiple participants. The application leverages AI-based receipt understanding models to read receipt images and automatically structure purchase information.
---

## Fitur Utama

*  Upload gambar struk / bill belanja
*  Ekstraksi otomatis data transaksi menggunakan AI
  * Nama item
  * Jumlah
  * Harga per item
  * Total harga item
  * Subtotal
  * Pajak / service / biaya tambahan
  * Total bill
*  Input nama peserta bill
*  Assign item ke masing-masing peserta
*  Perhitungan otomatis total yang harus dibayar per orang
* Validasi: total pembayaran semua orang = total bill

---

## Arsitektur Project

```
SmartSplit Bill AI
├── app.py                 # Entry point Streamlit app
├── main.py                # Main application runner / orchestration
├── modules
│   ├── data               # Data schema & state management
│   │   ├── assignment_data.py
│   │   ├── receipt_data.py
│   │   ├── report_data.py
│   │   └── session_data.py
│   ├── models             # AI & document understanding models
│   │   ├── donut.py       # Donut document understanding model
│   │   ├── layoutlmv3.py  # LayoutLMv3 model
│   │   ├── gemini.py      # Gemini API integration
│   │   └── loader.py      # Model loader & abstraction
│   ├── views              # Streamlit UI pages
│   │   ├── view_1_receipt_upload.py
│   │   ├── view_2_assign_participants.py
│   │   ├── view_3_report.py
│   │   └── view_setting.py
│   ├── controller.py      # App flow controller
│   ├── styles.py          # Custom UI styles
│   └── utils.py           # Helper utilities
├── dockerfile
├── docker-compose.yml
├── pyproject.toml
├── requirements.txt
├── uv.lock
├── .env.example
└── README.md
```

---

## Model AI yang Digunakan

### Model yang Dieksplorasi

1. **Donut (Document Understanding Transformer)**

   * OCR-free
   * End-to-end document parsing
   * Kuat untuk struktur semi-formal seperti struk

2. **LayoutLMv3**

   * Multimodal (text + layout + vision)
   * Akurasi tinggi, namun inference relatif lebih lambat

3. **Gemini (API-based LLM)**

   * Parsing berbasis vision-language model
   * Sangat fleksibel untuk reasoning & data cleaning

---

## Contoh Hasil Ekstraksi Bill

**Input:**

* Gambar struk restoran / minimarket

**Output (contoh):**
<img width="802" height="671" alt="Screenshot 2026-01-30 171356" src="https://github.com/user-attachments/assets/fb97d3e8-afd2-4bd2-9ff3-7be63a2f5263" />

---

## Contoh Split Bill
<img width="805" height="1032" alt="Screenshot (60)" src="https://github.com/user-attachments/assets/90855894-8589-4d5f-af64-77dfeaa69268" />

---

## Evaluasi & Analisis

### 1. Evaluasi Model AI

**Kelebihan:**

* Parsing semantik kuat
* Tidak bergantung OCR tradisional
* Robust terhadap noise ringan

**Kelemahan:**

* Ketergantungan API
* Biaya inference
* Kadang perlu normalisasi manual

**Ide Improvement:**

* Hybrid: Donut (local) + LLM validation
* Fine-tuning Donut dengan dataset struk lokal
* Confidence score per field

### 2. Evaluasi Produk Web

**Kelebihan:**

* Flow sederhana & intuitif
* Modular & scalable
* Mudah dikembangkan

**Kelemahan:**

* Belum ada auth user
* Error handling masih basic

**Ide Improvement:**

* User login & history bill
* Export PDF / CSV
* Multi-currency support

---

## Cara Menjalankan Project

###  Clone Repository

```bash
git clone https://github.com/rilufiyy/Smart-Split-Bill-Assistant.git
cd Smart-Split-Bill-Assistant
```

###  Setup Environment

```bash
cp .env.example .env
```

Isi API key (contoh: Gemini).

###  Install Dependency (Local)

```bash
pip install -r requirements.txt
```

atau menggunakan **uv**:

```bash
uv sync
```

### Run Aplikasi

```bash
streamlit run app.py
```

---

## Menjalankan dengan Docker

```bash
docker-compose up --build
```

Akses aplikasi di:

```
http://localhost:8501
```

---

## Tech Stack

* Python
* Streamlit
* Hugging Face Transformers
* Gemini API
* Docker & Docker Compose

---

## Author

**Sri Lutfiya Dwiyeni**
Machine Learning & AI Engineer

---

## License

This project is for educational and portfolio purposes.

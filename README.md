# Medical Telegram Warehouse 🏥📊

An end-to-end data engineering pipeline that scrapes medical supply data from Telegram, enriches images using **YOLOv8** object detection, and stores the structured results in a **PostgreSQL** star schema. The data is served via a **FastAPI** analytical layer and orchestrated by **Dagster**.

---

## 🚀 Features

- **Data Ingestion:** Automated scraping of Telegram channels using Telethon  
- **AI Enrichment:** Object detection (YOLOv8) to categorize medical supplies in images  
- **Data Modeling:** dbt-powered star schema (Facts & Dimensions) in PostgreSQL  
- **Orchestration:** Fully observable pipeline managed by Dagster  
- **API:** Analytical REST endpoints for top products, channel activity, and keyword search  

---

## 🛠️ Tech Stack

- **Language:** Python 3.8+  
- **Database:** PostgreSQL  
- **Transformation:** dbt  
- **AI/ML:** Ultralytics YOLOv8  
- **Orchestration:** Dagster  
- **API:** FastAPI & Uvicorn  

---

## 📋 Prerequisites

- Python 3.8 or higher  
- PostgreSQL installed and running  
- Telegram API credentials (`api_id` and `api_hash` from [my.telegram.org](https://my.telegram.org))  

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
  git clone https://github.com/yourusername/medical-telegram-warehouse.git
  cd medical-telegram-warehouse
```

### 2. Create Environment Variables
Create a .env file in the root directory and add the following values:
```bash
  TG_API_ID=your_id
  TG_API_HASH=your_hash
  DB_HOST=localhost
  DB_USER=postgres
  DB_PASSWORD=yourpassword
  DB_NAME=medical_warehouse
  DB_PORT=5432
```

### 3. Install Dependencies
Create and activate a virtual environment, then install dependencies:
```bash
  python -m venv .venv
  
  # Windows
  .venv\Scripts\activate
  
  # Linux / Mac
  source .venv/bin/activate

  pip install -r requirements.txt
```

🏃 Running the Project
1. Start the Pipeline (Dagster)
This orchestrates the scraper, YOLO detection, and dbt transformations.

```
  dagster dev -f dagster_pipeline.py -p 3007
```
Access the Dagster UI at:
👉 http://localhost:3007

2. Launch the API
```
uvicorn api.main:app --reload
```
Access Swagger documentation at:
👉 http://127.0.0.1:8000/docs

🧪 Testing
Run dbt data quality tests to verify warehouse integrity:
```
  cd medical_warehouse
  dbt test --select assert_positive_views
```

# 🚦 ETL Toll Data Pipeline using Apache Airflow

This is an ETL (Extract, Transform, Load) pipeline built using **Apache Airflow** and **Python**. It processes toll data from multiple file formats and transforms it into a single consolidated CSV file. This project demonstrates task orchestration, file handling, and basic data transformation using Airflow and Pandas.

---

## 🧩 Project Overview

The ETL pipeline performs the following steps:

1. **Download** a `.tgz` archive containing toll data.
2. **Extract** the archive into a local staging folder.
3. **Process** and extract data from:
   - `vehicle-data.csv`
   - `tollplaza-data.tsv`
   - `payment-data.txt` (fixed-width format)
4. **Consolidate** data into a single DataFrame.
5. **Transform** vehicle types to uppercase and save the final result as `transformed_data.csv`.

All tasks are managed using Airflow’s modern `@dag` and `@task` decorators, and the data is handled using `pandas`.

---

## 📁 Directory Structure

project-root/
│
├── dags/
│ ├── etl_toll_pipeline.py # Main Airflow DAG
│ └── staging/ # Staging folder for all data files
│ ├── vehicle-data.csv
│ ├── tollplaza-data.tsv
│ ├── payment-data.txt
│ ├── csv_data.csv
│ ├── tsv_data.csv
│ ├── fixed_width_data.csv
│ ├── extracted_data.csv
│ └── transformed_data.csv
├── requirements.txt
└── README.md


---

## 🚀 Setup Instructions

### 1. Install Apache Airflow

Follow the official [Airflow Installation Guide](https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html)

Example using `pip`:

```bash
pip install apache-airflow==2.9.1 \
  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.1/constraints-3.8.txt"

Clone This Repository
git clone https://github.com/your-username/etl-toll-data-airflow.git
cd etl-toll-data-airflow

Copy DAG to Airflow
# Linux/Mac
cp dags/etl_toll_pipeline.py ~/airflow/dags/

# Windows (default Airflow Home for Astronomer or custom setups)
copy dags\etl_toll_pipeline.py C:\airflow-astro\dags\

Start Airflow
airflow db init
airflow scheduler
airflow webserver --port 8080

Open Airflow UI at: http://localhost:8080
Enable the DAG named ETL_toll_data.

Trigger the DAG
Trigger the DAG manually from the UI or wait for its daily schedule.

📦 Dependencies
Install required Python libraries using:
pip install -r requirements.txt

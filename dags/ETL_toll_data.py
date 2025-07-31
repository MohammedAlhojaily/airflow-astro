from airflow.decorators import dag, task
from datetime import datetime, timedelta
import os
import requests
import tarfile
import pandas as pd

# Constants
BASE_PATH = os.path.join(os.getenv("AIRFLOW_HOME", "C:\\airflow-astro"), "dags")
STAGING_PATH = os.path.join(BASE_PATH, "staging")

os.makedirs(STAGING_PATH, exist_ok=True)

CSV_FILE = os.path.join(STAGING_PATH, "vehicle-data.csv")
TSV_FILE = os.path.join(STAGING_PATH, "tollplaza-data.tsv")
FW_FILE = os.path.join(STAGING_PATH, "payment-data.txt")

@dag(
    dag_id='ETL_toll_data',
    start_date=datetime(2025, 1, 1),
    schedule='@daily',           # ✅ use `schedule` instead of `schedule_interval`
    catchup=False,
    default_args={
        'owner': 'Mohammed',
        'email': 'test@gmail.com',
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
        'email_on_failure': False,
    },
    tags=['ETL', 'Project', 'Python']
)
def etl_toll_pipeline():

    @task
    def download_dataset():
        url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Final%20Assignment/tolldata.tgz"
        dest_path = os.path.join(STAGING_PATH, "tolldata.tgz")
        response = requests.get(url)
        with open(dest_path, 'wb') as f:
            f.write(response.content)

    @task
    def untar_dataset():
        tar_path = os.path.join(STAGING_PATH, "tolldata.tgz")
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall(path=STAGING_PATH)

    @task
    def extract_csv():
        column_names = ['Rowid', 'Timestamp', 'Anonymized Vehicle number', 'Vehicle type', 'Number of axles', 'Vehicle code']
        df = pd.read_csv(CSV_FILE, header=None, names=column_names)
        df[['Rowid', 'Timestamp', 'Anonymized Vehicle number', 'Vehicle type']].to_csv(os.path.join(STAGING_PATH, "csv_data.csv"), index=False)

    @task
    def extract_tsv():
        column_names = ['Rowid', 'Timestamp', 'Anonymized Vehicle number', 'Vehicle type', 'Number of axles', 'Tollplaza id', 'Tollplaza code']
        df = pd.read_csv(TSV_FILE, sep='\t', header=None, names=column_names)
        df[['Number of axles', 'Tollplaza id', 'Tollplaza code']].to_csv(os.path.join(STAGING_PATH, "tsv_data.csv"), index=False)

    @task
    def extract_fixed_width():
        colspecs = [(0, 18), (18, 38)]
        names = ['Type of Payment code', 'Vehicle Code']
        df = pd.read_fwf(FW_FILE, colspecs=colspecs, names=names)
        df.to_csv(os.path.join(STAGING_PATH, "fixed_width_data.csv"), index=False)

    @task
    def consolidate():
        df1 = pd.read_csv(os.path.join(STAGING_PATH, "csv_data.csv"))
        df2 = pd.read_csv(os.path.join(STAGING_PATH, "tsv_data.csv"))
        df3 = pd.read_csv(os.path.join(STAGING_PATH, "fixed_width_data.csv"))
        pd.concat([df1, df2, df3], axis=1).to_csv(os.path.join(STAGING_PATH, "extracted_data.csv"), index=False)

    @task
    def transform():
        df = pd.read_csv(os.path.join(STAGING_PATH, "extracted_data.csv"))
        df['Vehicle type'] = df['Vehicle type'].str.upper()
        df.to_csv(os.path.join(STAGING_PATH, "transformed_data.csv"), index=False)

    # Task chaining
    download_dataset() >> untar_dataset() >> extract_csv() >> extract_tsv() >> extract_fixed_width() >> consolidate() >> transform()

etl_toll_pipeline = etl_toll_pipeline()

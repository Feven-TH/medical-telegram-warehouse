import sys
import os
import subprocess
from dagster import op, job, In, Definitions, ScheduleDefinition

# Get the absolute path to your project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@op
def scrape_telegram_data():
    """Runs the scraper using the EXACT python from your .venv."""
    script_path = os.path.join(BASE_DIR, "src", "scraper.py")
    
    # sys.executable is the path to the python.exe inside your .venv
    # This guarantees it finds Telethon
    subprocess.run(
        [sys.executable, script_path], 
        check=True, 
        env=os.environ.copy()
    )
    return "Scraping Complete"

@op(ins={"start": In(str)})
def run_yolo_enrichment(start):
    """Runs YOLO using the .venv python."""
    script_path = os.path.join(BASE_DIR, "scripts", "yolo_detect.py")
    subprocess.run(
        [sys.executable, script_path], 
        check=True, 
        env=os.environ.copy()
    )
    return "YOLO Complete"

@op(ins={"start": In(str)})
def run_dbt_transformations(start):
    """Runs dbt transformations."""
    # dbt is usually an executable in your .venv Scripts folder
    subprocess.run(["dbt", "run"], check=True, cwd=BASE_DIR, env=os.environ.copy())
    return "dbt Complete"

@job
def medical_warehouse_pipeline():
    scraped = scrape_telegram_data()
    yolo_done = run_yolo_enrichment(scraped)
    run_dbt_transformations(yolo_done)

defs = Definitions(
    jobs=[medical_warehouse_pipeline],
    schedules=[ScheduleDefinition(job=medical_warehouse_pipeline, cron_schedule="0 0 * * *")]
)
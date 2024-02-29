from flask import Flask, render_template, jsonify
from flask_apscheduler import APScheduler
from apscheduler.triggers.cron import CronTrigger
import threading
from utils import check_database_status, download_and_insert_csv, build_endpoint_data,delete_and_remove_non_existent_companies

app = Flask(__name__)

sched = APScheduler()


@app.route("/")
def home():
    return (
        jsonify(
            {
                "status": "UP",
                "api_endpoints": [
                    build_endpoint_data(
                        name="home", path="/", description="", method="GET"
                    ),
                    build_endpoint_data(
                        name="health", path="/health", description="", method="GET"
                    ),
                    build_endpoint_data(
                    name="insert", path="/insert", description="", method="GET"
                    ),
                    build_endpoint_data(
                        name="manually trigger crawler",
                        path="/manual-trigger",
                        description="",
                        method="GET",
                    ),
                ],
            }
        ),
        200,
    )


@app.route("/health")
def health():
    return (
        jsonify(
            {
                "status": "UP",
                "database": True if check_database_status() is True else False,
            }
        ),
        200,
    )


@app.route("/manual-trigger")
def manual_trigger():
    return render_template("index.html")


@app.route("/insert", methods=["GET"])
def insert_from_csv():
    csv_url = "https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers"
    save_path = "./data/downloaded_file.csv"

    # Create a new thread for CSV download and data insertion
    download_insert_thread = threading.Thread(
        target=download_and_insert_csv, args=(csv_url, save_path)
    )
    download_insert_thread.start()

    return (
        jsonify(
            {"message": "New Items are being uploaded, this might take about an hour"}
        ),
        201,
    )
@app.route("/delete", methods=["GET"])
def delete_from_csv():
    csv_url = "https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers"
    save_path = "./data/downloaded_file.csv"

    # Create a new thread for CSV download and data insertion
    start_delete_thread = threading.Thread(
        target=delete_and_remove_non_existent_companies, args=(csv_url, save_path)
    )
    start_delete_thread.start()

    return (
        jsonify(
            {"message": "Old Items are being purge, this might take about an hour"}
        ),
        201,
    )


if __name__ == "__main__":
    # Specify the trigger to run every day at 12
    trigger = CronTrigger(hour=12)

    # Add the job with the specified trigger
    sched.add_job(
        id="insert_from_csv",
        func=insert_from_csv,
        trigger=trigger,
        replace_existing=True,
    )

    # Start the scheduler
    sched.start()
    app.run(debug=True, host="0.0.0.0", port=5000)

from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup
import csv
from pymongo import MongoClient
import cloudinary
import cloudinary.api
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()


cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_NAME"),
    api_key=os.environ.get("CLOUDINARY_KEY"),
    api_secret=os.environ.get("CLOUDINARY_SECRET"),
    secure=True,
)

# MongoDB client initialization
user = os.getenv('MONGO_USER')
pwd = os.getenv('MONGO_PASSWORD')
url = os.getenv('MONGO_URL')

mongo_client = MongoClient(f'mongodb+srv://{user}:{pwd}@{url}/?retryWrites=true&w=majority')

db_name = "csv_data"
collection_name = "companies"
db = mongo_client[db_name]
collection = db[collection_name]


def download_and_insert_csv(url, save_path):
    try:
        # Fetch HTML content from the specified URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse HTML content using BeautifulSoup
        html_content = BeautifulSoup(response.text, "html.parser")

        # Extract the CSV link from the HTML
        csv_link = html_content.find("a", class_="gem-c-attachment__link")["href"]
        print(f"CSV link: {csv_link}")

        # Download the CSV file
        csv_response = requests.get(csv_link)
        csv_response.raise_for_status()
        print(f"CSV downloaded successfully from: {csv_link}")

        # Save the CSV content to a local file
        with open(save_path, "wb") as file:
            file.write(csv_response.content)
        print(f"CSV saved locally at: {save_path}")

        # Cloudinary upload logic
        cloudinary_upload_result = cloudinary.uploader.upload(
            save_path,
            resource_type="raw",
            public_id=f"downloaded_file-{datetime.now()}.csv",
            folder="zeninzone/uksponsorshipjobs",
        )
        print(f"Cloudinary upload result: {cloudinary_upload_result}")

        # Insert CSV data into MongoDB
        with open(save_path, "r") as data:
            reader = csv.DictReader(data)
            for idx, row in enumerate(reader):
                if idx != 0:
                    # Exclude None keys and convert them to strings
                    document = {
                        str(key): value for key, value in row.items() if key is not None
                    }
                    document_exists = collection.find_one(document)
                    if document_exists:
                        print("This row exists in the database")
                    else:
                        print("This row does not exist in the database")
                        collection.insert_one(document)

        print("Data insertion complete")


    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Connection Error: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")

def delete_and_remove_non_existent_companies(url, save_path):
    try:
        # Fetch HTML content from the specified URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse HTML content using BeautifulSoup
        html_content = BeautifulSoup(response.text, "html.parser")

        # Extract the CSV link from the HTML
        csv_link = html_content.find("a", class_="gem-c-attachment__link")["href"]
        print(f"CSV link: {csv_link}")

        # Download the CSV file
        csv_response = requests.get(csv_link)
        csv_response.raise_for_status()
        print(f"CSV downloaded successfully from: {csv_link}")

        # Save the CSV content to a local file
        with open(save_path, "wb") as file:
            file.write(csv_response.content)
        print(f"CSV saved locally at: {save_path}")

        # Read CSV data
        csv_data = set()
        with open(save_path, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                csv_data.add(tuple(row.items()))

        # Get all documents from MongoDB
        mongo_documents = collection.find({})

        # Remove MongoDB documents not present in CSV
        for mongo_doc in mongo_documents:
            if tuple(mongo_doc.items()) not in csv_data:
                print(f"Removing data from MongoDB: {mongo_doc}")
                collection.delete_one(mongo_doc)

        print("Data removal complete")


    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Connection Error: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")

def insert_data_from_csv(csv_path):
    with open(csv_path, "r") as downloaded_file:
        reader = csv.DictReader(downloaded_file)
        for row in reader:
            # Exclude None keys and convert them to strings
            document = {
                str(key): value for key, value in row.items() if key is not None
            }
            document_exists = collection.find_one(document)
            if document_exists:
                print("This row exists in the database")
            else:
                print("This row does not exist in the database")
                collection.insert_one(document)

    print("Data insertion complete")


def check_database_status():
    return True

def build_endpoint_data(name="None", path="", description="", method="") -> dict:
    description = f"endpoint for {name}" if description == "" else description
    return {name: path, "description": description, "method": method}

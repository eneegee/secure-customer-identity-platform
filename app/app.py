import os

from flask import Flask, jsonify
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "application": "NexaFlow Identity Demo",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/data")
def read_blob():
    storage_account_name = os.environ["STORAGE_ACCOUNT_NAME"]
    container_name = os.environ["CONTAINER_NAME"]
    blob_name = os.environ["BLOB_NAME"]

    account_url = (
        f"https://{storage_account_name}.blob.core.windows.net"
    )

    # DefaultAzureCredential will use the managed identity
    # when the application is running in Azure.
    credential = DefaultAzureCredential()

    blob_service_client = BlobServiceClient(
        account_url=account_url,
        credential=credential
    )

    blob_client = blob_service_client.get_blob_client(
        container=container_name,
        blob=blob_name
    )

    blob_content = blob_client.download_blob().readall()

    return jsonify({
        "status": "success",
        "authentication": "Azure managed identity",
        "blob": blob_name,
        "content": blob_content.decode("utf-8")
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

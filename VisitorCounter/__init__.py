import logging
import os
import json
import azure.functions as func
from azure.data.tables import TableClient, UpdateMode
from azure.core.credentials import AzureNamedKeyCredential
from azure.core.exceptions import ResourceNotFoundError

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("🚀 Python VisitorCounter function triggered.")

    account_name = os.environ.get("TABLE_ACCOUNT")
    account_key = os.environ.get("TABLE_KEY")
    table_name = os.environ.get("TABLE_NAME")

    if not all([account_name, account_key, table_name]):
        logging.error("Missing one or more required environment variables.")
        return func.HttpResponse("Server config error", status_code=500)

    try:
        credential = AzureNamedKeyCredential(account_name, account_key)
        table_client = TableClient(
            endpoint=f"https://{account_name}.table.cosmos.azure.com:443",
            table_name=table_name,
            credential=credential
        )

        partition_key = "resume"
        row_key = "visitorCounter"

        try:
            entity = table_client.get_entity(partition_key=partition_key, row_key=row_key)
            count = int(entity.get("count", 0)) + 1
            entity["count"] = count
            table_client.update_entity(entity=entity, mode=UpdateMode.REPLACE)
        except ResourceNotFoundError:
            entity = {"PartitionKey": partition_key, "RowKey": row_key, "count": 1}
            table_client.create_entity(entity)
            count = 1

        return func.HttpResponse(
            body=json.dumps({"count": count}),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"💥 Unhandled error: {str(e)}")
        return func.HttpResponse("Internal Server Error", status_code=500)

import logging
import os
import azure.functions as func
from azure.data.tables import TableClient
from azure.core.credentials import AzureNamedKeyCredential

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python VisitorCounter function triggered.")

    account_name = os.environ.get("TABLE_ACCOUNT")
    account_key = os.environ.get("TABLE_KEY")
    table_name = os.environ.get("TABLE_NAME")

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
        table_client.update_entity(entity, mode="Replace")
    except Exception as e:
        if "ResourceNotFound" in str(e) or "404" in str(e):
            entity = {"PartitionKey": partition_key, "RowKey": row_key, "count": 1}
            table_client.create_entity(entity)
            count = 1
        else:
            logging.error(f"Error accessing table: {str(e)}")
            return func.HttpResponse("Internal Server Error", status_code=500)

    return func.HttpResponse(f"{{\"count\": {count}}}", mimetype="application/json")

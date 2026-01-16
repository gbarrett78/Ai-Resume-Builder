import os
import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.environ.get("TABLE_NAME", "cloud-resume-visitors")
COUNTER_ID = os.environ.get("COUNTER_ID", "homepage")

def _response(status_code: int, body: dict):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Content-Type": "application/json",
        },
        "body": json.dumps(body),
    }

def main():
    # CI pipeline entry point (GitHub Actions)
    html = "<html><body><h1>Resume Pipeline Running</h1><body></html>"

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Generated index.html")

def legacy_lambda_handler(event, context):
    try:
        # Handle CORS preflight
        if (
            event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS"
            or event.get("httpMethod") == "OPTIONS"
        ):
            return _response(200, {"ok": True})

        table = dynamodb.Table(TABLE_NAME)

        result = table.update_item(
            Key={"id": COUNTER_ID},
            UpdateExpression="SET #c = if_not_exists(#c, :zero) + :incr",
            ExpressionAttributeNames={"#c": "count"},
            ExpressionAttributeValues={":incr": 1, ":zero": 0},
            ReturnValues="UPDATED_NEW",
        )

        new_count = int(result["Attributes"]["count"])
        return _response(200, {"visits": new_count})

    except ClientError as e:
        return _response(500, {"error": "DynamoDB error", "details": str(e)})

    except Exception as e:
        return _response(500, {"error": "Server error", "details": str(e)})

if __name__ == "__main__":
    main()
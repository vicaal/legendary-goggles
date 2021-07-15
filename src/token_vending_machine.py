import json
import boto3
import os
from mako.template import Template

sts = boto3.client('sts')

def handler(event, context):

    tenant = event["tenant"]
    item_id = event["item_id"]
    scoped_policy = Template(filename='/var/task/src/policy-template/DynamodbLeadingkeys.json').render(table="legendaryGoggles", tenant=tenant)

    assumed_role = sts.assume_role(
        RoleArn=os.environ.get('ROLE_ARN'), 
        DurationSeconds=900,
        RoleSessionName=tenant,
        Policy=scoped_policy)

    credentails = assumed_role["Credentials"]

    dynamodb = boto3.client(
        service_name='dynamodb',
        aws_access_key_id=credentails["AccessKeyId"], 
        aws_secret_access_key=credentails["SecretAccessKey"],
        aws_session_token=credentails["SessionToken"])

    item = dynamodb.get_item(
        TableName="legendaryGoggles",
        Key={"pk": {"S": item_id }}
    )


    response = {
        "statusCode": 200,
        "items": json.dumps(item["Item"])
    }

    return response
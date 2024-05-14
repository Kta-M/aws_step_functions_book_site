import os
import boto3
import json
import base64
from urllib import parse

# Step Functionsのクライアント
sfn_client = boto3.client('stepfunctions', region_name='ap-northeast-1')

def lambda_handler(event, context):
    param = parse.parse_qs(base64.b64decode(event['body']).decode())
    data = json.loads(param['payload'][0])

    # ボタンのアクションID(approve or reject)
    action = data['actions'][0]['action_id']
    # コールバック用トークン
    taskToken = data['actions'][0]['value']

    if action == 'approve':
        approve(taskToken, { 'result': 'approve' })
    elif action == 'reject':
        reject(taskToken)

# 承認
def approve(taskToken, payload):
    sfn_client.send_task_success(
        taskToken=taskToken,
        output=json.dumps(payload)
    )

# 却下
def reject(taskToken):
    sfn_client.send_task_failure(
        taskToken=taskToken,
        error='Rejected'
    )
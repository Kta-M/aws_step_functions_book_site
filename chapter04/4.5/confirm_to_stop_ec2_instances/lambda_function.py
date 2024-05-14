import os
import boto3
import json
import urllib.request

def lambda_handler(event, context):
    payload = {
        'callback_id': 'confirm_to_stop_ec2_instances',
        'blocks': [
            # メッセージ
            {
                'type': 'section',
                'text': {
                    'type': 'plain_text',
                    'text': event['message']
                }
            },
            # リアクションボタン
            {
                'type': 'actions',
                'elements': [
                    # 承認
                    {
                        'action_id': 'approve',
                        'type': 'button',
                        'style': 'primary',
                        'text': {
                            'type': 'plain_text',
                            'text': event['approve']
                        },
                        # Step Functionsにコールバックする際のトークンを持たせる
                        'value': event['taskToken']
                    },
                    # 却下
                    {
                        'action_id': 'reject',
                        'type': 'button',
                        'style': 'danger',
                        'text': {
                            'type': 'plain_text',
                            'text': event['reject']
                        },
                        'value': event['taskToken']
                    }
                ]
            }
        ]
    }

    # ヘッダ
    headers = {
        'Content-type': 'application/json'
    }

    # リクエスト
    req = urllib.request.Request(
        os.environ['WEBHOOK_URL'],
        data=json.dumps(payload).encode(),
        headers=headers,
        method='POST'
    )
    response = urllib.request.urlopen(req)

    # レスポンス取得
    response_body = response.read().decode('utf-8')
    print('Response:', response_body)
import json

def lambda_handler(event, context):
    print(json.dumps(event))

    return send_invoice(event)

def send_invoice(user):
    user_id = user['id']

    # ここでDBを参照するなどして請求額を計算して、
    # 請求書のPDFを生成して、
    # メールで送る処理を書くようなイメージ

    # "0003"のユーザーは失敗したことにする
    result = user_id != '0003'

    return { 'id': user_id, 'result': result }
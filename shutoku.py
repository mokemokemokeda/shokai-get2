import csv
import os
import requests
import time

# GitHub Secrets から BEARER_TOKEN を取得
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN3")

# BEARER_TOKEN がない場合はエラー
if not BEARER_TOKEN:
    print("Error: BEARER_TOKEN is missing. Check your GitHub Secrets settings.")
    exit(1)

# CSVファイルからユーザー名をリストとして読み込む
with open("usernames.csv", mode="r", encoding="utf-8-sig") as file:
    reader = csv.reader(file)
    usernames = [row[0].strip() for row in reader]  # 全ユーザー名をリストに格納

# 3人ずつ処理する
for i in range(0, len(usernames), 3):
    batch = usernames[i:i+3]  # 3人ずつのグループを作成

    for username in batch:
        print(f"Fetching bio for {username}")

        # Twitter API のエンドポイント（自己紹介文を取得）
        url = f"https://api.twitter.com/2/users/by/username/{username}?user.fields=description"

        # APIリクエストのヘッダー
        headers = {
            "Authorization": f"Bearer {BEARER_TOKEN}",
        }

        try:
            response = requests.get(url, headers=headers)
            response_json = response.json()

            if response.status_code == 200:
                user_data = response_json.get("data", {})
                bio = user_data.get("description", "No bio available")
                print(f"{username} の自己紹介: {bio}")
            else:
                print(f"Error: HTTP {response.status_code} for {username}")
                print("Response:", response_json)  # エラーメッセージを表示

        except Exception as e:
            print(f"Error for {username}: {str(e)}")  # 例外の詳細を表示

    # 3人処理した後、まだ処理が残っている場合は30分待機
    if i + 3 < len(usernames):
        print("Waiting for 30 minutes before fetching the next batch...")
        time.sleep(10)  # 1800秒 = 30分

print("All users processed. Script finished.")

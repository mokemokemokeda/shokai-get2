import os
import requests
import csv

# GitHub Secrets から BEARER_TOKEN を取得
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# BEARER_TOKEN がない場合はエラー
if not BEARER_TOKEN:
    print("Error: BEARER_TOKEN is missing. Check your GitHub Secrets settings.")
    exit(1)

# CSVファイルのパス（GitHubリポジトリのルートに `usernames.csv` を置く想定）
CSV_FILE = "usernames.csv"

# APIリクエストのヘッダー
headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
}

# CSVを読み込んで処理
try:
    with open(CSV_FILE, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if not row:  # 空行はスキップ
                continue

            username = row[0].strip()  # ユーザー名を取得

            # Twitter API のエンドポイント（自己紹介文を取得）
            url = f"https://api.twitter.com/2/users/by/username/{username}?user.fields=description"

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
    print("Error:", str(e))  # 例外の詳細を表示

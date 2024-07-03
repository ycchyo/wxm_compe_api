import requests
import json
import datetime
import pandas as pd
import os
import warnings
import logging
import logging.config
warnings.simplefilter("ignore")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)
#
file_path = resource_path('./userinfo.csv')
df = pd.read_csv(file_path, encoding='utf_8', keep_default_na=False, low_memory=False)
# print(df.iloc[0,1])

TOKEN = df.iloc[0, 1]
# ORG_ID = df.iloc[1, 1]
# LOCID = df.iloc[2, 1]
# HOLIDAY_NAME = df.iloc[3, 1]
# YEAR = df.iloc[4, 1]

now = datetime.datetime.now()
Date_log = now.strftime("%Y%m%d%H%M")

url = f"https://webexapis.com/v1/meetings?"
url_webhook = f"https://webexapis.com/v1/webhooks?max=100&ownedBy=org"
payload = {}
headers = {
  'Authorization': f'Bearer {TOKEN}',
  'Content-Type': 'application/json'
}
def logging_setup():
    DIR = "logfile"
    if not os.path.exists(DIR):
        # ディレクトリが存在しない場合、ディレクトリを作成する
        os.makedirs(DIR)
    # フォーマットを指定
    fmtstr = '%(asctime)s: %(levelname)s: %(funcName)s Line:%(lineno)d %(message)s'

    # ログをファイルに出力する設定
    logging.basicConfig(
        level=logging.DEBUG,  # 'DEBUG' なら logging.DEBUGを指定していることになる
        format=fmtstr,
        filemode="w", # 上書きはw追記はa
        filename=f'./logfile/output_{Date_log}.log'
    )
    # コンソールにもログを表示するハンドラを追加
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # コンソールのログレベルも設定（DEBUGなど）
    console_formatter = logging.Formatter(fmtstr)
    console_handler.setFormatter(console_formatter)

    logging.getLogger().addHandler(console_handler)
def getmeetinglist():
    response = requests.request("GET", url, headers=headers,
                             data=payload)

    res_j = response.json()
    print("GET for MeetingList" + "-" * 10)
    print(response)
    print(json.dumps(res_j, indent=4, ensure_ascii=False))
    # Get the length of the 'items' list
    num_items = len(res_j.get("items", []))
    # print(num_items)
    # 各アイテムの内容を表示
    for item in res_j.get("items", []):
        print("-" * 20)
        print(f"Title:{item.get('title', '')}")
    # with open('outputlogs_wxm_{0:%Y%m%d_%H%M%S}.txt'.format(now), 'w', encoding='UTF-8') as f:
    #     # f.write(f"{url_api}""\n")
    #     f.write("GET" + "-" * 10 + "\n")
    #     json.dump(res_j, f, ensure_ascii=False, indent=4)
def webhook():
    response = requests.request("GET", url, headers=headers,
                             data=payload)
    res_j = response.json()
    print("GET for Webhook" + "-" * 10)
    print(response)
    print(json.dumps(res_j, indent=4, ensure_ascii=False))

def createmeeting():
    # Meeting details
    title = "My Meeting"
    start_time = "2024-07-04T14:00:00Z"
    end_time = "2024-07-04T15:00:00Z"
    host_Email = "yuichi.okubo@nttcdd.com"
    timezone = "Japan"
    # Create the request body
    payload = json.dumps({
        "title": title,#mandatory
        "start": start_time,#mandatory
        "end": end_time,#mandatory
        "hostEmail": host_Email,
        "timezone ": timezone,
        "agenda": "This is the meeting agenda.",
        "enable_recordings": True
    }, ensure_ascii=False).encode("utf-8")
    response = requests.request("POST", url, headers=headers,
                             data=payload)
    res_j = response.json()
    print("POST for Create-meeting" + "-" * 10)
    print(response)
    print(json.dumps(res_j, indent=4, ensure_ascii=False))
def main():
    logging_setup()
    logger = logging.getLogger('mainLogging')
    logger.debug('Debug message')
    # INFO レベル以上のログは出力される
    logger.info('Informational message')
    # logger.warning('Warning message')
    logger.error('Error message')
    # logger.critical('Critical message')

if __name__ == '__main__':
    try:
        main()
        # getmeetinglist()
        createmeeting()
    except Exception as e:
        # エラーをコンソールに出力
        print(f"Error: {str(e)}")

        # エラーをログに出力
        logging.error("An error occurred:", exc_info=True)
    # main()
    # webhook()
    # createmeeting()

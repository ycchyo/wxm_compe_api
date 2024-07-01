import requests
import json
import datetime
import pandas as pd
import os
import warnings
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

url = f"https://webexapis.com/v1/meetings?"
# url_base = f"https://webexapis.com/v1/"
payload = {}
headers = {
  'Authorization': f'Bearer {TOKEN}',
  'Content-Type': 'application/json'
}

def main():
    response = requests.request("GET", url, headers=headers,
                             data=payload)

    res_j = response.json()
    print("GET" + "-" * 10)
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


if __name__ == '__main__':
    main()


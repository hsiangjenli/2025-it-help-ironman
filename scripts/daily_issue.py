import os
import requests
import csv
import pandas as pd
from datetime import datetime, timedelta
from dateutil import tz

github_token = os.environ.get('GITHUB_TOKEN')
repo_owner = os.environ.get('REPO_OWNER')
repo_name = os.environ.get('REPO_NAME')
sheet_name = 'LLM-IT-HELP'
spreadsheet_id = os.environ.get('GSHEET_ID')
plan_path = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
headers = {'Authorization': f'token {github_token}'}

def get_today_day():
    # 以 Asia/Taipei 時區計算
    tz_tw = tz.gettz('Asia/Taipei')
    today = datetime.now(tz=tz_tw)
    return today.day

def get_issue_by_day(day):
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues'
    params = {'state': 'all', 'labels': f'Day{day}'}
    resp = requests.get(url, headers=headers, params=params)
    if resp.ok:
        issues = resp.json()
        return issues[0] if issues else None
    return None

def get_pr_for_issue(issue_number):
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}/events'
    resp = requests.get(url, headers=headers)
    if resp.ok:
        for event in resp.json():
            if event['event'] == 'closed' and event.get('commit_id'):
                return True
    return False

def create_issue(day, plan):
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues'
    title = f"Day {day}: {plan['主題']}"
    body = f"分類: {plan['分類']}\n\n指引: {plan['當日指引']}"
    labels = [f"Day{day}"]
    data = {'title': title, 'body': body, 'labels': labels}
    resp = requests.post(url, headers=headers, json=data)
    return resp.ok

def main():
    # 讀取所有計畫 day（用 pandas 直接讀 Excel）
    df = pd.read_csv(plan_path)
    days = df['Day'].astype(int).tolist()

    for day in days:
        plan = df[df['Day'] == day]
        if not plan:
            continue
        # 檢查上一個 day 是否已完成
        if day > 1:
            prev_issue = get_issue_by_day(day - 1)
            if not prev_issue or prev_issue['state'] != 'closed':
                print(f"Day {day-1} not finished, skip Day {day}")
                break
        # 檢查本 day 是否已存在 issue
        if get_issue_by_day(day):
            continue
        # 建立 issue
        if create_issue(day, plan):
            print(f"Issue for Day {day} created!")
        else:
            print(f"Issue creation for Day {day} failed.")
        break

if __name__ == '__main__':
    main()

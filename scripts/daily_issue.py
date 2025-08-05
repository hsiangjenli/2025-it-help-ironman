import os
import requests
import csv
from datetime import datetime, timedelta
from dateutil import tz

github_token = os.environ.get('GITHUB_TOKEN')
repo_owner = os.environ.get('REPO_OWNER')
repo_name = os.environ.get('REPO_NAME')
plan_path = os.path.join('.github', 'plan.tsv')
headers = {'Authorization': f'token {github_token}'}

def get_today_day():
    # 以 Asia/Taipei 時區計算
    tz_tw = tz.gettz('Asia/Taipei')
    today = datetime.now(tz=tz_tw)
    return today.day

def read_plan(day):
    with open(plan_path, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if int(row['Day']) == day:
                return row
    return None

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
    today_day = get_today_day()
    plan = read_plan(today_day)
    if not plan:
        print(f"No plan for Day {today_day}")
        return
    # Day 1 不檢查昨天的 issue
    if today_day > 1:
        prev_issue = get_issue_by_day(today_day - 1)
        if not prev_issue:
            print("昨天的 issue 不存在")
            return
        if prev_issue['state'] != 'closed':
            print("昨天的 issue 尚未關閉")
            return
    # 檢查今天的 issue 是否已存在
    if get_issue_by_day(today_day):
        print("今天的 issue 已存在")
        return
    # Day 1 直接建立 issue
    if create_issue(today_day, plan):
        print("Issue created!")
    else:
        print("Issue creation failed.")

if __name__ == '__main__':
    main()

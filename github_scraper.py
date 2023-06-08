import requests
import json
import time
import csv

username = ''
token = ''


pages = 1000
for page in range(0, pages+1):
    url_repos = f'https://api.github.com/search/repositories?q=stars:%3E1&sort=stars&page={page}&per_page=100'
    print('=========PAGE', page, '===========', url_repos)
    top_repos = requests.get(url_repos, auth=(username,token)).json()
    print(top_repos)
    top_repos = top_repos['items']
    for i in top_repos:
        name = i['name']
        html_url = i['html_url']
        url = i['url']
        out = [name, html_url, url]
        print(out)
        with open("repositories.csv", "a", newline='') as fp:
            writer = csv.writer(fp, delimiter=';',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(out)

with open('repositories.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for row in reader:
        name = row[0]
        html_url = row[1]
        url = row[2]
        print('====OPEN====')
        open_issues_url = url + '/issues?state=open&per_page=100&page='
        open_issues_page = 1
        open_issues_res = requests.get(open_issues_url + str(open_issues_page), auth=(username,token)).json()
        counter_open = 0
        while len(open_issues_res) > 0:
            for issue in open_issues_res:
                issue_url = issue['url']
                issue_html_url = issue['html_url']
                if '/pull/' not in issue_html_url:
                    counter_open+=1
                    title = issue['title']
                    labels = issue['labels']
                    labels = [h['name'] for h in labels]

                    out = [name, html_url, url, title, str(labels), issue_url, issue_html_url]
                    print(open_issues_page, counter_open, title, str(labels), issue_url)
                    with open("issues_initial.csv", "a", newline='', encoding='utf-8') as fp:
                            writer = csv.writer(fp, delimiter=';',
                                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
                            writer.writerow(out)
            time.sleep(0.5)
            open_issues_page += 1
            open_issues_res = requests.get(open_issues_url + str(open_issues_page), auth=(username,token)).json()
        print(counter_open)

        print('====CLOSED====')
        closed_issues_url = url + '/issues?state=closed&per_page=100&page='
        closed_issues_page = 1
        closed_issues_res = requests.get(closed_issues_url + str(closed_issues_page), auth=(username,token)).json()
        counter_closed = 0
        while len(closed_issues_res)!=0:
            for issue in closed_issues_res:
                issue_url = issue['url']
                issue_html_url = issue['html_url']
                if '/pull/' not in issue_html_url:
                    counter_closed+=1
                    # if counter_closed>327:
                    title = issue['title']
                    labels = issue['labels']
                    labels = [h['name'] for h in labels]

                    out = [name, html_url, url, title, str(labels), issue_url, issue_html_url]
                    print(closed_issues_page, counter_closed, title, str(labels), issue_url)
                    with open("issues_initial.csv", "a", newline='', encoding='utf-8') as fp:
                        writer = csv.writer(fp, delimiter=';',
                                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        writer.writerow(out)
            time.sleep(0.5)
            closed_issues_page += 1
            closed_issues_res = requests.get(closed_issues_url + str(closed_issues_page), auth=(username,token)).json()

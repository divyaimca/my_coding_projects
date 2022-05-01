## Date : 28th Mar 2022
## Maintainer : priyadarshee.dibyashree.kumar
## To create PR and Merge PR in git
from urllib import response
import argparse
import requests
import json

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def createPR(token, api, repo, title, branch):
    print("Creating Pull Request")
    headers = {
       "Accept": "application/vnd.github.v3+json",
       'Content-Type': 'application/x-www-form-urlencoded',
       "Authorization": f"token {token}"
    }
    payload = {
       "base": "master",
       "head": branch,
       "title": title,
       "body": title
    }
    uri = api + "/" + repo + "/pulls" 

    response = requests.post(uri, data=json.dumps(payload), headers=headers, verify=False) 
    parsed = json.loads(response.content)
    pretty_response = json.dumps(parsed, indent=4, sort_keys=True)
    print(response.status_code)
    if response.status_code not in [200, 201]:
        raise Exception(f"Response : {response.status_code}, {pretty_response}")
    else:
        print(f"PR Create successfull with response : {response.json()['url']}")
        return(response.json()["url"])

def getPR(token, api, repo, branch):
    headers = {
       "Accept": "application/vnd.github.v3+json",
       'Content-Type': 'application/x-www-form-urlencoded',
       "Authorization": f"token {token}"
    }
    uri = api + "/" + repo + "/pulls" 
    response = requests.get(uri, headers=headers, verify=False)
    if response.status_code == 200:
        for pr in response.json():
            pr_branch = pr["head"]["ref"]
            if pr_branch == branch:
                pr_num = pr["url"]
                return [response.status_code, pr_num]
    else:
        raise Exception(f"No PR found with branch : {branch} in repo {repo}")

def mergePR(token, api, repo, title, branch, extra_message):
    print("Merging Pull Request..")
    print("Collecting PR details..")
    [ status, pr_url ]= getPR(token, api, repo, branch)
    if status in [200,201]:
        print(f"Got the PR : {pr_url}")
    else:
        raise Exception(f"No PR found with branch : {branch} in repo {repo}")
    
    pull_number = pr_url.split("/")[-1]
    headers = {
       "Accept": "application/vnd.github.v3+json",
       'Content-Type': 'application/x-www-form-urlencoded',
       "Authorization": f"token {token}"
    }
    payload = {
       "commit_title": title,
       "commit_message": extra_message,
       "pull_number": pull_number,
    }
    uri = pr_url + "/merge"
    response = requests.put(uri, data=json.dumps(payload), headers=headers, verify=False)

    parsed = json.loads(response.content)
    pretty_response = json.dumps(parsed, indent=4, sort_keys=True)

    if  response.status_code == 200:
        print(f"Pull Request : {pr_url} Merged successfully in repo {repo}")
    else:
        raise Exception(f"PR Merge unsuccessfull, Response : {response.status_code}, {pretty_response}")


def main():
    if (args.gitAction == "createPR"):
        prNumber = createPR(args.token, args.gitApi, args.gitRepo, args.title, args.branch)
        print(f"PR Created : {prNumber}")
    elif (args.gitAction == "mergePR"):
        mergePR(args.token, args.gitApi, args.gitRepo, args.title, args.branch, args.emessage)
    else:
        print("No git action selected")

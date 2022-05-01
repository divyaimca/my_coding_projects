#Create PR
python3 gitOps.py --gitApi=$repositoryApiUrl --token=$GITHUB_CREDENTIAL_PSW --gitAction="createPR" --branch=$strBranchName --gitRepo=$strRepoName --title="$pullRequestTitle"

#Merge PR
python3 gitOps.py --gitApi=$repositoryApiUrl --token=$GITHUB_CREDENTIAL_PSW --gitAction="mergePR" --branch=$strBranchName --gitRepo=$strRepoName --title="$pullRequestTitle" --emessage="$pullRequestMessage"
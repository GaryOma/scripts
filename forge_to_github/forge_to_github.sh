#! /bin/bash

PREFIX="forge-"
input="repos.txt"
GIT_PREFIX="git@github.com:GaryOma/"

creds="github.txt"
user=$(cat $creds | cut -d" " -f 1)
pass=$(cat $creds | cut -d" " -f 2)
export GITHUB_USER=$user
export GITHUB_PASSWORD=$pass

while IFS= read -r line
do
    name=$(echo $line | cut -d" " -f 1)
    url=$(echo $line | cut -d" " -f 2)
    repo_name="$PREFIX$name"
    echo "Cloning $name ..."
    git clone $url
    cd */
    echo "Creating $repo_name ..."
    git config hub.protocol ssh
    hub create -p $repo_name
    repo_url="$GIT_PREFIX$repo_name"
    git remote set-url origin $repo_url
    git config user.email "gary.sublet@hotmail.fr"
    git config user.name "Gary SUBLET"
    echo "Pushing to $repo_url ..."
    git push
    cd ..
    sudo rm -r */
done < "$input"

#!/bin/bash

border () {
    local str="$*"      # Put all arguments into single string
    local len=${#str}
    local i
    for (( i = 0; i < len + 4; ++i )); do
        printf '-'
    done
    printf "\n| $str |\n"
    for (( i = 0; i < len + 4; ++i )); do
        printf '-'
    done
    echo
}

 pip freeze > requirements.txt

git add .

read -p "Commit Message: " message
git commit -m "$message"

declare -a repositories=("origin" "heroku")

for repo in "${repositories[@]}"
do
    git push "$repo" master
    border "Pushed the Commit to "$repo" Sucessfuly"
done

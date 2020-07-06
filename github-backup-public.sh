# Create the backup in the dir of a current date: YYYYMMDD
date=$(date "+%Y%m%d")
mkdir "$date"
cd "$date" || exit

# Inspect repos from page 1 | max repos per page is 100
curl "https://api.github.com/users/AngryMaciek/repos?page=1&per_page=100" |
grep -e "git_url*" |
cut -d \" -f 4 |
xargs -L1 git clone

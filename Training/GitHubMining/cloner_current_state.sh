github_link=$1
language=$2

# replace cat with head -10 to clone only the top 10 repos
# remove depth flag from "git clone -q --depth 1 https://github.com/$org/$name $DIR/$name" to retain history
echo "github_link: $github_link" 
echo "language: $language" 

name_part=$(echo $github_link | cut -d"/" -f4-6)
name=$(echo $name_part | cut -d"/" -f2)
org=$(echo $name_part | cut -d"/" -f1)

echo "Cloning $org/$name"

DIR=./data/GitHubMining/CurrentState/$language/$org
# DIR=./data/GitHubMining/RawTestData/$language/$org

mkdir -p $DIR; 
echo "Dir created! Path: $DIR"; 

git clone -q --depth 1 https://github.com/$org/$name $DIR/$name
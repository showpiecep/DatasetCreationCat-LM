language=python
# in_file=data/GitHubMining/test_python.txt || можно завести отдельный файл с репоизиториями которые не входят в трейн
in_file=${1:-"python-top-repos.txt"}

# --- Для другого языка ---
# language=java
# in_file=/data/GitHubMining/test_java.txt

# head заменил на tail, т.к. взял 1000 с конца из всех данных из файла 
tail -500 $in_file | xargs -P32 -n1 -I% bash -c '
    echo %; \
    line=$"%";\
    line_array=($line);\
    github_link=${line_array[0]};\
    ./extract_pairs.sh $github_link '$language'
    #./cloner_current_state.sh $github_link '$language'; \
'


# unbuffer ./mine_test_data.sh 2>&1 | tee output_mine_test_data_java.txt
# unbuffer ./mine_test_data.sh 2>&1 | tee output_mine_test_data_python.txt
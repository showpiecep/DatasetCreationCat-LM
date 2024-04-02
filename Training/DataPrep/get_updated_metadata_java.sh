language=java
in_file=../GitHubMining/java-top-repos.txt
head -49000 $in_file | xargs -P32 -n1 -I% bash -c 'echo %; \
line=$"%";\
line_array=($line);\
github_link=${line_array[0]};\
unbuffer python3 get_metadata_after_dedup.py $github_link '$language 2>&1 | tee output_metadata_java.txt
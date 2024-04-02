language=python
in_file=../GitHubMining/cutted_python-top-repos.txt     # python-top-repos.txt
head -1500 $in_file | xargs -P1 -n1 -I% bash -c 'echo %; \
line=$"%";\
line_array=($line);\
github_link=${line_array[0]};\
unbuffer python3 get_metadata_after_dedup.py $github_link '$language 2>&1 | tee output_metadata_python.txt
language=java
in_file=java-top-repos.txt
head -49000 $in_file | xargs -P32 -n1 -I% bash -c 'echo %; \
line=$"%";\
line_array=($line);\
github_link=${line_array[0]};\
./cloner_current_state.sh $github_link '$language'; \
./extract_pairs.sh $github_link '$language


# unbuffer ./mine_code_test_pairs_java.sh 2>&1 | tee output_mine_java.txt

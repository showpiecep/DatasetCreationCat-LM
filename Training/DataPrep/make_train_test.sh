input_path=/data/GitHubMining/CurrentStateDeduplicated
train_test_output_dir=/data/GitHubMining
output_dir=/data/GitHubMining/Output
python_repos_file=../GitHubMining/python-top-repos.txt
java_repos_file=../GitHubMining/java-top-repos.txt


python3 make_train_test.py \
    --repo_dir=$input_path \
    --train_test_output_dir=$train_test_output_dir \
    --output_dir=$output_dir \
    --python_repos_file=$python_repos_file \
    --java_repos_file=$java_repos_file 

# unbuffer python3 make_train_test.py \
#     --input_path=$input_path \
#     --train_test_output_dir=$train_test_output_dir \
#     --output_dir=$output_dir \
#     --python_repos_file=$python_repos_file \
#     --java_repos_file=$java_repos_file 2>&1 | tee output_train_test_split_python.txt

# old 
# unbuffer python3 make_train_test.py \
    # $input_path \
    # $train_test_output_dir \
    # $output_dir \
    # $python_repos_file \
    # $java_repos_file  2>&1 | tee output_train_test_split_python.txt
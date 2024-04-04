input_path=./data/GitHubMining/CurrentStateDeduplicated
train_dir=./data/GitHubMining/CurrentStateProcessed/train
test_dir=./data/GitHubMining/CurrentStateProcessed/test
output_dir=../GitHubMining/data/GitHubMining/Output
train_test_list_path=./data/GitHubMining
language=python

python3 concatinate_pairs.py \
    --repo_dir=$input_path \
    --train_dir=$train_dir \
    --test_dir=$test_dir \
    --output_dir=$output_dir \
    --train_test_list_path=$train_test_list_path \
    --pl=$language

# unbuffer python3 concatinate_pairs.py \
#     --repo_dir=$input_path \
#     --train_dir=$train_dir \
#     --test_dir=$test_dir \
#     --output_dir=$output_dir \
#     --train_test_list_path=$train_test_list_path \
#     --language=$language  2>&1 | tee output_concat_fp_python.txt
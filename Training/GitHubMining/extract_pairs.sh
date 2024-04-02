github_link=$1
language=$2

# нужно, чтобы файл extract_file_pairs.py видел поддиректории строчки 18, 19
meta_folder=MetaData
pairs_folder=FilePairs

input_dir=./data/GitHubMining/CurrentState/$language/
output_dir=./data/GitHubMining/Output/$language/

# input_dir=/data/GitHubMining/RawDataSample/$language/
# output_dir=/data/GitHubMining/RawDataSampleOutput/$language/

mkdir -p $output_dir/{$meta_folder,$pairs_folder}

python3 extract_file_pairs.py $input_dir $output_dir $github_link $language


# # --- old code --- 
# # Не работает так как появляются ошибки FileNotFoundError: [Errno 2] No such file or directory: \
# # './data/GitHubMining/Output/python/MetaData/some_json_name.json'

# github_link=$1
# language=$2

# input_dir=./data/GitHubMining/CurrentState/$language/
# output_dir=./data/GitHubMining/Output/$language/

# # input_dir=./data/GitHubMining/RawDataSample/$language/
# # output_dir=./data/GitHubMining/RawDataSampleOutput/$language/

# mkdir -p $output_dir

# python3 extract_file_pairs.py $input_dir $output_dir $github_link $language
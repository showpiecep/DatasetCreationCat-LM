input_path=/data/GitHubMining/RawDataSample
train_test_output_dir=/data/GitHubMining
output_dir=/data/GitHubMining/RawDataSampleOutput

python3 filter_test_set_fp.py $input_path $train_test_output_dir $output_dir  2>&1 | tee output_filter_test_set.txt
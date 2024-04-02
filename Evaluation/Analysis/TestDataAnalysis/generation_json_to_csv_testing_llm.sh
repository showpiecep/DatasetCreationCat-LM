input_json_java='/data/GitHubMining/TestFramework/TestingLLM/java/asserts_completion_metrics_ds.json'
data_json_java='/data/GitHubMining/TestFramework/TestingLLM/java/completion_baseline_covs.json'
output_csv_java='/data/GitHubMining/TestFramework/TestingLLM/java/asserts_completion_metrics_ds.csv'

input_json_python='/data/GitHubMining/TestFramework/TestingLLM/python/asserts_completion_metrics_ds.json'
data_json_python='/data/GitHubMining/TestFramework/TestingLLM/python/completion_baseline_covs.json'
output_csv_python='/data/GitHubMining/TestFramework/TestingLLM/python/asserts_completion_metrics_ds.csv'

python3 generation_json_to_csv.py $input_json_java $data_json_java $output_csv_java
python3 generation_json_to_csv.py $input_json_python $data_json_python $output_csv_python
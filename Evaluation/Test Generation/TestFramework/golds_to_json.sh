completions_path="/data/GitHubMining/Generated_TestOutputs"
frameworks_path="/data/GitHubMining/TestFramework"
output_path="/data/GitHubMining/TextMetrics/TestGeneration"

python3 golds_to_json.py $completions_path "java" $frameworks_path $output_path
python3 golds_to_json.py $completions_path "python" $frameworks_path $output_path
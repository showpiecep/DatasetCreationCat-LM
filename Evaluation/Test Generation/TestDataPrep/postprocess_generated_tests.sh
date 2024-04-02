completions_path="/data/GitHubMining/Generated_TestOutputs"
frameworks_path="/data/GitHubMining/TestFramework"
output_path="/data/GitHubMining/TextMetrics/TestGeneration"

# python3 postprocess_generated_tests.py $completions_path "java" 0.2 10 $frameworks_path $output_path
# python3 postprocess_generated_tests.py $completions_path "java" 0.8 10 $frameworks_path $output_path
python3 postprocess_generated_tests.py $completions_path "python" 0.2 10 $frameworks_path $output_path
# python3 postprocess_generated_tests.py $completions_path "python" 0.8 10 $frameworks_path $output_path
teco_completions_path="/data/GitHubMining/Generated_TestOutputs/TecoContexts"
num_samples=10
fps_path="/data/GitHubMining/TestFramework/teco_fps.json"
teco_gold_statements_path="/code/teco/_work/setup/CSNm/eval-any-stmt/test/gold_stmts.jsonl"
output_path="/data/GitHubMining/TextMetrics/Teco"

python3 postprocess_generated_tests.py $teco_completions_path 0.2 $num_samples $fps_path $teco_gold_statements_path $output_path
# python3 postprocess_generated_tests.py $teco_completions_path 0.8 $num_samples $fps_path $teco_gold_statements_path $output_path
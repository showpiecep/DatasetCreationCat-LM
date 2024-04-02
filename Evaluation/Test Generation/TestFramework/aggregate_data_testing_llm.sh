filepair_dir=/data/GitHubMining/TestFramework
generations_dir=/data/GitHubMining/Generated_TestOutputs
aggregation_dir=/data/GitHubMining/TestFramework/TestingLLM
preds_root=/data/GitHubMining/TextMetrics/TestGeneration

python3 aggregate_data.py $filepair_dir $generations_dir $aggregation_dir $preds_root
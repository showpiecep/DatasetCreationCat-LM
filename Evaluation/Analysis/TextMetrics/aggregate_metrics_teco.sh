metrics_path="/data/GitHubMining/TextMetrics/Teco/teco_metrics_0.2.json"
output_path="/data/GitHubMining/TextMetrics/Teco/teco_aggregated_metrics_0.2.json"

metrics_path08="/data/GitHubMining/TextMetrics/Teco/teco_metrics_0.8.json"
output_path08="/data/GitHubMining/TextMetrics/Teco/teco_aggregated_metrics_0.8.json"


python3 aggregate_metrics_teco.py $metrics_path $output_path 
python3 aggregate_metrics_teco.py $metrics_path08 $output_path08 
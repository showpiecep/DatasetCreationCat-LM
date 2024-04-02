preds_path="/data/GitHubMining/TextMetrics/Teco/teco_preds_0.2.json"
golds_path="/data/GitHubMining/TextMetrics/Teco/teco_gold.json"
output_path="/data/GitHubMining/TextMetrics/Teco/teco_metrics_0.2.json"
pl="java"

preds_path08="/data/GitHubMining/TextMetrics/Teco/teco_preds_0.8.json"
golds_path08="/data/GitHubMining/TextMetrics/Teco/teco_gold.json"
output_path08="/data/GitHubMining/TextMetrics/Teco/teco_metrics_0.8.json"

python3 compute_metrics_teco.py $preds_path $golds_path $output_path $pl
# python3 compute_metrics_teco.py $preds_path08 $golds_path08 $output_path08 $pl
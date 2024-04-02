github_link=$1
language=$2

input_dir=/data/GitHubMining/CurrentState/$language/
output_dir=/data/GitHubMining/Output/$language/

echo $github_link
mkdir -p $output_dir
python3 compute_corpus_stats.py $input_dir $output_dir $github_link
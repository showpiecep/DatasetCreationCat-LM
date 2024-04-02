input_path=../GitHubMining/data/GitHubMining/CurrentState
copy_dir=data/GitHubMining/CurrentStateDeduplicated
metadata_dir=data/GitHubMining/DeduplicationMetaData

repos_file=../GitHubMining/cutted_python-top-repos.txt

language=python

# python3 main_deduplicate_data.py \
#   --repo_dir=$input_path \
#   --copy_dir=$copy_dir \
#   --metadata_dir=$metadata_dir \
#   --repos_file_path=$repos_file

unbuffer python3 main_deduplicate_data.py \
  --repo_dir=$input_path \
  --copy_dir=$copy_dir \
  --metadata_dir=$metadata_dir \
  --repos_file_path=$repos_file \
  --pl=$language  2>&1 | tee cutted_output_dedup_python.txt
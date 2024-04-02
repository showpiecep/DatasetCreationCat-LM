input_path=/data/GitHubMining/CurrentState
copy_dir=/data/GitHubMining/CurrentStateDeduplicated
metadata_dir=/data/GitHubMining/DeduplicationMetaData
repos_file=../GitHubMining/java-top-repos.txt
language=java

unbuffer python3 main_deduplicate_data.py $input_path $copy_dir $metadata_dir $repos_file $language  2>&1 | tee output_dedup_java.txt
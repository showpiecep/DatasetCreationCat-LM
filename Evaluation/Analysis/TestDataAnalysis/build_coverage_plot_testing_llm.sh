aggregation_dir='/data/GitHubMining/TestFramework/'
generations_dir='/data/GitHubMining/Generated_TestOutputs/'
output_fp_java='/data/GitHubMining/TestFramework/TestingLLM/java/java_coverage_trejs.png'
output_fp_python='/data/GitHubMining/TestFramework/TestingLLM/python/python_coverage_trejs.png'

python3 build_coverage_plot.py $aggregation_dir $generations_dir $output_fp_java $output_fp_python
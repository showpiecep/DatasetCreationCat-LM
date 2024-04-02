metrics_path_02_java="/data/GitHubMining/TextMetrics/TestGeneration/java_t0.2_n10_metrics.json"
output_path_02_java="/data/GitHubMining/TextMetrics/TestGeneration/java_t0.2_n10_aggregated_metrics.json"

metrics_path_08_java="/data/GitHubMining/TextMetrics/TestGeneration/java_t0.8_n10_metrics.json"
output_path_08_java="/data/GitHubMining/TextMetrics/TestGeneration/java_t0.8_n10_aggregated_metrics.json"

metrics_path_02_python="/data/GitHubMining/TextMetrics/TestGeneration/python_t0.2_n10_metrics.json"
output_path_02_python="/data/GitHubMining/TextMetrics/TestGeneration/python_t0.2_n10_aggregated_metrics.json"

metrics_path_08_python="/data/GitHubMining/TextMetrics/TestGeneration/python_t0.8_n10_metrics.json"
output_path_08_python="/data/GitHubMining/TextMetrics/TestGeneration/python_t0.8_n10_aggregated_metrics.json"

metrics_path_codegen2B_02_java="/data/GitHubMining/TextMetrics/TestGeneration/java_codegen-2B-multi_t0.2_n10_v2_metrics.json"
output_path_codegen2B_02_java="/data/GitHubMining/TextMetrics/TestGeneration/java_codegen-2B-multi_t0.2_n10_v2_aggregated_metrics.json"

metrics_path_codegen16B_02_java="/data/GitHubMining/TextMetrics/TestGeneration/java_codegen-16B-multi_t0.2_n10_metrics.json"
output_path_codegen16B_02_java="/data/GitHubMining/TextMetrics/TestGeneration/java_codegen-16B-multi_t0.2_n10_aggregated_metrics.json"

metrics_path_codegen2B_02_python="/data/GitHubMining/TextMetrics/TestGeneration/python_codegen-2B-multi_t0.2_n10_metrics.json"
output_path_codegen2B_02_python="/data/GitHubMining/TextMetrics/TestGeneration/python_codegen-2B-multi_t0.2_n10_aggregated_metrics.json"

metrics_path_codegen16B_02_python="/data/GitHubMining/TextMetrics/TestGeneration/python_codegen-16B-multi_t0.2_n10_metrics.json"
output_path_codegen16B_02_python="/data/GitHubMining/TextMetrics/TestGeneration/python_codegen-16B-multi_t0.2_n10_aggregated_metrics.json"


metrics_path_codegen2Bmono_02_python="/data/GitHubMining/TextMetrics/TestGeneration/python_codegen-2B-mono_t0.2_n10_metrics.json"
output_path_codegen2Bmono_02_python="/data/GitHubMining/TextMetrics/TestGeneration/python_codegen-2B-mono_t0.2_n10_aggregated_metrics.json"

metrics_path_codegen16Bmono_02_python="/data/GitHubMining/TextMetrics/TestGeneration/python_codegen-16B-mono_t0.2_n10_metrics.json"
output_path_codegen16Bmono_02_python="/data/GitHubMining/TextMetrics/TestGeneration/python_codegen-16B-mono_t0.2_n10_aggregated_metrics.json"


# python3 aggregate_metrics_test_framework.py $metrics_path_02_java $output_path_02_java 
# python3 aggregate_metrics_test_framework.py $metrics_path_08_java $output_path_08_java 

python3 aggregate_metrics_test_framework.py $metrics_path_02_python $output_path_02_python
# python3 aggregate_metrics_test_framework.py $metrics_path_08_python $output_path_08_python

# python3 aggregate_metrics_test_framework.py $metrics_path_codegen2B_02_java $output_path_codegen2B_02_java "yes"
# python3 aggregate_metrics_test_framework.py $metrics_path_codegen16B_02_java $output_path_codegen16B_02_java "yes"

# python3 aggregate_metrics_test_framework.py $metrics_path_codegen2B_02_python $output_path_codegen2B_02_python "yes"
# python3 aggregate_metrics_test_framework.py $metrics_path_codegen16B_02_python $output_path_codegen16B_02_python "yes"

# python3 aggregate_metrics_test_framework.py $metrics_path_codegen2Bmono_02_python $output_path_codegen2Bmono_02_python "yes"
# python3 aggregate_metrics_test_framework.py $metrics_path_codegen16Bmono_02_python $output_path_codegen16Bmono_02_python "yes"
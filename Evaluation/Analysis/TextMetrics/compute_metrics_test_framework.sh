preds_path_02_py="/data/GitHubMining/TextMetrics/TestGeneration/python_t0.2_n10_filepairs_preds.json"
golds_path_02_py="/data/GitHubMining/TextMetrics/TestGeneration/python_filepairs_golds.json"
output_path_02_py="/data/GitHubMining/TextMetrics/TestGeneration/python_t0.2_n10_metrics.json"

preds_path_08_py="/data/GitHubMining/TextMetrics/TestGeneration/python_t0.8_n10_filepairs_preds.json"
golds_path_08_py="/data/GitHubMining/TextMetrics/TestGeneration/python_filepairs_golds.json"
output_path_08_py="/data/GitHubMining/TextMetrics/TestGeneration/python_t0.8_n10_metrics.json"

preds_path_02_java="/data/GitHubMining/TextMetrics/TestGeneration/java_t0.2_n10_filepairs_preds.json"
golds_path_02_java="/data/GitHubMining/TextMetrics/TestGeneration/java_filepairs_golds.json"
output_path_02_java="/data/GitHubMining/TextMetrics/TestGeneration/java_t0.2_n10_metrics.json"

preds_path_08_java="/data/GitHubMining/TextMetrics/TestGeneration/java_t0.8_n10_filepairs_preds.json"
golds_path_08_java="/data/GitHubMining/TextMetrics/TestGeneration/java_filepairs_golds.json"
output_path_08_java="/data/GitHubMining/TextMetrics/TestGeneration/java_t0.8_n10_metrics.json"

preds_path_codegen2B_02_java="/data/GitHubMining/TextMetrics/TestGeneration/java_codegen-2B-multi_t0.2_n10_v2_filepairs_preds.json"
golds_path_codegen2B_02_java="/data/GitHubMining/TextMetrics/TestGeneration/java_filepairs_golds.json"
output_path_codegen2B_02_java="/data/GitHubMining/TextMetrics/TestGeneration/java_codegen-2B-multi_t0.2_n10_v2_metrics.json"

preds_path_codegen2B_02_python="/data/GitHubMining/TextMetrics/TestGeneration/python_codegen-2B-multi_t0.2_n10_filepairs_preds.json"
golds_path_codegen2B_02_python="/data/GitHubMining/TextMetrics/TestGeneration/python_filepairs_golds.json"
output_path_codegen2B_02_python="/data/GitHubMining/TextMetrics/TestGeneration/python_codegen-2B-multi_t0.2_n10_metrics.json"

preds_path_codegen2Bmono_02_python="/data/GitHubMining/TextMetrics/TestGeneration/python_codegen-2B-mono_t0.2_n10_filepairs_preds.json"
golds_path_codegen2Bmono_02_python="/data/GitHubMining/TextMetrics/TestGeneration/python_filepairs_golds.json"
output_path_codegen2Bmono_02_python="/data/GitHubMining/TextMetrics/TestGeneration/python_codegen-2B-mono_t0.2_n10_metrics.json"

preds_path_codegen16B_02_java="/data/GitHubMining/TextMetrics/TestGeneration/java_codegen-16B-multi_t0.2_n10_filepairs_preds.json"
golds_path_codegen16B_02_java="/data/GitHubMining/TextMetrics/TestGeneration/java_filepairs_golds.json"
output_path_codegen16B_02_java="/data/GitHubMining/TextMetrics/TestGeneration/java_codegen-16B-multi_t0.2_n10_metrics.json"

preds_path_codegen16B_02_python="/data/GitHubMining/TextMetrics/TestGeneration/python_codegen-16B-multi_t0.2_n10_filepairs_preds.json"
golds_path_codegen16B_02_python="/data/GitHubMining/TextMetrics/TestGeneration/python_filepairs_golds.json"
output_path_codegen16B_02_python="/data/GitHubMining/TextMetrics/TestGeneration/python_codegen-16B-multi_t0.2_n10_metrics.json"

preds_path_codegen16Bmono_02_python="/data/GitHubMining/TextMetrics/TestGeneration/python_codegen-16B-mono_t0.2_n10_filepairs_preds.json"
golds_path_codegen16Bmono_02_python="/data/GitHubMining/TextMetrics/TestGeneration/python_filepairs_golds.json"
output_path_codegen16Bmono_02_python="/data/GitHubMining/TextMetrics/TestGeneration/python_codegen-16B-mono_t0.2_n10_metrics.json"

python3 compute_metrics_test_framework.py $preds_path_02_py $golds_path_02_py $output_path_02_py "python"
# python3 compute_metrics_test_framework.py $preds_path_08_py $golds_path_08_py $output_path_08_py "python"
# python3 compute_metrics_test_framework.py $preds_path_02_java $golds_path_02_java $output_path_02_java "java"
# python3 compute_metrics_test_framework.py $preds_path_08_java $golds_path_08_java $output_path_08_java "java"

# python3 compute_metrics_test_framework.py $preds_path_codegen2B_02_java $golds_path_codegen2B_02_java $output_path_codegen2B_02_java "java"
# python3 compute_metrics_test_framework.py $preds_path_codegen16B_02_java $golds_path_codegen16B_02_java $output_path_codegen16B_02_java "java"

# python3 compute_metrics_test_framework.py $preds_path_codegen2B_02_python $golds_path_codegen2B_02_python $output_path_codegen2B_02_python "python"
# python3 compute_metrics_test_framework.py $preds_path_codegen16B_02_python $golds_path_codegen16B_02_python $output_path_codegen16B_02_python "python"

# python3 compute_metrics_test_framework.py $preds_path_codegen2Bmono_02_python $golds_path_codegen2Bmono_02_python $output_path_codegen2Bmono_02_python "python"
# python3 compute_metrics_test_framework.py $preds_path_codegen16Bmono_02_python $golds_path_codegen16Bmono_02_python $output_path_codegen16Bmono_02_python "python"
import sys
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def compute_results(projs_data, language):
    buckets = {(1,2): [], (2,3): [], (3,4): [], (4,5): [], (5,1000): []}
    for org in projs_data:
        for proj in projs_data[org]:
            proj_data = projs_data[org][proj]
            for i, (source_fn, test_fn) in enumerate(proj_data):
                curr_trej = []
                results_file = os.path.join(aggregation_dir, "TestingLLM", language, "results", f"{org}____{proj}_v2.json")    
                with open(results_file, "r") as f:
                    proj_info = json.load(f)
                    log_key = f"{source_fn}____{test_fn}"
                    file_pair_data = proj_info[log_key]
                    incremental_test_dir = os.path.join(generations_dir, language, org, proj, f"filepair{i}", "incremental_test_files")
                    num_tests = len(os.listdir(incremental_test_dir))
                    extension = "java" if language == "java" else "py"
                    test_filename = test_fn.split('/')[-1][:-5] if language == "java" else test_fn.split('/')[-1][:-3]
                    for i in range(num_tests):
                        test_gen_path = os.path.join(incremental_test_dir, f"{test_filename}_{i+1}.{extension}")
                        if file_pair_data[f"tests{i}"]["line_coverage"] != "":
                            for start, end in buckets:
                                if start <= i and i < end:
                                    buckets[(start, end)].append(file_pair_data[f"tests{i}"]["line_coverage"])
                                    break

    return buckets


def plot_trejs(buckets, output_file, pl):
    res_arr = []
    labels = []
    for start, end in buckets:
        if start == 1:
            labels.append(f"{start} Test")
        elif start < 5:
            labels.append(f"{start} Tests")
        else:
            labels.append(f"{start}+ Tests")

        res_arr.append(buckets[(start, end)])
    

    # Create the side-by-side boxplots
    df = pd.DataFrame()
    df['value'] = np.concatenate(res_arr)
    df['label'] = np.concatenate([[labels[i]] * len(res_arr[i]) for i in range(len(res_arr))])
    print(df)
    plt.figure(figsize=(6, 6))
    sns.set(style="whitegrid",font_scale=1.3)
    sns.boxplot(x='label', y='value', data=df, palette="pastel", width=0.6)
    # plt.title(f'Coverage distribution of tests ({pl.title()})')
    plt.ylabel('Coverage')
    plt.xlabel('')
    plt.savefig(output_file)

    plt.clf()
    
    

if __name__ == '__main__':
    aggregation_dir = sys.argv[1] if len(sys.argv) > 1 else '/data/GitHubMining/TestFramework/'
    generations_dir = sys.argv[2] if len(sys.argv) > 2 else '/data/GitHubMining/Generated_TestOutputs/'
    output_fp_java = sys.argv[3] if len(sys.argv) > 3 else '/data/GitHubMining/TestFramework/TestingLLM/java/java_coverage_buckets.pdf'
    output_fp_python = sys.argv[4] if len(sys.argv) > 4 else '/data/GitHubMining/TestFramework/TestingLLM/python/python_coverage_buckets.pdf'

    with open(os.path.join(aggregation_dir, "java_filepairs.json"), "r") as f:
        java_data = json.load(f)
    
    trejs = compute_results(java_data, "java")
    plot_trejs(trejs, output_fp_java, "java")

    with open(os.path.join(aggregation_dir, "python_filepairs.json"), "r") as f:
        python_data = json.load(f)
    
    trejs = compute_results(python_data, "python")
    plot_trejs(trejs, output_fp_python, "python")
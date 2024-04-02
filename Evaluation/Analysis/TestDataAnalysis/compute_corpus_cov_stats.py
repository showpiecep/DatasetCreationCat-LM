import sys
import os
import json

def compute_corpus_cov_stats(aggregation_dir, generations_dir, projs_data, language):
    first_test_cov_improvement = []
    last_test_cov_improvement = []
    extra_test_cov_improvement = []

    first_test_cov = []
    last_test_cov = []
    extra_test_cov = []

    for org in projs_data:
        for proj in projs_data[org]:
            proj_data = projs_data[org][proj]
            for i, (source_fn, test_fn) in enumerate(proj_data):
                results_file = os.path.join(aggregation_dir, "TestingLLM", language, "results", f"{org}____{proj}_v2.json")    
                with open(results_file, "r") as f:
                    proj_info = json.load(f)
                    log_key = f"{source_fn}____{test_fn}"
                    file_pair_data = proj_info[log_key]
                    base_coverage = file_pair_data["base_coverage"]["line_coverage"]
                    if base_coverage != 0:
                        extra_test_cov_improvement.append(0)
                        extra_test_cov.append(base_coverage)

                    num_tests = len(os.listdir(os.path.join(generations_dir, language, org, proj, f"filepair{i}", "incremental_test_files")))
                    preamble = file_pair_data["preamble"]["line_coverage"]
                    first_test = file_pair_data["first_test"]["line_coverage"]
                    if first_test == "" or preamble == "":
                        continue
                    first_test_cov_improvement.append(first_test - preamble)
                    first_test_cov.append(first_test)
                    if num_tests > 1:
                        last_test = file_pair_data["all_but_one"]["line_coverage"]
                        baseline = file_pair_data["base_coverage"]["line_coverage"]
                        if last_test == "" or baseline == "":
                            continue
                        last_test_cov_improvement.append(baseline - last_test)
                        last_test_cov.append(last_test)

    print(sum(first_test_cov)/len(first_test_cov))
    print(sum(last_test_cov)/len(last_test_cov))
    print(sum(extra_test_cov)/len(extra_test_cov))

    return first_test_cov_improvement, last_test_cov_improvement, extra_test_cov_improvement



if __name__ == '__main__':
    aggregation_dir = sys.argv[1] if len(sys.argv) > 1 else '/data/GitHubMining/TestFramework/'
    generations_dir = sys.argv[2] if len(sys.argv) > 2 else '/data/GitHubMining/Generated_TestOutputs/'
    output_fp = sys.argv[3] if len(sys.argv) > 3 else '/data/GitHubMining/TestFramework/TestingLLM/python/completion_baseline_covs.csv'
    output_json = sys.argv[4] if len(sys.argv) > 4 else '/data/GitHubMining/TestFramework/TestingLLM/python/completion_baseline_covs.json'

    with open(os.path.join(aggregation_dir, "python_filepairs.json"), "r") as f:
        java_data = json.load(f)
    
    first_test, last_test, extra_test = compute_corpus_cov_stats(aggregation_dir, generations_dir, java_data, "python")

    csv_text = "First Test Coverage Improvement,Last Test Coverage Improvement, Extra Test Coverage Improvement\n"
    first_test_cov_improvement = sum(first_test) / len(first_test)
    last_test_cov_improvement = sum(last_test) / len(last_test)
    extra_test_cov_improvement = sum(extra_test) / len(extra_test)

    first_test_cov_improvement_percent = round(first_test_cov_improvement * 100, 2)
    last_test_cov_improvement_percent = round(last_test_cov_improvement * 100, 2)
    extra_test_cov_improvement_percent = round(extra_test_cov_improvement * 100, 2)

    csv_text += f"{first_test_cov_improvement_percent}% ({len(first_test)}),{last_test_cov_improvement_percent}% ({len(last_test)}),{extra_test_cov_improvement_percent}% ({len(extra_test)})"

    with open(output_fp, "w") as f:
        f.write(csv_text)
    
    with open(output_json, "w") as f:
        json.dump({
            "first_test_total": len(first_test), 
            "last_test_total": len(last_test), 
            "extra_test_total": len(extra_test),
            "first_test_cov": first_test_cov_improvement,
            "last_test_cov": last_test_cov_improvement,
            "extra_test_cov": extra_test_cov_improvement,
        }, f)
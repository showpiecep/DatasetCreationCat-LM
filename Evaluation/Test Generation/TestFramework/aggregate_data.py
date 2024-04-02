import sys
import os
import json
import re

BASELINE_LABELS = ["preamble", "all_but_one", "first_test", "base_coverage"]
LABELS = ("first_test_context", "all_but_one_context", "extra_test_context", "first_test_no_context", "all_but_one_no_context", "extra_test_no_context")

mapping = {
    "t0.2_n10": {
        (0,10): {"label": "first_test", "context": True, "baseline_cov": "preamble", "human_cov": "first_test"}, 
        (10,20): {"label": "last_test", "context": True, "baseline_cov": "all_but_one", "human_cov": "base_coverage"},
        (20,30): {"label": "extra_test", "context": True, "baseline_cov": "base_coverage", "human_cov": "base_coverage"},
        (30,40): {"label": "first_test", "context": False, "baseline_cov": "preamble", "human_cov": "first_test"},
        (40,50): {"label": "last_test", "context": False, "baseline_cov": "all_but_one", "human_cov": "base_coverage"},
        (50,60): {"label": "extra_test", "context": False, "baseline_cov": "base_coverage", "human_cov": "base_coverage"},
    },
    # "t0.2_n10_v2": {
    #     (0,10): {"label": "first_test", "context": True, "baseline_cov": "preamble", "human_cov": "first_test"}, 
    #     (10,20): {"label": "last_test", "context": True, "baseline_cov": "all_but_one", "human_cov": "base_coverage"},
    #     (20,30): {"label": "extra_test", "context": True, "baseline_cov": "base_coverage", "human_cov": "base_coverage"},
    #     (30,40): {"label": "first_test", "context": False, "baseline_cov": "preamble", "human_cov": "first_test"},
    #     (40,50): {"label": "last_test", "context": False, "baseline_cov": "all_but_one", "human_cov": "base_coverage"},
    #     (50,60): {"label": "extra_test", "context": False, "baseline_cov": "base_coverage", "human_cov": "base_coverage"},
    # },
    # "t0.8_n10": {
    #     (0,10): {"label": "first_test", "context": True, "baseline_cov": "preamble", "human_cov": "first_test"}, 
    #     (10,20): {"label": "last_test", "context": True, "baseline_cov": "all_but_one", "human_cov": "base_coverage"},
    #     (20,30): {"label": "extra_test", "context": True, "baseline_cov": "base_coverage", "human_cov": "base_coverage"},
    #     (30,40): {"label": "first_test", "context": False, "baseline_cov": "preamble", "human_cov": "first_test"},
    #     (40,50): {"label": "last_test", "context": False, "baseline_cov": "all_but_one", "human_cov": "base_coverage"},
    #     (50,60): {"label": "extra_test", "context": False, "baseline_cov": "base_coverage", "human_cov": "base_coverage"},
    # },
    "codegen-2B-multi_t0.2_n10": {
        (0,10): {"label": "first_test", "context": False, "baseline_cov": "preamble", "human_cov": "first_test"},
        (10,20): {"label": "last_test", "context": False, "baseline_cov": "all_but_one", "human_cov": "base_coverage"},
        (20,30): {"label": "extra_test", "context": False, "baseline_cov": "base_coverage", "human_cov": "base_coverage"},
    },
    "codegen-2B-multi_t0.2_n10_v2": {
        (0,10): {"label": "first_test", "context": False, "baseline_cov": "preamble", "human_cov": "first_test"},
        (10,20): {"label": "last_test", "context": False, "baseline_cov": "all_but_one", "human_cov": "base_coverage"},
        (20,30): {"label": "extra_test", "context": False, "baseline_cov": "base_coverage", "human_cov": "base_coverage"},
    },
    "codegen-16B-multi_t0.2_n10": {
        (0,10): {"label": "first_test", "context": False, "baseline_cov": "preamble", "human_cov": "first_test"},
        (10,20): {"label": "last_test", "context": False, "baseline_cov": "all_but_one", "human_cov": "base_coverage"},
        (20,30): {"label": "extra_test", "context": False, "baseline_cov": "base_coverage", "human_cov": "base_coverage"},
    },
    "codegen-2B-mono_t0.2_n10": {
        (0,10): {"label": "first_test", "context": False, "baseline_cov": "preamble", "human_cov": "first_test"},
        (10,20): {"label": "last_test", "context": False, "baseline_cov": "all_but_one", "human_cov": "base_coverage"},
        (20,30): {"label": "extra_test", "context": False, "baseline_cov": "base_coverage", "human_cov": "base_coverage"},
    },
    "codegen-16B-mono_t0.2_n10": {
        (0,10): {"label": "first_test", "context": False, "baseline_cov": "preamble", "human_cov": "first_test"},
        (10,20): {"label": "last_test", "context": False, "baseline_cov": "all_but_one", "human_cov": "base_coverage"},
        (20,30): {"label": "extra_test", "context": False, "baseline_cov": "base_coverage", "human_cov": "base_coverage"},
    },
}


def check_test(generated_test):
    return True if "assert" in generated_test or "Assert" in generated_test or "then()" in generated_test or "expect" in generated_test or "verify" in generated_test or "fail" in generated_test else False


def get_baselines_obj(projs_data, language):
    baselines_obj = {}
    for org in projs_data:
        baselines_obj[org] = {}
        for proj in projs_data[org]:
            baselines_obj[org][proj] = {}
            proj_data = projs_data[org][proj]
            for i, (source_fn, test_fn) in enumerate(proj_data):
                results_file = os.path.join(aggregation_dir, language, "results", f"{org}____{proj}_v2.json")
                if os.path.exists(results_file):    
                    with open(results_file, "r") as f:
                        proj_info = json.load(f)
                        log_key = f"{source_fn}____{test_fn}"
                        if log_key in proj_info:
                            baselines_obj[org][proj][log_key] = {}
                            file_pair_data = proj_info[log_key]
                            for label in file_pair_data:  
                                results = file_pair_data[label]             
                                for baseline_label in BASELINE_LABELS:
                                    if baseline_label in label:
                                        baselines_obj[org][proj][log_key][baseline_label] = (results["status"], results["line_coverage"])
    return baselines_obj


def compute_results(projs_data, language, aggregation_dir, generations_dir, preds_root):
    results_arr = ["Organization,Project,Source Filename,Test Filename,Filepair Index,Generation Path,Is Test,Setting,Mode,Context,Status,Coverage,Baseline Coverage,Human Coverage\n"]
    baselines_obj = get_baselines_obj(projs_data, language)

    for org in projs_data:
        for proj in projs_data[org]:
            proj_data = projs_data[org][proj]
            for i, (source_fn, test_fn) in enumerate(proj_data):
                results_file = os.path.join(aggregation_dir, language, "results", f"{org}____{proj}_v2.json")    
                if os.path.exists(results_file):
                    with open(results_file, "r") as f:
                        proj_info = json.load(f)
                        log_key = f"{source_fn}____{test_fn}"
                        if log_key in proj_info:
                            file_pair_data = proj_info[log_key]
                            num_tests = len(os.listdir(os.path.join(generations_dir, language, org, proj, f"filepair{i}", "incremental_test_files")))
                            for setting in mapping:
                                preds_path = os.path.join(preds_root, f"{language}_{setting}_filepairs_preds.json")
                                if os.path.exists(preds_path):
                                    with open(preds_path, "r") as f:
                                        preds = json.load(f)

                                ranges = mapping[setting]
                                for curr_range, metadata in ranges.items():
                                    if num_tests <= 1 and metadata["label"] == "last_test":
                                        continue
                                    for n in range(curr_range[0], curr_range[1]):
                                        label = f"{setting}_{n}"
                                        if label in file_pair_data:
                                            results = file_pair_data[label]
                                            test_prefix, ending = test_fn.rsplit("/", 1)[1].split(".")
                                            generation_path = os.path.join(generations_dir, language, org, proj, f"filepair{i}", setting, f"{test_prefix}__v2n{n}.{ending}")
                                            pred_test = preds[org][proj][str(i)][str(n)]
                                            is_test = check_test(pred_test)
                                            baseline_cov = baselines_obj[org][proj][log_key][metadata["baseline_cov"]][1] if metadata["baseline_cov"] in baselines_obj[org][proj][log_key] else ""
                                            baseline_cov = "" if baseline_cov == "NOT FOUND" else baseline_cov
                                            human_cov = baselines_obj[org][proj][log_key][metadata["human_cov"]][1] if metadata["human_cov"] in baselines_obj[org][proj][log_key] else ""
                                            human_cov = "" if human_cov == "NOT FOUND" else human_cov
                                            if human_cov == "" or baseline_cov == "":
                                                continue
                                            results_arr.append(",".join([org, proj, source_fn, test_fn, str(i), generation_path, str(is_test), setting, metadata["label"], str(metadata["context"]), results["status"], str(results["line_coverage"]), str(baseline_cov), str(human_cov)]) + "\n")

    return results_arr


if __name__ == '__main__':
    filepair_dir = sys.argv[1] if len(sys.argv) > 1 else '/data/GitHubMining/TestFramework/'
    generations_dir = sys.argv[2] if len(sys.argv) > 2 else '/data/GitHubMining/Generated_TestOutputs/'
    aggregation_dir = sys.argv[3] if len(sys.argv) > 1 else '/data/GitHubMining/TestFramework/TestingLLM'
    preds_root = sys.argv[4] if len(sys.argv) > 4 else '/data/GitHubMining/TextMetrics/TestGeneration'

    with open(os.path.join(filepair_dir, "java_filepairs.json"), "r") as f:
        java_data = json.load(f)
    
    with open(os.path.join(filepair_dir, "python_filepairs.json"), "r") as f:
        python_data = json.load(f)

    java_results = compute_results(java_data, "java", aggregation_dir, generations_dir, preds_root)
    python_results = compute_results(python_data, "python", aggregation_dir, generations_dir, preds_root)
    
    with open(os.path.join(aggregation_dir, "java_coverage_results_v2.csv"), "w") as f:
        f.writelines(java_results)

    with open(os.path.join(aggregation_dir, "python_coverage_results_v2.csv"), "w") as f:
        f.writelines(python_results)

    
import sys
import os
import json

def val_to_percent(val, ct, total):
    if ct == 0:
        return f"0% (0/{total})"
    percent = round(val * 100, 2)
    return f"{percent}% ({ct}/{total})"

def average_to_percent(val, total):
    if total == 0:
        return f"N/A (0)"
    percent = round(val * 100, 2)
    return f"{percent}% ({total})"

def dataset_stats_to_csv(dataset_json, covs_json):
    text = "Setting,Evaluation Mode,Has Context,Total,Unique,W/Asserts, Compile, Pass,Baseline Cov (%),Cov Imp (Model) (%),Cov Imp (Human) (%),Cov Imp (Model) - 0% (%),Cov Imp (Human) - 0% (%)\n"
    for key in dataset_json:
        setting, eval_mode, has_context = key.split(",")
        stats = dataset_json[key]
        num_examples_per_fp = int(setting.split("_n")[1])
        if eval_mode == "last_test":
            total_examples = covs_json["last_test_total"] * num_examples_per_fp
        elif eval_mode == "first_test":
            total_examples = covs_json["first_test_total"] * num_examples_per_fp
        else:
            total_examples = covs_json["extra_test_total"] * num_examples_per_fp

        cov_improvement_model = average_to_percent(stats['all_cov_improvement'], stats['all_cov_examples'])
        cov_improvement_human = average_to_percent(stats['all_human_cov_improvement'], stats['all_cov_examples'])
        baseline_cov = average_to_percent(stats['all_baseline_cov'], stats['all_cov_examples'])
        cov_improvement_model_no_zero = average_to_percent(stats['non_zero_cov_improvement'], stats['non_zero_cov_examples'])
        cov_improvement_human_no_zero = average_to_percent(stats['non_zero_human_cov_improvement'], stats['non_zero_cov_examples'])


        text += f"{setting},{eval_mode},{has_context},{total_examples},{stats['num_examples']},{stats['total']},{stats['compiling']},{stats['passing']},{baseline_cov},{cov_improvement_model},{cov_improvement_human},{cov_improvement_model_no_zero},{cov_improvement_human_no_zero}\n"
    
    return text


if __name__ == '__main__':
    input_json = sys.argv[1] if len(sys.argv) > 1 else '/data/GitHubMining/TestFramework/TestingLLM/java/asserts_completion_metrics_ds.json'
    data_json = sys.argv[2] if len(sys.argv) > 2 else '/data/GitHubMining/TestFramework/TestingLLM/java/completion_baseline_covs.json'
    output_csv = sys.argv[3] if len(sys.argv) > 3 else '/data/GitHubMining/TestFramework/TestingLLM/java/asserts_completion_metrics_ds.csv'

    with open(input_json, "r") as f:
        data = json.load(f)

    with open(data_json, "r") as f:
        covs = json.load(f)

    text = dataset_stats_to_csv(data, covs)
    with open(output_csv, "w") as f:
        f.write(text)

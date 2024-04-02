import sys
import json

FILEPAIR_RANGES = {(0,10):"context_first_test", (10,20): "context_last_test", (30,40): "no_context_first_test", (40,50): "no_context_last_test"}
CODEGEN_RANGES = {(0,10):"no_context_first_test", (10,20): "no_context_last_test"}

def compute_average(dict_list):
    mean_dict = {}
    for key in dict_list[0].keys():
        mean_dict[key] = sum(d[key] for d in dict_list) / len(dict_list)
    return mean_dict

def aggregate_metrics(metrics, ranges):
    aggregate_metrics = {}
    for org in metrics:
        aggregate_metrics[org] = {}
        for project in metrics[org]:
            aggregate_metrics[org][project] = {}
            for ind in metrics[org][project]:
                aggregate_metrics[org][project][ind] = {}
                for start, end in ranges:
                    mode = ranges[(start, end)]
                    print("HERE")
                    print(mode)
                    mode_arr = []
                    for i in range(start, end):
                        if str(i) in metrics[org][project][ind]:
                            mode_arr.append(metrics[org][project][ind][str(i)])
                    if len(mode_arr) > 0:
                        aggregate_metrics[org][project][str(ind)][mode] = compute_average(mode_arr)

    print(aggregate_metrics)
    aggregate_proj = {}

    for org in aggregate_metrics:
        aggregate_proj[org] = {}
        for project in aggregate_metrics[org]:
            aggregate_proj[org][project] = {}
            for ind in aggregate_metrics[org][project]:
                for mode in aggregate_metrics[org][project][ind]:
                    if mode not in aggregate_proj[org][project]:
                        aggregate_proj[org][project][mode] = []
                    aggregate_proj[org][project][mode].append(aggregate_metrics[org][project][ind][mode])

            for mode in aggregate_proj[org][project]:
                aggregate_proj[org][project][mode] = compute_average(aggregate_proj[org][project][mode])
    

    aggregate_ds = {}
    
    for org in aggregate_proj:
        for project in aggregate_proj[org]:
            for mode in aggregate_proj[org][project]:
                if mode not in aggregate_ds:
                    aggregate_ds[mode] = []
                aggregate_ds[mode].append(aggregate_proj[org][project][mode])
    
    for mode in aggregate_ds:
        aggregate_ds[mode] = compute_average(aggregate_ds[mode])
    
    return aggregate_ds


if __name__ == "__main__":
    metrics_path = sys.argv[1] if len(sys.argv) > 1 else "/data/GitHubMining/TextMetrics/TestGeneration/java_0.2_10_metrics.json"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "/data/GitHubMining/TextMetrics/TestGeneration/java_0.2_10_aggregated_metrics.json"
    is_codegen = sys.argv[3] if len(sys.argv) > 3 else "no"

    ranges = FILEPAIR_RANGES if is_codegen == "no" else CODEGEN_RANGES
    with open(metrics_path, 'r') as json_file:
        metrics = json.load(json_file)

    aggregate_metrics_data = aggregate_metrics(metrics, ranges)
    with open(output_path, 'w') as json_file:
        json.dump(aggregate_metrics_data, json_file, indent=4)

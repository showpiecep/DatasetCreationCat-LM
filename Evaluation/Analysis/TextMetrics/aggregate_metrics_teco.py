import sys
import json

TECO_RANGES = {(0,10):"context", (10,20): "no_context"}

def compute_average(dict_list):
    mean_dict = {}
    for key in dict_list[0].keys():
        mean_dict[key] = sum(d[key] for d in dict_list) / len(dict_list)
    return mean_dict

def aggregate_metrics(metrics):
    aggregate_metrics = {}
    for ind in metrics:
        aggregate_metrics[ind] = {}
        for start, end in TECO_RANGES:
            mode = TECO_RANGES[(start, end)]
            mode_arr = []
            for i in range(start, end):
                if str(i) in metrics[ind]:
                    mode_arr.append(metrics[ind][str(i)])
            aggregate_metrics[ind][mode] = compute_average(mode_arr)

    aggregate_modes = {}

    for ind in aggregate_metrics:
        for mode in aggregate_metrics[ind]:
            if mode not in aggregate_modes:
                aggregate_modes[mode] = []
            aggregate_modes[mode].append(aggregate_metrics[ind][mode])
    
    for mode in aggregate_modes:
        aggregate_modes[mode] = compute_average(aggregate_modes[mode])
    
    return aggregate_modes


if __name__ == "__main__":
    metrics_path = sys.argv[1] if len(sys.argv) > 1 else "/data/GitHubMining/TextMetrics/Teco/teco_metrics_0.8.json"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "/data/GitHubMining/TextMetrics/Teco/teco_aggregated_metrics_0.8.json"

    with open(metrics_path, 'r') as json_file:
        metrics = json.load(json_file)

    aggregate_metrics_data = aggregate_metrics(metrics)
    with open(output_path, 'w') as json_file:
        json.dump(aggregate_metrics_data, json_file)

import sys
import json

JAVA_JSONS = {
    "/data/GitHubMining/TextMetrics/TestGeneration/java_t0.2_n10_aggregated_metrics.json": "CAT-LM (0.2)",
    "/data/GitHubMining/TextMetrics/TestGeneration/java_t0.8_n10_aggregated_metrics.json": "CAT-LM (0.8)", 
    "/data/GitHubMining/TextMetrics/TestGeneration/java_codegen-2B-multi_t0.2_n10_aggregated_metrics.json": "Codegen 2B (0.2)",
    "/data/GitHubMining/TextMetrics/TestGeneration/java_codegen-16B-multi_t0.2_n10_aggregated_metrics.json": "Codegen 16B (0.2)",
}

PYTHON_JSONS = {
    "/data/GitHubMining/TextMetrics/TestGeneration/python_t0.2_n10_aggregated_metrics.json": "CAT-LM (0.2)",
    "/data/GitHubMining/TextMetrics/TestGeneration/python_t0.8_n10_aggregated_metrics.json": "\\CAT-LM (0.8)",
    "/data/GitHubMining/TextMetrics/TestGeneration/python_codegen-2B-multi_t0.2_n10_aggregated_metrics.json": "Codegen 2B Multi (0.2)",
    "/data/GitHubMining/TextMetrics/TestGeneration/python_codegen-16B-multi_t0.2_n10_aggregated_metrics.json": "Codegen 16B Multi (0.2)",
    "/data/GitHubMining/TextMetrics/TestGeneration/python_codegen-2B-mono_t0.2_n10_aggregated_metrics.json": "Codegen 2B Mono (0.2)",
    "/data/GitHubMining/TextMetrics/TestGeneration/python_codegen-16B-mono_t0.2_n10_aggregated_metrics.json": "Codegen 16B Mono (0.2)",
}

def round_data(d):
    return round(d, 2)

if __name__ == "__main__":
    java_csv = "/data/GitHubMining/TextMetrics/TestGeneration/java_metrics.csv"
    python_csv = "/data/GitHubMining/TextMetrics/TestGeneration/python_metrics.csv"

    java_csv_cols = "Model,Temperature,Context (True/False),Test Case,CodeBLEU,BLEU,XMatch,EditSim,Rouge-F,Rouge-P,Rouge-R\n"
    for json_file in JAVA_JSONS:
        label = JAVA_JSONS[json_file]
        model = label.split(" (")[0]
        temp = label.split(" (")[1].split(")")[0]
        with open(json_file, 'r') as json_file:
            java_data = json.load(json_file)
        for mode in java_data:
            mode_data = java_data[mode]
            context = False if "no_context" in mode else "True"
            test_case = " ".join(mode.split("context_")[1].split("_")).title()
            java_csv_cols += f"{model},{temp},{context},{test_case},{round_data(mode_data['code_bleu'])}%,{round_data(mode_data['bleu'])}%,{round_data(mode_data['xmatch'])}%,{round_data(mode_data['edit_sim'])}%,{round_data(mode_data['rouge_f'])}%,{round_data(mode_data['rouge_p'])}%,{round_data(mode_data['rouge_r'])}%\n"

    python_csv_cols = "Model,Temperature,Context (True/False),Test Case,CodeBLEU,BLEU,XMatch,EditSim,Rouge-F,Rouge-P,Rouge-R\n"
    for json_file in PYTHON_JSONS:
        label = PYTHON_JSONS[json_file]
        model = label.split(" (")[0]
        temp = label.split(" (")[1].split(")")[0]
        with open(json_file, 'r') as json_file:
            python_data = json.load(json_file)
        for mode in python_data:
            mode_data = python_data[mode]
            context = False if "no_context" in mode else "True"
            test_case = " ".join(mode.split("context_")[1].split("_")).title()
            python_csv_cols += f"{model},{temp},{context},{test_case},{round_data(mode_data['code_bleu'])}%,{round_data(mode_data['bleu'])}%,{round_data(mode_data['xmatch'])}%,{round_data(mode_data['edit_sim'])}%,{round_data(mode_data['rouge_f'])}%,{round_data(mode_data['rouge_p'])}%,{round_data(mode_data['rouge_r'])}%\n"

    with open(java_csv, 'w') as csv_file:
        csv_file.write(java_csv_cols)

    with open(python_csv, 'w') as csv_file:
        csv_file.write(python_csv_cols)
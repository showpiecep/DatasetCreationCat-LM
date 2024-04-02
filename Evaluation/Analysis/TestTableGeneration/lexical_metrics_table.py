import json

table_template = """\\begin{table*}[ht]
{\\small
\\begin{center}
\\centering
\\caption{Lexical metrics performance comparison of the models on the held-out test set for Java and Python.}
\\label{tab:codegenlexical}
\\begin{tabular}{ll|rrr|rrr}
\\toprule
 & & \\multicolumn{3}{c|}{\\textbf{Java Lexical Metrics}} & \\multicolumn{3}{c}{\\textbf{Python Lexical Metrics}} \\\\\\toprule
\\textbf{Model} & \\textbf{Context}  & \\textbf{CodeBLEU} & \\textbf{XMatch} & \\textbf{Rouge} & \\textbf{CodeBLEU} & \\textbf{XMatch} & \\textbf{Rouge} \\\\ \\midrule
\\multicolumn{8}{c}{\\textbf{First Test}} \\\\\\midrule
\\tool & With & 41.93\\% & 16.0\\% & 60.77\\% & 17.24\\% & 0.12\\% & 31.32\\% \\\\
\\tool & Without & 26.68\\% & 0.0\\% & 49.14\\% & 19.80\\% & 0.0\\% & 28.99\\% \\\\
Codegen 2B & N/A & 34.09\\% & 7.69\\% & 54.76\\% & 14.74\\% & 0.0\\% & 26.68\\%  \\\\
Codegen 16B & N/A & 40.12\\% & 7.69\\% & 58.16\\% & -- & -- & -- \\\\\\midrule
\\multicolumn{8}{c}{\\textbf{Last Test}} \\\\\\midrule
\\tool & With & 41.84\\% & 2.38\\% & 59.39\\% & 35.98\\% & 2.94\\% & 50.81\\% \\\\
\\tool & Without & 38.52\\% & 0.0\\% & 59.58\\% & 31.96\\% & 0.0\\% & 51.19\\% \\\\
Codegen 2B & N/A & 35.2\\% & 4.35\\% & 47.01\\% & 34.78\\% & 3.87\\% & 48.88\\%\\\\
Codegen 16B & N/A & 34.84\\% & 5.95\\% & 45.31\\% & -- & -- & -- \\\\ \\bottomrule
\\end{tabular}
\\end{center}}
\\end{table*}"""


curr_table = """\\begin{table*}[ht]
{\\small
\\begin{center}
\\centering
\\caption{Lexical metrics performance comparison of the models on the held-out test set for Java and Python. BLEU, Edit Similarity, Rouge-P and Rouge-R scores are in Appendix \\Cref{sec:appendixlexicaltestgen}. We only report lexical metrics for our first test and last test
settings, as there is no gold test to compare against in our extra test setting.}
\\label{tab:codegenlexical}
\\begin{tabular}{ll|rrr|rrr}
\\toprule
 & & \\multicolumn{3}{c|}{\\textbf{Java Lexical Metrics}} & \\multicolumn{3}{c}{\\textbf{Python Lexical Metrics}} \\\\\\toprule
\\textbf{Model} & \\textbf{Context}  & \\textbf{CodeBLEU} & \\textbf{XMatch} & \\textbf{Rouge} & \\textbf{CodeBLEU} & \\textbf{XMatch} & \\textbf{Rouge} \\\\ \\midrule
\\multicolumn{8}{c}{\\textbf{First Test}} \\\\\\midrule
"""

table_suffix = """\\bottomrule
\\end{tabular}
\\end{center}}
\\end{table*}
"""

file_mapping = {
    "\\tool": (
        "/data/GitHubMining/TextMetrics/TestGeneration/java_t0.2_n10_v2_aggregated_metrics.json",
        "/data/GitHubMining/TextMetrics/TestGeneration/python_t0.2_n10_aggregated_metrics.json"
    ),
    "Codegen-2B-multi": (
        "/data/GitHubMining/TextMetrics/TestGeneration/java_codegen-2B-multi_t0.2_n10_v2_aggregated_metrics.json",
        "/data/GitHubMining/TextMetrics/TestGeneration/python_codegen-2B-multi_t0.2_n10_aggregated_metrics.json"
    ),
    "Codegen-16B-multi": (
        "/data/GitHubMining/TextMetrics/TestGeneration/java_codegen-16B-multi_t0.2_n10_aggregated_metrics.json",
        "/data/GitHubMining/TextMetrics/TestGeneration/python_codegen-16B-multi_t0.2_n10_aggregated_metrics.json"
    ),
    "Codegen-2B-mono": "/data/GitHubMining/TextMetrics/TestGeneration/python_codegen-2B-mono_t0.2_n10_aggregated_metrics.json",
    "Codegen-16B-mono": "/data/GitHubMining/TextMetrics/TestGeneration/python_codegen-16B-mono_t0.2_n10_aggregated_metrics.json"
}


def get_metrics(data):
    return f"& {data['code_bleu']:.1f}\\% & {data['xmatch']:.1f}\\% & {data['rouge_f']:.1f}\\% "


def get_rows(file_data, is_first):
    rows = ""
    for toolname in file_data:
        if "mono" in toolname:
            python_data = file_data[toolname][0]
            if is_first:
                rows += f"{toolname} & N/A & "
                rows += " & ".join(["--"] * 3)
                rows += get_metrics(python_data["no_context_first_test"])
                rows += "\\\\\n"
            else:
                rows += f"{toolname} & N/A & "
                rows += " & ".join(["--"] * 3)
                rows += get_metrics(python_data["no_context_last_test"])
                rows += "\\\\\n"
            continue

        python_data, java_data= file_data[toolname]
        if is_first:
            if toolname == "\\tool":
                rows += f"{toolname} & With "
                rows += get_metrics(java_data["context_first_test"])
                rows += get_metrics(python_data["context_first_test"])
                rows += "\\\\\n"

                rows += f"{toolname} & Without "
                rows += get_metrics(java_data["no_context_first_test"])
                rows += get_metrics(python_data["no_context_first_test"])
                rows += "\\\\\n"
            else:
                rows += f"{toolname} & N/A "
                rows += get_metrics(java_data["no_context_first_test"])
                rows += get_metrics(python_data["no_context_first_test"])
                rows += "\\\\\n"
        else:
            if toolname == "\\tool":
                rows += f"{toolname} & With "
                rows += get_metrics(java_data["context_last_test"])
                rows += get_metrics(python_data["context_last_test"])
                rows += "\\\\\n"

                rows += f"{toolname} & Without "
                rows += get_metrics(java_data["no_context_last_test"])
                rows += get_metrics(python_data["no_context_last_test"])
                rows += "\\\\\n"
            else:
                rows += f"{toolname} & N/A "
                rows += get_metrics(java_data["no_context_last_test"])
                rows += get_metrics(python_data["no_context_last_test"])
                rows += "\\\\\n"
    return rows


if __name__ == "__main__":
    file_data = {}

    for toolname in file_mapping:
        file_data[toolname] = []
        if "mono" in toolname:
            python_file = file_mapping[toolname]
            with open(python_file, "r") as f:
                file_data[toolname].append(json.load(f))
            continue

        java_file, python_file = file_mapping[toolname]
        with open(java_file, "r") as f:
            file_data[toolname].append(json.load(f))
        
        with open(python_file, "r") as f:
            file_data[toolname].append(json.load(f))

    curr_table += get_rows(file_data, True)
    curr_table += "\\midrule\\multicolumn{8}{c}{\\textbf{Last Test}} \\\\\\midrule\n"
    curr_table += get_rows(file_data, False)
    curr_table += table_suffix

    print(curr_table)




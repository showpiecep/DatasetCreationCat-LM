import json

table_template = """\\begin{table*}[ht]
    {\\small 
    \\begin{center}
    \\centering
    \\caption{Lexical metrics performance comparison of our model vs CodeGen 2B and 16B on our held out test set for Java.}
    \\begin{tabular}{l|l|r|r|r|r|r|r|r}
    \\toprule
        \\textbf{Model} & \\textbf{Ctxt.} & \\textbf{CodeBLEU} & \\textbf{BLEU} & \\textbf{XMatch} & \\textbf{EditSim} & \\textbf{Rouge-F} & \\textbf{Rouge-P} & \\textbf{Rouge-R} \\\\
    \\midrule
    \\multicolumn{8}{c}{\\textbf{First Test}} \\\\\\midrule
        \\tool-0.2 & Y  & \\textbf{41.93}\\% & \\textbf{31.99\\%} & \\textbf{16.0\\%} & 40.68\\% & \\textbf{60.77\\%} & \\textbf{65.4\\%} & \\textbf{60.5\\%} \\\\ 
        \\tool-0.2 & N & 26.68\\% & 14.06\\% & 0.0\\% & 27.69\\% & 49.14\\% & 56.56\\% & 48.02\\% \\\\ 
        \\tool-0.8 & Y & 36.51\\% & 27.23\\% & 12.0\\% & 37.79\\% & 56.7\\% & 57.86\\% & 60.41\\% \\\\ 
         \\tool-0.8 & N & 23.14\\% & 12.93\\% & 0.0\\% & 23.76\\% & 45.31\\% & 47.36\\% & 49.11\\% \\\\ 
       \\multicolumn{2}{l|}{Codegen 2B} & 34.09\\% & 24.92\\% & 7.69\\% & 46.62\\% & 54.76\\% & 59.58\\% & 55.78\\% \\\\ 
       \\multicolumn{2}{l|}{Codegen 16B} & 40.12\\% & 30.85\\% & 7.69\\% & \\textbf{54.40\\%} & 58.16\\% & 62.25\\% & 58.83\\% \\\\ \\midrule
    \\multicolumn{8}{c}{\\textbf{Last Test}} \\\\\\midrule
        \\tool-0.2  & Y & \\textbf{41.84\\%} & \\textbf{33.31\\%} & 2.38\\% & 41.19\\% & 59.39\\% & 63.58\\% & 58.55\\% \\\\ 
         \\tool-0.2 & N & 38.52\\% & 29.43\\% & 0.0\\% & 37.98\\% & \\textbf{59.58\\%} & \\textbf{64.11\\%} & \\textbf{59.12\\%} \\\\  
        \\tool-0.8  & Y & 37.95\\% & 29.38\\% & 1.59\\% & 35.8\\% & 53.76\\% & 56.42\\% & 55.42\\% \\\\ 
         \\tool-0.8 & N & 39.68\\% & 30.11\\% & 0.0\\% & 39.44\\% & 57.66\\% & 61.98\\% & 58.08\\% \\\\ 
      \\multicolumn{2}{l|}{Codegen 2B} & 35.2\\% & 28.91\\% & 4.35\\% & \\textbf{45.90\\%} & 47.01\\% & 48.62\\% & 48.63\\% \\\\ 
        \\multicolumn{2}{l|}{Codegen 16B} & 34.84\\% & 27.94\\% & \\textbf{5.95\\%} & 44.97\\% & 45.31\\% & 49.31\\% & 44.42\\% \\\\ \\bottomrule

    \\end{tabular}
    \\end{center}}
\\end{table*}
"""


curr_table_python = """\\begin{table*}[ht]
    {\\small 
    \\begin{center}
    \\centering
    \\caption{Lexical metrics performance comparison of our model vs CodeGen baselines on our held out test set for Python. We report lexical metrics for \\tool both with and without context.}
    \\label{tab:supplementallexicalpython}
    \\begin{tabular}{l|r|r|r|r|r|r|r}
    \\toprule
        \\textbf{Model} & \\textbf{CodeBLEU} & \\textbf{BLEU} & \\textbf{XMatch} & \\textbf{EditSim} & \\textbf{Rouge-F} & \\textbf{Rouge-P} & \\textbf{Rouge-R} \\\\
    \\midrule
    \\multicolumn{8}{c}{\\textbf{First Test}} \\\\\\midrule
"""

curr_table_java = """\\begin{table*}[ht]
    {\\small 
    \\begin{center}
    \\centering
    \\caption{Lexical metrics performance comparison of our model vs CodeGen baselines on our held out test set for Java. We report lexical metrics for \\tool both with and without context.}
    \\label{tab:supplementallexicaljava}
    \\begin{tabular}{l|r|r|r|r|r|r|r}
    \\toprule
        \\textbf{Model} & \\textbf{CodeBLEU} & \\textbf{BLEU} & \\textbf{XMatch} & \\textbf{EditSim} & \\textbf{Rouge-F} & \\textbf{Rouge-P} & \\textbf{Rouge-R} \\\\
    \\midrule
    \\multicolumn{8}{c}{\\textbf{First Test}} \\\\\\midrule
"""

table_suffix = """\\bottomrule

    \\end{tabular}
    \\end{center}}
\\end{table*}
"""

file_mapping = {
    "\\tool": (
        "/data/GitHubMining/TextMetrics/TestGeneration/java_t0.2_n10_aggregated_metrics.json",
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
    return f"& {data['code_bleu']:.1f}\\% & {data['bleu']:.1f}\\% & {data['xmatch']:.1f}\\% & {data['edit_sim']:.1f}\\% & {data['rouge_f']:.1f}\\% & {data['rouge_p']:.1f}\\% & {data['rouge_r']:.1f}\\%"


def get_rows(file_data, is_first, is_python):
    rows = ""
    for toolname in file_data:
        if "mono" in toolname:
            if is_python:
                python_data = file_data[toolname][0]
                if is_first:
                    rows += f"{toolname} "
                    rows += get_metrics(python_data["no_context_first_test"])
                    rows += "\\\\\n"
                else:
                    rows += f"{toolname} "
                    rows += get_metrics(python_data["no_context_last_test"])
                    rows += "\\\\\n"
            continue


        python_data, java_data= file_data[toolname]
        if is_first:
            if "\\tool" in toolname:
                rows += f"{toolname} w Context "
                rows += get_metrics(python_data["context_first_test"]) if is_python else get_metrics(java_data["context_first_test"])
                rows += "\\\\\n"

                rows += f"{toolname} w/o Context "
                rows += get_metrics(python_data["no_context_first_test"]) if is_python else get_metrics(java_data["no_context_first_test"])
                rows += "\\\\\n"
            else:
                rows += f"{toolname} "
                rows += get_metrics(python_data["no_context_first_test"]) if is_python else get_metrics(java_data["no_context_first_test"])
                rows += "\\\\\n"
        else:
            if "\\tool" in toolname:
                rows += f"{toolname} w Context "
                rows += get_metrics(python_data["context_last_test"]) if is_python else get_metrics(java_data["context_last_test"])
                rows += "\\\\\n"

                rows += f"{toolname} w/o Context "
                rows += get_metrics(python_data["no_context_last_test"]) if is_python else get_metrics(java_data["no_context_last_test"])
                rows += "\\\\\n"
            else:
                rows += f"{toolname} "
                rows += get_metrics(python_data["no_context_last_test"]) if is_python else get_metrics(java_data["no_context_last_test"])
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

    curr_table_python += get_rows(file_data, True, True)
    curr_table_python += "\\midrule\\multicolumn{8}{c}{\\textbf{Last Test}} \\\\\\midrule\n"
    curr_table_python += get_rows(file_data, False, True)
    curr_table_python += table_suffix

    print(curr_table_python)

    curr_table_java += get_rows(file_data, True, False)
    curr_table_java += "\\midrule\\multicolumn{8}{c}{\\textbf{Last Test}} \\\\\\midrule\n"
    curr_table_java += get_rows(file_data, False, False)
    curr_table_java += table_suffix

    print(curr_table_java)




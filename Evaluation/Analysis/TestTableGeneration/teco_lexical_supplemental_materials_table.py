import json

teco_table = """\\begin{table*}[ht]
 {\\small 
 \\begin{center}
\\centering
\\caption{Comparison against TeCo (all temperatures)}
\\begin{tabular}{l|l|r|r|r|r|r|r|r}
\\toprule
\\textbf{Model} & \\textbf{Context} & \\textbf{CodeBLEU} & \\textbf{BLEU} & \\textbf{XMatch} & \\textbf{EditSim} & \\textbf{Rouge-F} & \\textbf{Rouge-P} & \\textbf{Rouge-R} \\\\
\\midrule
\\tool-0.2 & Y & \\textbf{66.48\\%} & \\textbf{68.54\\%} & \\textbf{49.62\\%} & \\textbf{80.74\\%} & \\textbf{82.46\\%} & \\textbf{82.60\\%} & \\textbf{83.91\\%} \\\\
\\tool-0.2 & N & 65.14\\% & 67.21\\% & 47.92\\% & 79.91\\% & 81.79\\% & 82.11\\% & 83.13\\% \\\\
\\tool-0.8 & Y & 56.74\\% & 59.55\\% & 38.11\\% & 74.37\\% & 76.66\\% & 76.47\\% & 78.93\\% \\\\
\\tool-0.8 & N & 55.88\\% & 58.70\\% & 36.19\\% & 74.09\\% & 75.97\\% & 76.02\\% & 78.04\\% \\\\
\\multicolumn{2}{l|}{TeCo} & 34.98\\% & 39.97\\% & 13.80\\% & 62.98\\% & 60.16\\% & 58.98\\% & 64.62\\% \\\\ \\bottomrule
\\end{tabular}
\\end{center}
}
\\end{table*}
"""

curr_table = """\\begin{table*}[ht]
 {\\small 
 \\begin{center}
\\centering
\\caption{Comparison of TeCo vs \\tool both with and without context across all lexical metrics.}
\\label{tab:supplementarylexicalteco}
\\begin{tabular}{l|r|r|r|r|r|r|r}
\\toprule
\\textbf{Model} & \\textbf{CodeBLEU} & \\textbf{BLEU} & \\textbf{XMatch} & \\textbf{EditSim} & \\textbf{Rouge-F} & \\textbf{Rouge-P} & \\textbf{Rouge-R} \\\\
\\midrule
"""

table_suffix = """\\bottomrule
\\end{tabular}
\\end{center}
}
\\end{table*}
"""


file_mapping = {
    "\\tool": "/data/GitHubMining/TextMetrics/Teco/teco_aggregated_metrics_0.2.json",
    "TeCo": "/code/teco/_work/exp/CSNm/eval-any-stmt/test/SingleEvaluator-teco-norr/bs10-last/metrics_summary.json"
}

if __name__ == "__main__":
    file_data = {}

    for toolname in file_mapping:
        file_data[toolname] = json.load(open(file_mapping[toolname]))


    for toolname in file_data:
        if "\\tool" in toolname:
            context_data = file_data[toolname]["context"]
            no_context_data = file_data[toolname]["no_context"]
            curr_table += f"{toolname} w Context & {context_data['code_bleu']:.1f}\\% & {context_data['bleu']:.1f}\\% & {context_data['xmatch']:.1f}\\% & {context_data['edit_sim']:.1f}\\% & {context_data['rouge_f']:.1f}\\% & {context_data['rouge_p']:.1f}\\% & {context_data['rouge_r']:.1f}\\% \\% \\\\\n"
            curr_table += f"{toolname} w/o Context & {no_context_data['code_bleu']:.1f}\\% & {no_context_data['bleu']:.1f}\\% & {no_context_data['xmatch']:.1f}\\% & {no_context_data['edit_sim']:.1f}\\% & {no_context_data['rouge_f']:.1f}\\% & {no_context_data['rouge_p']:.1f}\\% & {no_context_data['rouge_r']:.1f}\\% \\% \\\\\n"
        else:
            curr_table += f"{toolname}  & {file_data[toolname]['code-bleu-avg']:.1f}\\% & {file_data[toolname]['bleu-avg']:.1f}\\% & {file_data[toolname]['xmatch']:.1f}\\% & {file_data[toolname]['edit-sim-avg']:.1f}\\% & {file_data[toolname]['rouge-f-avg']:.1f}\\% & {file_data[toolname]['rouge-p-avg']:.1f}\\% & {file_data[toolname]['rouge-r-avg']:.1f}\\% \\% \\\\\n"

    curr_table += table_suffix

    print(curr_table)
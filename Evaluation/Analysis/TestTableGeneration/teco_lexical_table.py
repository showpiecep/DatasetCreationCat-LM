import json

teco_table = """\\begin{table}[ht]
{\\small
\\begin{center}
\\centering
\\caption{Comparison of \\tool and TeCo on selected lexical metrics on 1000 randomly sampled statements in their test set. All rows with \\tool have a temperature of 0.2.}
\\label{tab:lexicalteco}
\\begin{tabular}{l|l|r|r|r}
\\toprule
\\textbf{Model} & \\textbf{Context} & \\textbf{CodeBLEU} & \\textbf{XMatch} & \\textbf{Rouge} \\\\
\\midrule
TeCo & N/A & 34.98\\% & 13.8\\% & 60.16\\% \\\\
\\tool & Without & 65.14\\% & 47.92\\% & 81.79\\% \\\\
\\tool & With & \\textbf{66.48\\%} & \\textbf{49.62\\%} & \\textbf{82.46\\%} \\\\
\\bottomrule
\\end{tabular}
\\end{center}
}
\\end{table}
"""

curr_table = """\\begin{table}[ht]
{\\small
\\begin{center}
\\centering
\\caption{Comparison of \\tool and TeCo on 1000 randomly sampled statements in their test set.}
\\label{tab:lexicalteco}
\\begin{tabular}{l|r|r|r}
\\toprule
\\textbf{Model} & \\textbf{CodeBLEU} & \\textbf{XMatch} & \\textbf{Rouge} \\\\
\\midrule
"""

table_suffix = """\\bottomrule
\\end{tabular}
\\end{center}
}
\\end{table}"""


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
            curr_table += f"\\tool w Context & {context_data['code_bleu']:.1f}\\% & {context_data['xmatch']:.1f}\\% & {context_data['rouge_f']:.1f}\\% \\\\\n"
            curr_table += f"\\tool w/o Context & {no_context_data['code_bleu']:.1f}\\% & {no_context_data['xmatch']:.1f}\\% & {no_context_data['rouge_f']:.1f}\\% \\\\\n"
        else:
            curr_table += f"{toolname} & {file_data[toolname]['code-bleu-avg']:.1f}\\% & {file_data[toolname]['xmatch']:.1f}\\% & {file_data[toolname]['rouge-f-avg']:.1f}\\% \\\\\n"

    curr_table += table_suffix

    print(curr_table)
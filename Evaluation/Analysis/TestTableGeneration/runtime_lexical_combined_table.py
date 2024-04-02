import json

template = """
\\begin{table*}
{\\small
\\begin{center}
\\centering
\\caption{Lexical and runtime metrics performance comparison of the models on the held-out test set for Java and Python. We only report lexical metrics for our first test and last test settings, as there is no gold test to compare against in our extra test setting.}
\\label{tab:codegenlexical}
\\begin{tabular}{@{}l|rrr|rr|rrr|rr@{}}
\\toprule
 & \\multicolumn{5}{c|}{\\textbf{Java}} & \\multicolumn{5}{c}{\\textbf{Python }} \\\\\\toprule
 
 & \\multicolumn{3}{c|}{\\textbf{Lexical Metrics}} & \\multicolumn{2}{c|}{\\textbf{Runtime Metrics}} & \\multicolumn{3}{c|}{\\textbf{Lexical Metrics}} & \\multicolumn{2}{c}{\\textbf{Runtime Metrics}} \\\\\\toprule

\\textbf{Model} & \\textbf{CodeBLEU} & \\textbf{XMatch} & \\textbf{Rouge} &  \\textbf{Compile} & \\textbf{Pass} & \\textbf{CodeBLEU} & \\textbf{XMatch} & \\textbf{Rouge} & \\textbf{Compile} & \\textbf{Pass} \\\\ \\midrule

\\multicolumn{11}{c}{\\textbf{First Test (Total: Java = x, Python = x)}} \\\\\\midrule
\\tool w context  & \\textbf{}\\% & \\% & \\textbf{\\%} & & & \\textbf{\\%} & \\textbf{\\%} & \\textbf{\\%} & &  \\\\
\\tool w/o context &\\% & \\% & \\% & & & \\% & \\% & \\% & & \\\\
Codegen-2B-multi& \\% & \\% & \\% & & & \\% & \\% & \\% & & \\\\
Codegen-16B-multi & \\% & \\% & \\% & \\% & \\% & \\% \\\\
Codegen-2B-mono & -- & -- & --& \\% & \\% & \\% \\\\
Codegen-16B-mono  & -- & -- & --& \\% & \\% & \\% \\\\
\\midrule\\multicolumn{11}{c}{\\textbf{Last Test}} \\\\\\midrule
\\tool & \\textbf{\\%} & \\% & \\textbf{\\%} & \\% & \\textbf{\\%} & \\textbf{\\%} \\\\
\\tool & \\% & \\% & \\% & \\% & \\% & \\% \\\\
Codegen-2B-multi & \\% & \\% & \\% & \\% & \\% & \\% \\\\
Codegen-16B-multi& \\% & \\textbf{\\%} & \\% & \\textbf{\\%} & \\% & \\% \\\\
Codegen-2B-mono  & -- & -- & --& \\% & \\% & \\% \\\\
Codegen-16B-mono & -- & -- & --& \\% & \\% & \\% \\\\
\\midrule\\multicolumn{11}{c}{\\textbf{Extra Test}} \\\\\\midrule
\\tool & \\textbf{\\%} & \\% & \\textbf{\\%} & \\% & \\textbf{\\%} & \\textbf{\\%} \\\\
\\tool & \\% & \\% & \\% & \\% & \\% & \\% \\\\
Codegen-2B-multi & \\% & \\% & \\% & \\% & \\% & \\% \\\\
Codegen-16B-multi& \\% & \\textbf{\\%} & \\% & \\textbf{\\%} & \\% & \\% \\\\
Codegen-2B-mono  & -- & -- & --& \\% & \\% & \\% \\\\
Codegen-16B-mono & -- & -- & --& \\% & \\% & \\% \\\\
\\bottomrule
\\end{tabular}
\\end{center}}
\\end{table*}
"""

table_prefix = """
\\begin{table*}
{\\small
\\begin{center}
\\centering
\\caption{Lexical and runtime metrics performance comparison of the models on the held-out test set for Java and Python. We only report lexical metrics for our first test and last test settings, as there is no gold test to compare against in our extra test setting.}
\\label{tab:codegenlexical}
\\begin{tabular}{@{}l|rrr|rr|rrr|rr@{}}
\\toprule
 & \\multicolumn{5}{c|}{\\textbf{Java}} & \\multicolumn{5}{c}{\\textbf{Python }} \\\\\\toprule
 
 & \\multicolumn{3}{c|}{\\textbf{Lexical Metrics}} & \\multicolumn{2}{c|}{\\textbf{Runtime Metrics}} & \\multicolumn{3}{c|}{\\textbf{Lexical Metrics}} & \\multicolumn{2}{c}{\\textbf{Runtime Metrics}} \\\\\\toprule

\\textbf{Model} & \\textbf{CodeBLEU} & \\textbf{XMatch} & \\textbf{Rouge} &  \\textbf{Compile} & \\textbf{Pass} & \\textbf{CodeBLEU} & \\textbf{XMatch} & \\textbf{Rouge} & \\textbf{Compile} & \\textbf{Pass} \\\\ \\midrule

\\multicolumn{11}{c}{\\textbf{First Test (Total: Java = 270, Python = 1120)}} \\\\\\midrule
"""

table_suffix = """\\bottomrule
\\end{tabular}
\\end{center}}
\\end{table*}
"""

lexical_mapping = {
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



def add_row(python_runtime_data, java_runtime_data, python_lexical_data, java_lexical_data, tool):
    curr_row =  f"{tool} & {java_lexical_data['code_bleu']:.1f}\\% & {java_lexical_data['xmatch']:.1f}\\% & {java_lexical_data['rouge_f']:.1f}\\% & {java_runtime_data['compiling']} & {java_runtime_data['passing']}"
    curr_row +=  f" & {python_lexical_data['code_bleu']:.1f}\\% & {python_lexical_data['xmatch']:.1f}\\% & {python_lexical_data['rouge_f']:.1f}\\% & {python_runtime_data['compiling']} & {python_runtime_data['passing']} \\\\\n"
    return curr_row

def add_mono_row(python_runtime_data, python_lexical_data, tool):
    curr_row =  f"{tool} & -- & -- & -- & -- & -- "
    curr_row +=  f" & {python_lexical_data['code_bleu']:.1f}\\% & {python_lexical_data['xmatch']:.1f}\\% & {python_lexical_data['rouge_f']:.1f}\\% & {python_runtime_data['compiling']} & {python_runtime_data['passing']} \\\\\n"
    return curr_row

def add_extra_test_row(python_runtime_data, java_runtime_data, tool):
    curr_row =  f"{tool} & -- & -- & -- & {java_runtime_data['compiling']} & {java_runtime_data['passing']}"
    curr_row +=  f" & -- & -- & -- & {python_runtime_data['compiling']} & {python_runtime_data['passing']} \\\\\n"
    return curr_row

def add_extra_test_mono_row(python_runtime_data, tool):
    curr_row =  f"{tool} & -- & -- & -- & -- & -- "
    curr_row +=  f" & -- & -- & -- & {python_runtime_data['compiling']} & {python_runtime_data['passing']} \\\\\n"
    return curr_row

if __name__ == "__main__":
    java_ds = json.load(open("/data/GitHubMining/TestFramework/TestingLLM/java/asserts_completion_metrics_ds.json", "r"))
    python_ds = json.load(open("/data/GitHubMining/TestFramework/TestingLLM/python/asserts_completion_metrics_ds.json", "r"))

    lexical_data = {}

    for toolname in lexical_mapping:
        lexical_data[toolname] = []
        if "mono" in toolname:
            python_file = lexical_mapping[toolname]
            with open(python_file, "r") as f:
                lexical_data[toolname].append(json.load(f))
            continue

        java_file, python_file = lexical_mapping[toolname]
        with open(java_file, "r") as f:
            lexical_data[toolname].append(json.load(f))
        
        with open(python_file, "r") as f:
            lexical_data[toolname].append(json.load(f))

    table_prefix += add_row(python_ds["t0.2_n10,first_test,True"], java_ds["t0.2_n10,first_test,True"], lexical_data["\\tool"][1]["context_first_test"], lexical_data["\\tool"][0]["context_first_test"], "\\tool w Context")
    table_prefix += add_row(python_ds["t0.2_n10,first_test,False"], java_ds["t0.2_n10,first_test,False"], lexical_data["\\tool"][1]["no_context_first_test"], lexical_data["\\tool"][0]["no_context_first_test"], "\\tool w/o Context")
    table_prefix += add_row(python_ds["codegen-2B-multi_t0.2_n10,first_test,False"], java_ds["codegen-2B-multi_t0.2_n10_v2,first_test,False"], lexical_data["Codegen-2B-multi"][1]["no_context_first_test"], lexical_data["Codegen-2B-multi"][0]["no_context_first_test"], "Codegen-2B-multi")
    table_prefix += add_row(python_ds["codegen-16B-multi_t0.2_n10,first_test,False"], java_ds["codegen-16B-multi_t0.2_n10,first_test,False"], lexical_data["Codegen-16B-multi"][1]["no_context_first_test"], lexical_data["Codegen-16B-multi"][0]["no_context_first_test"], "Codegen-16B-multi")
    table_prefix += add_mono_row(python_ds["codegen-2B-multi_t0.2_n10,first_test,False"], lexical_data["Codegen-2B-mono"][0]["no_context_first_test"], "Codegen-2B-mono")
    table_prefix += add_mono_row(python_ds["codegen-16B-multi_t0.2_n10,first_test,False"], lexical_data["Codegen-16B-mono"][0]["no_context_first_test"], "Codegen-16B-mono")
    table_prefix += "\\midrule\\multicolumn{11}{c}{\\textbf{Last Test (Total: Java = 180, Python = 930)}} \\\\\\midrule\n"
    table_prefix += add_row(python_ds["t0.2_n10,last_test,True"], java_ds["t0.2_n10,last_test,True"], lexical_data["\\tool"][1]["context_last_test"], lexical_data["\\tool"][0]["context_last_test"], "\\tool w Context")
    table_prefix += add_row(python_ds["t0.2_n10,last_test,False"], java_ds["t0.2_n10,last_test,False"], lexical_data["\\tool"][1]["no_context_last_test"], lexical_data["\\tool"][0]["no_context_last_test"], "\\tool w/o Context")
    table_prefix += add_row(python_ds["codegen-2B-multi_t0.2_n10,last_test,False"], java_ds["codegen-2B-multi_t0.2_n10_v2,last_test,False"], lexical_data["Codegen-2B-multi"][1]["no_context_last_test"], lexical_data["Codegen-2B-multi"][0]["no_context_last_test"], "Codegen-2B-multi")
    table_prefix += add_row(python_ds["codegen-16B-multi_t0.2_n10,last_test,False"], java_ds["codegen-16B-multi_t0.2_n10,last_test,False"], lexical_data["Codegen-16B-multi"][1]["no_context_last_test"], lexical_data["Codegen-16B-multi"][0]["no_context_last_test"], "Codegen-16B-multi")
    table_prefix += add_mono_row(python_ds["codegen-2B-multi_t0.2_n10,last_test,False"], lexical_data["Codegen-2B-mono"][0]["no_context_last_test"], "Codegen-2B-mono")
    table_prefix += add_mono_row(python_ds["codegen-16B-multi_t0.2_n10,last_test,False"], lexical_data["Codegen-16B-mono"][0]["no_context_last_test"], "Codegen-16B-mono")
    table_prefix += "\\midrule\\multicolumn{11}{c}{\\textbf{Extra Test (Total: Java = 270, Python = 1230)}} \\\\\\midrule\n"
    table_prefix += add_extra_test_row(python_ds["t0.2_n10,extra_test,True"], java_ds["t0.2_n10,extra_test,True"], "\\tool w Context")
    table_prefix += add_extra_test_row(python_ds["t0.2_n10,extra_test,False"], java_ds["t0.2_n10,extra_test,False"], "\\tool w/o Context")
    table_prefix += add_extra_test_row(python_ds["codegen-2B-multi_t0.2_n10,extra_test,False"], java_ds["codegen-2B-multi_t0.2_n10_v2,extra_test,False"], "Codegen-2B-multi")
    table_prefix += add_extra_test_row(python_ds["codegen-16B-multi_t0.2_n10,extra_test,False"], java_ds["codegen-16B-multi_t0.2_n10,extra_test,False"], "Codegen-16B-multi")
    table_prefix += add_extra_test_mono_row(python_ds["codegen-2B-multi_t0.2_n10,extra_test,False"], "Codegen-2B-mono")
    table_prefix += add_extra_test_mono_row(python_ds["codegen-16B-multi_t0.2_n10,extra_test,False"], "Codegen-16B-mono")
    table_prefix += table_suffix

    print(table_prefix)

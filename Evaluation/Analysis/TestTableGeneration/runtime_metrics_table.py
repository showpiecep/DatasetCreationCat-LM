import json

table_template = """\\begin{table*}[ht]
{\\small
\\begin{center}
\\centering
\\caption{Runtime metrics comparison between our model vs Codegen 2B for the Java and Python test sets.}
\\label{tab:codegenruntime}
\\begin{tabular}{ll|rrrrr|rrrrr}
\\toprule
& & \\multicolumn{5}{c}{\\textbf{Java Runtime Metrics}} & \\multicolumn{5}{|c}{\\textbf{Python Runtime Metrics}} \\\\\\toprule
\\textbf{Model} & \\textbf{Context} & \\textbf{Total} & \\textbf{Unique} & \\textbf{Assert} & \\textbf{Compile} & \\textbf{Pass} & \\textbf{Total} & \\textbf{Unique} & \\textbf{Assert} & \\textbf{Compile} & \\textbf{Pass} \\\\ \\midrule
\\multicolumn{12}{c}{\\textbf{Extra test}}\\\\ \\midrule
\\tool & With & \\multirow{4}{*}{1230} & 600 & 514 & 368 & \\textbf{93} & \\multirow{4}{*}{270} & 75 & 72 & \\textbf{54} & \\textbf{31} \\\\
\\tool & Without & & 551 & 504 & \\textbf{372} & 79 & & 63 & 59 & 24 & 16 \\\\
Codegen 2B & N/A &  & 569 & 505 & 356 & 78 & & 35 & 28 & 24 & 14 \\\\
Codegen 16B & N/A & & & & & & & 40 & 34 & 19 & 12 \\\\\\midrule
\\multicolumn{12}{c}{\\textbf{First test}}\\\\ \\midrule
\\tool & With & \\multirow{4}{*}{1120} & 751 & 538 & \\textbf{363} & \\textbf{46} & \\multirow{4}{*}{180} & 173 & 131 & 53 & 22 \\\\
\\tool & Without & & 756 & 422 & 220 & 25 & & 159 & 113 & 8 & 5 \\\\ %
Codegen 2B & N/A & & 873 & 505 & 234 & 17 & & 196 & 152 & 25 & 13 \\\\
Codegen 16B & N/A & & & & & & & 176 & 151 & 33 & 7 \\\\\\midrule
\\multicolumn{12}{c}{\\textbf{Last test}}\\\\\\midrule
\\tool & With & \\multirow{4}{*}{930} & 483 & 407 & 305 & 66 & \\multirow{4}{*}{270} & 83 & 74 & 50 & 17 \\\\ % 9
\\tool & Without & & 452 & 373 & 264 & 54 & & 51 & 44 & 23 & 9 \\\\ % 6
Codegen 2B & N/A & & 545 & 486 & 349 & \\textbf{68} & & 64 & 56 & 35 & 16 \\\\
Codegen 16B & N/A & & & & & & & 47 & 38 & 20 & 9 \\\\\\bottomrule
\\end{tabular}
\\end{center}}
\\end{table*}
"""

table_prefix = """\\begin{table*}[ht]
{\\small
\\begin{center}
\\centering
\\caption{Runtime metrics comparison between our model vs CodeGen baselines for the Java and Python test sets. We measure the total number of completions, completions that are unique, completions that have an assert and compiling and passing completions.}
\\label{tab:codegenruntime}
\\begin{tabular}{ll|rrrrr|rrrrr}
\\toprule
& & \\multicolumn{5}{c}{\\textbf{Java Runtime Metrics}} & \\multicolumn{5}{|c}{\\textbf{Python Runtime Metrics}} \\\\\\toprule
\\textbf{Model} & \\textbf{Context} & \\textbf{Total} & \\textbf{Unique} & \\textbf{Assert} & \\textbf{Compile} & \\textbf{Pass} & \\textbf{Total} & \\textbf{Unique} & \\textbf{Assert} & \\textbf{Compile} & \\textbf{Pass} \\\\ \\midrule
\\multicolumn{12}{c}{\\textbf{Extra test}}\\\\ \\midrule
"""

table_suffix = """\\bottomrule
\\end{tabular}
\\end{center}}
\\end{table*}
"""

def add_mono_row(python_data, setting, tool):
    curr_py_data = python_data[setting]
    return f"{tool} & N/A & & -- & -- & -- & -- & & {curr_py_data['num_examples']} & {curr_py_data['total']} & {curr_py_data['compiling']} & {curr_py_data['passing']} \\\\\n"


def add_row(python_data, java_data, setting, tool, has_context="N/A", java_totals=-1, python_totals=-1, j_v2=False, p_v2=False):
    py_setting = f"{setting}_v2" if p_v2 else setting
    java_setting = f"{setting}_v2" if j_v2 else setting
    curr_py_data = python_data[py_setting]
    curr_java_data = java_data[java_setting]
    java_totals = "\\multirow{6}{*}{"+str(java_totals)+"}" if java_totals != -1 else ""
    python_totals = "\\multirow{6}{*}{"+str(python_totals)+"}" if python_totals != -1 else ""

    return f"{tool} & {has_context} & {java_totals} & {curr_java_data['num_examples']} & {curr_java_data['total']} & {curr_java_data['compiling']} & {curr_java_data['passing']} & {python_totals} & {curr_py_data['num_examples']} & {curr_py_data['total']} & {curr_py_data['compiling']} & {curr_py_data['passing']} \\\\\n"
    #\\tool & With & \\multirow{4}{*}{1120} & 751 & 538 & \\textbf{363} & \\textbf{46} & \\multirow{4}{*}{180} & 173 & 131 & 53 & 22 \\\\


if __name__ == "__main__":
    java_ds = json.load(open("/data/GitHubMining/TestFramework/TestingLLM/java/asserts_completion_metrics_ds.json", "r"))
    python_ds = json.load(open("/data/GitHubMining/TestFramework/TestingLLM/python/asserts_completion_metrics_ds.json", "r"))
    java_baseline_covs = json.load(open("/data/GitHubMining/TestFramework/TestingLLM/java/completion_baseline_covs.json", "r"))
    python_baseline_covs = json.load(open("/data/GitHubMining/TestFramework/TestingLLM/python/completion_baseline_covs.json", "r"))

    j_extra_test_totals = java_baseline_covs["extra_test_total"] * 10
    j_first_test_totals = java_baseline_covs["first_test_total"] * 10
    j_last_test_totals = java_baseline_covs["last_test_total"] * 10

    p_extra_test_totals = python_baseline_covs["extra_test_total"] * 10
    p_first_test_totals = python_baseline_covs["first_test_total"] * 10
    p_last_test_totals = python_baseline_covs["last_test_total"] * 10

    table_prefix += add_row(python_ds, java_ds, "t0.2_n10,extra_test,True", "\\tool", "With", j_extra_test_totals, p_extra_test_totals, j_v2=True, p_v2=True)
    table_prefix += add_row(python_ds, java_ds, "t0.2_n10,extra_test,False", "\\tool", "Without", j_v2=True, p_v2=True)
    table_prefix += add_row(python_ds, java_ds, "codegen-2B-multi_t0.2_n10,extra_test,False", "Codegen-2B-multi", j_v2=True, p_v2=False)
    table_prefix += add_row(python_ds, java_ds, "codegen-16B-multi_t0.2_n10,extra_test,False", "Codegen-16B-multi")
    table_prefix += add_mono_row(python_ds, "codegen-2B-mono_t0.2_n10,extra_test,False", "CodeGen-2B-mono")
    table_prefix += add_mono_row(python_ds, "codegen-16B-mono_t0.2_n10,extra_test,False", "CodeGen-16B-mono")

    table_prefix += "\\midrule\\multicolumn{12}{c}{\\textbf{First test}}\\\\ \\midrule"

    table_prefix += add_row(python_ds, java_ds, "t0.2_n10,first_test,True", "\\tool", "With", j_first_test_totals, p_first_test_totals)
    table_prefix += add_row(python_ds, java_ds, "t0.2_n10,first_test,False", "\\tool", "Without")
    table_prefix += add_row(python_ds, java_ds, "codegen-2B-multi_t0.2_n10,first_test,False", "Codegen-2B-multi")
    table_prefix += add_row(python_ds, java_ds, "codegen-16B-multi_t0.2_n10,first_test,False", "Codegen-16B-multi")
    table_prefix += add_mono_row(python_ds, "codegen-2B-mono_t0.2_n10,first_test,False", "CodeGen-2B-mono")
    table_prefix += add_mono_row(python_ds, "codegen-16B-mono_t0.2_n10,first_test,False", "CodeGen-16B-mono")

    table_prefix += "\\midrule\\multicolumn{12}{c}{\\textbf{Last test}}\\\\ \\midrule"

    table_prefix += add_row(python_ds, java_ds, "t0.2_n10,last_test,True", "\\tool", "With", j_last_test_totals, p_last_test_totals)
    table_prefix += add_row(python_ds, java_ds, "t0.2_n10,last_test,False", "\\tool", "Without")
    table_prefix += add_row(python_ds, java_ds, "codegen-2B-multi_t0.2_n10,last_test,False", "Codegen-2B-multi")
    table_prefix += add_row(python_ds, java_ds, "codegen-16B-multi_t0.2_n10,last_test,False", "Codegen-16B-multi")
    table_prefix += add_mono_row(python_ds, "codegen-2B-mono_t0.2_n10,last_test,False", "CodeGen-2B-mono")
    table_prefix += add_mono_row(python_ds, "codegen-16B-mono_t0.2_n10,last_test,False", "CodeGen-16B-mono")

    table_prefix += table_suffix

    print(table_prefix)
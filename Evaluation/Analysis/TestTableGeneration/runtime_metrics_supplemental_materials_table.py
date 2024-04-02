import json
import numpy as np

table_template = """\\begin{table*}[ht]
{\\small 
    \\begin{center}
    \\centering
    \\caption{Runtime metrics and coverage information comparison between our model vs Codegen 2B for the Python test set.\\todo{EXPLAIN THE COLUMN HEADERS}}
    \\begin{tabular}{ll|rrrrr|rrrrr}
    \\toprule  
                &          &                       &  \\multicolumn{4}{c}{\\textbf{Runtime Metrics}}  &   \\multicolumn{4}{c}{\\textbf{Coverage}} \\\\
        \\textbf{Setting} & \\textbf{Context}  & \\textbf{Total}                 & \\textbf{Unq.}   & \\textbf{Asrt.} & \\textbf{Cmp.} & \\textbf{Pass} & \\textbf{Baseline} & \\textbf{Imp (M)} & \\textbf{Imp (H)} & \\textbf{\\makecell{Imp (M)\\\\- 0\\%}} & \\textbf{\\makecell{Imp (H)\\\\- 0\\%}} \\\\ \\midrule
\\multicolumn{12}{c}{\\textbf{Extra test}}\\\\\\midrule
        \\tool-0.2 & Y   & \\multirow{5}{*}{1230} & 600 & 514 & 368 & \\textbf{93} & 78.19\\%  & \\textbf{0.09\\%} & 0.0\\% & \\textbf{2.65\\%} & 0.0\\% \\\\ % 93, 3
        \\tool-0.2 & N  &                       & 551 & 504 & \\textbf{372} & 79 & 81.82\\%  & 0.0\\%  & 0.0\\% & N/A    & N/A  \\\\ %79
        \\tool-0.8 & Y   &                      & 665 & 516 & 263 & 34 & 77.52\\%  & 0.0\\%  & 0.0\\% & N/A    & N/A \\\\ % 32, 0
        \\tool-0.8 & N  &                       & \\textbf{689} & \\textbf{569} & 348 & 33 & 85.71\\% & 0.03\\% & 0.0\\% & 0.53\\% & 0.0\\% \\\\ % 33, 2
        \\multicolumn{2}{l|}{Codegen 2B} &      & 569 & 505 & 356 & 78  & 78.57\\% & 0.01\\% & 0.0\\% & 1.02\\% & 0.0\\%  \\\\\\midrule % 78
\\multicolumn{12}{c}{\\textbf{First test}}\\\\\\midrule
        \\tool-0.2 & Y   & \\multirow{5}{*}{1120} & 751 & 538 & \\textbf{363} & \\textbf{46} & 0.0\\%  & 51.80\\% & 55.89\\%  & 51.80\\% & 55.89\\% \\\\ 
        \\tool-0.2 & N  &                        & 756 & 422 & 220 & 25 & 0.0\\%  & 49.56\\% & 55.25\\%  & 49.56\\% & 55.25\\% \\\\ %
        \\tool-0.8 & Y   &                       & \\textbf{861} & \\textbf{579} & 343 & 43 & 0.0\\%  & \\textbf{61.65\\%} & 63.10\\%  & \\textbf{61.65\\%} & 63.10\\%  \\\\
        \\tool-0.8 & N  &                        & 821 & 522 & 254 & 18 & 0.0\\%  & 52.01\\% & 57.89\\%  & 52.01\\% & 57.89\\% \\\\
        \\multicolumn{2}{l|}{Codegen 2B} &       & 873 & 505 & 234 & 17 & 0.0\\%  & 58.91\\% & 46.79\\%  & 58.91\\% & 46.79\\% \\\\\\midrule  % numbers are same
\\multicolumn{12}{c}{\\textbf{Last test}}\\\\\\midrule
        \\tool-0.2 & Y   &  \\multirow{5}{*}{930} & 483  & 407 & 305 & 66 & 71.72\\% & \\textbf{1.93\\%} & 7.09\\%  & 14.18\\% & 14.93\\% \\\\ % 9
        \\tool-0.2 & N  &                        & 452  & 373 & 264 & 54 & 66.45\\% & 1.71\\% & 10.45\\% & \\textbf{15.39\\%} & 29.51\\% \\\\ % 6
        \\tool-0.8 & Y   &                       & 623  & 503 & \\textbf{350} & 64 & 74.64\\% & 1.76\\% & 6.56\\%  & 10.25\\% & 20.12\\% \\\\ % 11
        \\tool-0.8 & N  &                        & \\textbf{639}  & \\textbf{494} & 344 & 48 & 65.88\\% & 1.50\\% & 9.26\\%  & 14.38\\% & 35.67\\% \\\\ % 5
        \\multicolumn{2}{l|}{Codegen 2B} &       & 545 & 486 & 349 & \\textbf{68} & 66.84\\% & 1.17\\% & 11.94\\% & 7.94\\%  & 20.62\\% \\\\\\bottomrule % 10
    \\end{tabular}
    \\end{center}}
\\end{table*}
"""

py_table_prefix = """\\begin{table*}[ht]
{\\small 
    \\begin{center}
    \\centering
    \\caption{Comparison of runtime and coverage metrics for our model vs. CodeGen baselines for Python test set (total, unique, assert-containing, compiling, and passing completions; baseline coverage; human and model-generated test coverage improvements).}    
    \\label{tab:supplementalruntimepython}
    \\begin{tabular}{l|rrrr|rrrrr}
    \\toprule  
                &   \\multicolumn{4}{c}{\\textbf{Runtime Metrics}}  &   \\multicolumn{5}{c}{\\textbf{Coverage}} \\\\
        \\textbf{Setting} & \\textbf{Unq.}   & \\textbf{Asrt.} & \\textbf{Cmp.} & \\textbf{Pass} & \\textbf{Baseline} & \\textbf{Imp (M)} & \\textbf{Imp (H)} & \\textbf{\\makecell{Imp (M)\\\\- 0\\%}} & \\textbf{\\makecell{Imp (H)\\\\- 0\\%}} \\\\ \\midrule
\\multicolumn{10}{c}{\\textbf{First test (Total: Java = 270, Python = 1120)}}\\\\\\midrule
"""

java_table_prefix = """\\begin{table*}[ht]
{\\small 
    \\begin{center}
    \\centering
    \\caption{Comparison of runtime and coverage metrics for our model vs. CodeGen baselines for Java test set (total, unique, assert-containing, compiling, and passing completions; baseline coverage; human and model-generated test coverage improvements).}    
    \\label{tab:supplementalruntimejava}
    \\begin{tabular}{l|rrrr|rrrrr}
    \\toprule  
                &     \\multicolumn{4}{c}{\\textbf{Runtime Metrics}}  &   \\multicolumn{5}{c}{\\textbf{Coverage}} \\\\
        \\textbf{Setting} & \\textbf{Unq.}   & \\textbf{Asrt.} & \\textbf{Cmp.} & \\textbf{Pass} & \\textbf{Baseline} & \\textbf{Imp (M)} & \\textbf{Imp (H)} & \\textbf{\\makecell{Imp (M)\\\\- 0\\%}} & \\textbf{\\makecell{Imp (H)\\\\- 0\\%}} \\\\ \\midrule
\\multicolumn{10}{c}{\\textbf{First test (Total: Java = 270, Python = 1120)}}\\\\\\midrule
"""

table_suffix = """\\bottomrule % 10
    \\end{tabular}
    \\end{center}}
\\end{table*}
"""

def disp_metric(met_val):
    if np.isnan(met_val):
        return "N/A"
    else:
        return f"{met_val*100:.1f}\\%"


def add_row(data, setting, tool):
    curr_data = data[setting]
    #  \tool-0.2 & Y   & \multirow{5}{*}{1230} & 600 & 514 & 368 & \textbf{93} & 78.19\%  & \textbf{0.09\%} & 0.0\% & \textbf{2.65\%} & 0.0\% \\ % 93, 3


    return f"{tool} & {curr_data['num_examples']} & {curr_data['total']} & {curr_data['compiling']} & {curr_data['passing']} & {disp_metric(curr_data['all_baseline_cov'])} & {disp_metric(curr_data['all_cov_improvement'])} & {disp_metric(curr_data['all_human_cov_improvement'])} & {disp_metric(curr_data['non_zero_cov_improvement'])} & {disp_metric(curr_data['non_zero_human_cov_improvement'])} \\\\\n"
    #\\tool & With & \\multirow{4}{*}{1120} & 751 & 538 & \\textbf{363} & \\textbf{46} & \\multirow{4}{*}{180} & 173 & 131 & 53 & 22 \\\\

def gen_table(table_prefix, pl_df, is_python=False):
    table_prefix += add_row(pl_df, "t0.2_n10,first_test,True", "\\tool w Context")
    table_prefix += add_row(pl_df, "t0.2_n10,first_test,False", "\\tool w/o Context")
    java_setting = "codegen-2B-multi_t0.2_n10,first_test,False" if is_python else "codegen-2B-multi_t0.2_n10_v2,first_test,False"
    table_prefix += add_row(pl_df, java_setting, "Codegen-2B-multi")
    table_prefix += add_row(pl_df, "codegen-16B-multi_t0.2_n10,first_test,False", "Codegen-16B-multi")
    if is_python:
        table_prefix += add_row(pl_df, "codegen-2B-mono_t0.2_n10,first_test,False", "CodeGen-2B-mono")
        table_prefix += add_row(pl_df, "codegen-16B-mono_t0.2_n10,first_test,False", "CodeGen-16B-mono")

    table_prefix += "\\midrule\\multicolumn{10}{c}{\\textbf{Last test}}\\\\ \\midrule\n"

    table_prefix += add_row(pl_df, "t0.2_n10,last_test,True", "\\tool w Context")
    table_prefix += add_row(pl_df, "t0.2_n10,last_test,False", "\\tool w/o Context")
    java_setting = "codegen-2B-multi_t0.2_n10,last_test,False" if is_python else "codegen-2B-multi_t0.2_n10_v2,last_test,False"
    table_prefix += add_row(pl_df, java_setting, "Codegen-2B-multi")
    table_prefix += add_row(pl_df, "codegen-16B-multi_t0.2_n10,last_test,False", "Codegen-16B-multi")
    if is_python:
        table_prefix += add_row(pl_df, "codegen-2B-mono_t0.2_n10,last_test,False", "CodeGen-2B-mono")
        table_prefix += add_row(pl_df, "codegen-16B-mono_t0.2_n10,last_test,False", "CodeGen-16B-mono")

    table_prefix += "\\midrule\\multicolumn{10}{c}{\\textbf{Extra test}}\\\\ \\midrule\n"

    table_prefix += add_row(pl_df, "t0.2_n10,extra_test,True", "\\tool w Context")
    table_prefix += add_row(pl_df, "t0.2_n10,extra_test,False", "\\tool w/o Context")
    java_setting = "codegen-2B-multi_t0.2_n10,extra_test,False" if is_python else "codegen-2B-multi_t0.2_n10_v2,extra_test,False"
    table_prefix += add_row(pl_df, java_setting, "Codegen-2B-multi")
    table_prefix += add_row(pl_df, "codegen-16B-multi_t0.2_n10,extra_test,False", "Codegen-16B-multi")
    if is_python:
        table_prefix += add_row(pl_df, "codegen-2B-mono_t0.2_n10,extra_test,False", "CodeGen-2B-mono")
        table_prefix += add_row(pl_df, "codegen-16B-mono_t0.2_n10,extra_test,False", "CodeGen-16B-mono")

    table_prefix += table_suffix

    print(table_prefix)


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

    gen_table(py_table_prefix, python_ds, True)
    gen_table(java_table_prefix, java_ds)
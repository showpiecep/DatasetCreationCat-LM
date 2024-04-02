import sys
import os
import pandas as pd
import json
import numpy as np

# def compute_fp_stats(df, df_cov):

# def compute_proj_stats(df, df_cov):


def compute_df_stats(df):
    parse_rate = df[df["Status"] != "COMPILE"].shape[0] / df.shape[0]
    pass_rate = df[df["Status"] == "SUCCESS"].shape[0] / df.shape[0]
    compiling = df.shape[0] - df[df["Status"] == "COMPILE"].shape[0]
    passing = df[df["Status"] == "SUCCESS"].shape[0]
    total = df.shape[0]
    return {
        "parse_rate": parse_rate,
        "pass_rate": pass_rate,
        "compiling": compiling,
        "passing": passing,
        "total": total,
        "pass_rate_compile_rate":  passing / compiling if compiling != 0 else 0
    }

def compute_cov_df_stats(df_cov, prefix):
    cov_improvement = df_cov["Coverage Improvement"].mean()
    human_cov_improvement = df_cov["Human Coverage Improvement"].mean()
    baseline_cov = df_cov["Baseline Coverage"].mean()

    return {
        f"{prefix}_baseline_cov": baseline_cov,
        f"{prefix}_cov_improvement": cov_improvement,
        f"{prefix}_human_cov_improvement": human_cov_improvement,
        f"{prefix}_cov_examples": df_cov.shape[0]
    }

def compute_fp_stats(group_df):
    aggregate_obj = {}
    total_fps = group_df.groupby(['Source Filename', 'Test Filename']).ngroups
    aggregate_obj["filepair_parse_ct"] = group_df[group_df["Status"] != "COMPILE"].groupby(['Source Filename', 'Test Filename']).ngroups
    aggregate_obj["filepair_pass_ct"] = group_df[group_df["Status"] == "SUCCESS"].groupby(['Source Filename', 'Test Filename']).ngroups
    aggregate_obj["filepair_pass_rate"] = aggregate_obj["filepair_pass_ct"] / total_fps
    aggregate_obj["filepair_parse_rate"] = aggregate_obj["filepair_parse_ct"] / total_fps
    aggregate_obj["num_pairs"] = total_fps
    return aggregate_obj


def build_setting_obj(group_df, df_cov_grouping, df_cov_grouping_non_zero, df_full_grouping, is_fp):
    setting_obj = {}
    group_df_stats = compute_df_stats(group_df)
    setting_obj.update(group_df_stats)

    cov_group_stats = compute_cov_df_stats(df_cov_grouping, "all")
    setting_obj.update(cov_group_stats)

    cov_group_non_zero_stats = compute_cov_df_stats(df_cov_grouping_non_zero, "non_zero")
    setting_obj.update(cov_group_non_zero_stats)

    if not is_fp:
        group_df_fp_stats = compute_fp_stats(group_df)
        setting_obj.update(group_df_fp_stats)

    
    setting_obj["num_examples"] = df_full_grouping.shape[0]
    setting_obj["assert_rate"] = setting_obj["total"] / setting_obj["num_examples"]

    return setting_obj

def compute_stats(df, df_cov, df_full, grouping, output_path, is_fp):
    aggregate_obj = {}
    for name, group_df in df.groupby(grouping):
        df_cov_grouping = df_cov.copy()
        df_full_grouping = df_full.copy()
        for i, col in enumerate(grouping):
            df_cov_grouping = df_cov_grouping[df_cov_grouping[col] == name[i]]
            df_full_grouping = df_full_grouping[df_full_grouping[col] == name[i]]
        
        df_cov_grouping_non_zero = df_cov_grouping[df_cov_grouping["Coverage Improvement"] != 0]
        
        setting_obj = build_setting_obj(group_df, df_cov_grouping, df_cov_grouping_non_zero, df_full_grouping, is_fp)
        aggregate_obj[",".join([str(n) for n in name])] = setting_obj

    with open(output_path, 'w') as f:
        json.dump(aggregate_obj, f, indent=4)
    

def build_cov_df(df):
    df_cov = df[df[['Coverage', 'Baseline Coverage', 'Human Coverage']].notnull().all(1)]
    df_cov['Baseline Coverage'] = df_cov['Baseline Coverage'].astype(float)
    df_cov['Coverage Improvement'] = df_cov['Coverage'] - df_cov['Baseline Coverage']
    df_cov['Human Coverage Improvement'] = df_cov['Human Coverage'] - df_cov['Baseline Coverage']
    return df_cov


def build_json_files(framework_dir, df, cov_df, df_full, prefix, language):
    DS_GROUPING = ["Setting", "Mode", "Context"]
    PROJ_GROUPING = ["Setting", "Mode", "Context", "Organization", "Project"]
    FP_GROUPING = ["Setting", "Mode", "Context", "Organization", "Project", "Source Filename", "Test Filename"]

    ds_stats_path = os.path.join(framework_dir, language, f"{prefix}_completion_metrics_ds.json")
    proj_stats_path = os.path.join(framework_dir, language, f"{prefix}_completion_metrics_proj.json")
    fp_stats_path = os.path.join(framework_dir, language, f"{prefix}_completion_metrics_fp.json")
    compute_stats(df, cov_df, df_full, DS_GROUPING, ds_stats_path, False)
    compute_stats(df, cov_df, df_full, PROJ_GROUPING, proj_stats_path, False)
    compute_stats(df, cov_df, df_full, FP_GROUPING, fp_stats_path, True)


if __name__ == "__main__":
    framework_dir = sys.argv[1] if len(sys.argv) > 1 else '/data/GitHubMining/TestFramework/TestingLLM'

    python_csv_path = os.path.join(framework_dir, "python_coverage_results_v2.csv")
    df_py = pd.read_csv(python_csv_path)
    df_asserts_py = df_py[df_py['Is Test']]
    cov_asserts_py = build_cov_df(df_asserts_py)

    build_json_files(framework_dir, df_asserts_py, cov_asserts_py, df_py, "asserts", "python")


    java_csv_path = os.path.join(framework_dir, "java_coverage_results_v2.csv")
    df_java = pd.read_csv(java_csv_path)
    df_asserts_java = df_java[df_java['Is Test']]
    cov_asserts_java = build_cov_df(df_asserts_java)

    build_json_files(framework_dir, df_asserts_java, cov_asserts_java, df_java, "asserts", "java")

import pandas as pd
import json
import subprocess
import sys
import os


def run_cmd(cmd, timeout):
    try: 
        cmd_output = subprocess.run(cmd, stdout=subprocess.PIPE, timeout=timeout)
        return cmd_output, False
    except Exception as e:
        return None, True

def clean_proj(clean_cmd="", is_java=""):
    if is_java != "":
        if is_java == "maven":
            os.system("mvn clean")
        if is_java == "gradle":
            os.system("gradle clean")
    else:
        if len(clean_cmd) > 0:
            subprocess.run(clean_cmd, stdout=subprocess.PIPE)
        else:
            os.system("git clean -xdf")
            os.system("git checkout .")

def edit_test_cov_cmd(cmd, lang, test_fn):
    if lang == "python":
        return cmd + [test_fn]
    test_class = test_fn.split("/")[-1].split(".")[0]
    return cmd + [f"-Dtest={test_class}"]


def compute_coverage_java(coverage_csv, source_fn):
    csv_df = pd.read_csv(coverage_csv)
    filtered_rows = csv_df[csv_df["CLASS"] == source_fn.split("/")[-1].split(".")[0]]
    if len(filtered_rows) == 0:
        return "NOT FOUND"

    cov_row = filtered_rows.iloc[0]
    if len(filtered_rows) > 1:
        for index, row in filtered_rows.iterrows():
            if row["PACKAGE"].replace(".", "/") in source_fn:
                cov_row = row
    return cov_row["LINE_COVERED"] / (cov_row["LINE_COVERED"] + cov_row["LINE_MISSED"])


def compute_coverage_python(coverage_json, source_fn):
    with open(coverage_json, "r") as f:
        cov_info = json.load(f)
    
    for fn in cov_info["files"]:
        if fn in source_fn:
            return cov_info["files"][fn]["summary"]["percent_covered"]/100
    
    return "NOT FOUND"


def setup_project(proj_info, language, image):
    if language == "java":
        os.chdir(proj_info["build_dir"]) if "gradle" in image else os.chdir(proj_info["pom_dir"])

    cwd = os.getcwd()
    if len(proj_info["setup_dir"]) > 0:
        os.chdir(proj_info["setup_dir"])

    if len(proj_info["setup_steps"]) > 0:
        for step in proj_info["setup_steps"]:
            run_cmd(step, 1200) 
    
    os.chdir(cwd)

def run_tests(proj_info, source_fn, test_fn, language, image):
    if len(proj_info["compile_cmd"][0]) > 0:
        compile_result, compile_timeout = run_cmd(proj_info["compile_cmd"], 600)

        if compile_timeout or compile_result.returncode != 0:
            print("FAILED - not compiling")
            return "COMPILE", ""

    if len(proj_info["test_cmd"][0]) > 0:
        print(edit_test_cov_cmd(proj_info["test_cmd"], language, test_fn))
        test_result, test_timeout = run_cmd(edit_test_cov_cmd(proj_info["test_cmd"], language, test_fn), 600)
        if test_timeout or test_result.returncode != 0:
            if test_timeout:
                return "TEST", ""
            
            test_stdout = str(test_result.stdout, "utf-8")
            if language == "python" and "SyntaxError" in test_stdout or "NameError" in test_stdout or "ModuleNotFoundError" in test_stdout:
                print("FAILED - syntax or name error")
                return "COMPILE", ""
            
            print("FAILED - tests don't run")

            return "TEST", ""

    if len(proj_info["cov_cmd"][0]) > 0:
        cov_result, cov_timeout = run_cmd(edit_test_cov_cmd(proj_info["cov_cmd"], language, test_fn), 600)

        if cov_timeout or cov_result.returncode != 0:
            print("FAILED - coverage doesn't run")
            return "COV", ""
    
    if language == "python":
        subprocess.run(["coverage", "json"], stdout=subprocess.PIPE)
        line_coverage = compute_coverage_python("coverage.json", source_fn)
    else:
        file_path = "build/reports/jacoco/test/jacocoTestReport.csv" if "gradle" in image else "target/site/jacoco/jacoco.csv"
        line_coverage = compute_coverage_java(file_path, source_fn)

    print("SUCCESS - got coverage")
    return "SUCCESS", line_coverage
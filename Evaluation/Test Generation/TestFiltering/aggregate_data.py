import sys
import os
import json

def build_results(results_dir, repo_links):
    results = {}
    reasons = {}
    num_successful = 0
    num_total = 0

    for project_link in repo_links:
        project_link = project_link.split('\t')[0]
        if project_link.endswith('/'):
            project_link = project_link[:-1]
        *_, org, project = project_link.split('/')

        filename = os.path.join(results_dir, f"{org}_{project}.json")


        if os.path.exists(filename):
            with open(filename, "r") as f:
                result_proj = json.load(f)
            
            curr_reason = {}
            found_success = False
            for image in result_proj:
                result = result_proj[image]
                if "reason" in result:
                    res_reason = result["reason"]
                    if res_reason not in curr_reason:
                        curr_reason[res_reason] = 0
                    curr_reason[res_reason] += 1
                if result["status"] == "SUCCESS":
                    found_success = True
                    setup_steps = result["setup_steps"] if "setup_steps" in result is not None else []
                    cov_cmd = result["jacoco_cmd"] if "jacoco_cmd" in result is not None else result["coverage_cmd"]
                    if org not in results:
                        results[org] = {}
                    pom_dir = result["pom_dir"] if "pom_dir" in result else ""
                    build_dir = result["build_dir"] if "build_dir" in result else ""
                    clean_cmd = result["clean_cmd"] if "clean_cmd" in result else ""
                    setup_dir = result["setup_dir"] if "setup_dir" in result else ""

                    results[org][project] = {"pom_dir": pom_dir, "build_dir": build_dir, "clean_cmd": clean_cmd, "setup_dir": setup_dir, "setup_steps": setup_steps, "compile_cmd": result["compile_cmd"], "test_cmd": result["test_cmd"], "cov_cmd": cov_cmd, "image": image}
            num_total += 1
            if found_success:
                num_successful += 1
            else:
                for reason in curr_reason:
                    if reason not in reasons:
                        reasons[reason] = 0
                    if "POM" in reason:
                        print(project_link)
                        
                    reasons[reason] += curr_reason[reason]
            
        else:
            print(f"Unable to find results file for {org}/{project}")
    print(f"{results_dir}: {num_successful}/{num_total}")
    print(results)
    return results
        


if __name__ == '__main__':
    filter_dir = sys.argv[1] if len(sys.argv) > 1 else '/data/GitHubMining/TestFiltering/'
    output_dir = sys.argv[2] if len(sys.argv) > 2 else '/data/GitHubMining/'

    python_results_dir = os.path.join(filter_dir, "python", "results")
    java_results_dir = os.path.join(filter_dir, "java", "results")

    with open(os.path.join(output_dir, f"test_filtered_fp_python.txt"), "r") as f:
        python_repo_links = f.read().split('\n')

    with open(os.path.join(output_dir, f"test_filtered_fp_java.txt"), "r") as f:
        java_repo_links = f.read().split('\n')

    java_results = build_results(java_results_dir, java_repo_links)
    python_results = build_results(python_results_dir, python_repo_links)

    results = {"java": java_results, "python": python_results}

    with open(os.path.join(output_dir, "test_exec_filtered.json"), "w") as f:
        json.dump(results, f)
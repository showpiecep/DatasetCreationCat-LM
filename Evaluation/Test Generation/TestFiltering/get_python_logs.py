# Assumes this is in a docker image with pytest and coverage

import json
import sys
import os
import subprocess

def run_cmd(cmd, timeout):
    try: 
        cmd_output = subprocess.run(cmd, stdout=subprocess.PIPE, timeout=timeout)
        return cmd_output, False
    except subprocess.TimeoutExpired as e:
        return None, True

# checks code in /data
def check_python():
    setup_steps = []
    
    if os.path.isfile("setup.py"):
        setup_cmd = ["pip3", "install", ".[test]"]
        setup_steps.append(setup_cmd)
        run_cmd(setup_cmd, 600)

    elif os.path.isfile("requirements.txt"):
        requirements_cmd = ["pip3", "install", "-r", "requirements.txt"]
        setup_steps.append(requirements_cmd)
        run_cmd(requirements_cmd, 600)

    test_result, test_timeout = run_cmd(['pytest'], 600)
    if test_timeout or test_result.returncode != 0:
        print("Unable to run or failing tests -- skipping")
        return {"status": "FAILED", "reason": "Not testing"}

    coverage_result, coverage_timeout = run_cmd(['coverage', 'run', '-m', 'pytest'], 600)
    if coverage_timeout or coverage_result.returncode != 0:
        print("Unable to run coverage -- skipping")
        return {"status": "FAILED", "reason": "Not able to generate coverage report"}

    return {"status": "SUCCESS", "setup_steps": setup_steps, "compile_cmd": [""], "test_cmd": ["pytest"], "coverage_cmd": ["coverage", "run", "-m", "pytest"]}


if __name__ == "__main__":
    repo_dir = sys.argv[1]
    output_file = sys.argv[2]
    docker_image = sys.argv[3]
    
    curr_res = {}
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            curr_res = json.load(f)

    found_success = False
    for image in curr_res:
        if curr_res[image]["status"] == "SUCCESS":
            found_success = True
            break
    
    if not found_success:
        cwd = os.getcwd()
        os.chdir(repo_dir)

        result = check_python()
        curr_res[docker_image] = result

        os.chdir(cwd)
        with open(output_file, "w") as f:
            json.dump(curr_res, f)


# Assumes this is in a docker image with Java 8 and maven

import json
import sys
import os
import glob
import subprocess
import xmltodict

JACOCO_DEFAULT = {'groupId': 'org.jacoco', 'artifactId': 'jacoco-maven-plugin', 'version': '0.8.6', 'executions': {'execution': [{'id': 'prepare-agent', 'goals': {'goal': 'prepare-agent'}}, {'id': 'report', 'phase': 'test', 'goals': {'goal': 'report'}}]}}


def update_pom_file(pom_xml):
    with open(pom_xml, "r") as f:
        pom = xmltodict.parse(f.read())
    
    try:
        plugins = pom["project"]["build"]["plugins"]["plugin"]
        if not isinstance(plugins, list):
            plugins = [plugins]
            pom["project"]["build"]["plugins"]["plugin"] = plugins
        found_jacoco = "NO"
        for i, plugin in enumerate(plugins):
            if plugin.get("artifactId") == "jacoco-maven-plugin":
                found_jacoco = "YES"
                break
        if found_jacoco == "NO":
            pom["project"]["build"]["plugins"]["plugin"].append(JACOCO_DEFAULT)
            with open(pom_xml, "w") as f:
                f.write(xmltodict.unparse(pom))
        return found_jacoco
    except Exception as e:
        return "ERROR"

def update_gradle_file(build_gradle):
    with open(build_gradle, "r") as f:
        lines = f.read().split("\n")
    
    new_lines = []
    new_lines += lines
    new_lines += ["apply plugin: 'jacoco'"]
    new_lines += ["jacocoTestReport {", "reports {", "csv.required = true", "}", "}"]

    with open(build_gradle, "w") as f:
        f.write("\n".join(new_lines))

def run_cmd(cmd, timeout):
    try: 
        cmd_output = subprocess.run(cmd, stdout=subprocess.PIPE, timeout=timeout)
        return cmd_output, False
    except subprocess.TimeoutExpired as e:
        return None, True


# checks code in /data
def check_java_mvn():
    pom_files = glob.glob(f'./**/pom.xml', recursive=True)
    
    # check if maven
    if len(pom_files) == 0:
        print("Not maven -- skipping")
        return {"status": "FAILED", "reason": "Not maven", "pom_files": pom_files}

    # check single module
    if len(pom_files) > 1:
        print("Not single module -- skipping")
        return {"status": "FAILED", "reason": "Multi-module", "pom_files": pom_files}

    pom_file = pom_files[0]
    pom_dir = os.path.dirname(pom_file)
    os.chdir(pom_dir)
    # clean anything that is there
    run_cmd(['mvn', 'clean'], 600)
    run_cmd(['git', 'clean', "-xdf"], 600)
    run_cmd(['git', 'reset', "--hard"], 600)


    compile_result, compile_timeout = run_cmd(['mvn', 'compile'], 600)

    if compile_timeout or compile_result.returncode != 0:
        print("Unable to compile -- skipping")
        return {"status": "FAILED", "reason": "Not compiling"}

    test_result, test_timeout = run_cmd(['mvn', 'test'], 600)
    if test_timeout or test_result.returncode != 0:
        print("Unable to run or failing tests -- skipping")
        return {"status": "FAILED", "reason": "Not testing"}

    found_jacoco = update_pom_file(pom_file)    

    if found_jacoco == "ERROR":
        print("Unable to run coverage -- skipping")
        return {"status": "FAILED", "reason": "Not able to update POM"}
    else:
        jacoco_result, jacoco_timeout = run_cmd(['mvn', 'test'], 600)
        if jacoco_timeout or jacoco_result.returncode != 0:
            print("Unable to run coverage -- skipping")
            return {"status": "FAILED", "reason": "Not able to generate jacoco report"}
    
    jacoco_cmd = ["mvn", "jacoco:report"] if found_jacoco == "YES" else ["mvn", "test"]
    print({"status": "SUCCESS", "pom_file": pom_file, "pom_dir": pom_dir, "compile_cmd": ["mvn","compile"], "test_cmd": ["mvn", "test"], "jacoco_cmd": jacoco_cmd})
    return {"status": "SUCCESS", "pom_file": pom_file, "pom_dir": pom_dir, "compile_cmd": ["mvn","compile"], "test_cmd": ["mvn", "test"], "jacoco_cmd": jacoco_cmd}

# checks code in /data
def check_java_gradle():
    build_files = glob.glob(f'./**/build.gradle', recursive=True)
    
    # check if maven
    if len(build_files) == 0:
        print("Not gradle -- skipping")
        return {"status": "FAILED", "reason": "Not gradle", "build_files": build_files}

    # check single module
    if len(build_files) > 1:
        print("Not single module -- skipping")
        return {"status": "FAILED", "reason": "Multi-module", "build_files": build_files}

    build_file = build_files[0]
    build_dir = os.path.dirname(build_file)
    os.chdir(build_dir)
    # clean anything that is there
    run_cmd(['gradle', 'clean'], 600)
    run_cmd(['git', 'clean', "-xdf"], 600)
    run_cmd(['git', 'reset', "--hard"], 600)


    compile_result, compile_timeout = run_cmd(['gradle', 'compileJava'], 600)

    if compile_timeout or compile_result.returncode != 0:
        print("Unable to compile -- skipping")
        return {"status": "FAILED", "reason": "Not compiling"}

    test_result, test_timeout = run_cmd(['gradle', 'test'], 600)
    if test_timeout or test_result.returncode != 0:
        print("Unable to run or failing tests -- skipping")
        return {"status": "FAILED", "reason": "Not testing"}

    update_gradle_file(build_file)    

    jacoco_result, jacoco_timeout = run_cmd(['gradle', 'build', 'jacocoTestReport'], 600)
    if jacoco_timeout or jacoco_result.returncode != 0:
        print("Unable to run coverage -- skipping")
        return {"status": "FAILED", "reason": "Not able to generate jacoco report"}
    
    jacoco_cmd = ['gradle', 'build', 'jacocoTestReport']
    print({"status": "SUCCESS", "build_file": build_file, "build_dir": build_dir, "compile_cmd": ["gradle","compileJava"], "test_cmd": ["gradle", "test"], "jacoco_cmd": jacoco_cmd})
    return {"status": "SUCCESS", "build_file": build_file, "build_dir": build_dir, "compile_cmd": ["gradle","compileJava"], "test_cmd": ["gradle", "test"], "jacoco_cmd": jacoco_cmd}


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
    
    # if not found_success:
    cwd = os.getcwd()
    os.chdir(repo_dir)

    result = check_java_mvn() if "maven" in docker_image else check_java_gradle()
    curr_res[docker_image] = result

    os.chdir(cwd)
        # with open(output_file, "w") as f:
        #     json.dump(curr_res, f)

import docker
import sys
import os
import json

if __name__ == '__main__':
    IMAGES = ["java8gradle", "java8maven", "java11gradle", "java11maven", "java14gradle", "java14maven", "java17gradle", "java17maven"]
    repo_dir = sys.argv[1] if len(sys.argv) > 1 else '/data/GitHubMining/RawDataSample/'
    test_filtered_output_dir = sys.argv[2] if len(sys.argv) > 2 else '/data/GitHubMining/'

    with open(os.path.join(test_filtered_output_dir, f"test_filtered_fp_java.txt"), "r") as f:
        repo_links = f.read().split('\n')

    for project_link in repo_links:
        project_link = project_link.split('\t')[0]
        if project_link.endswith('/'):
            project_link = project_link[:-1]
        *_, org, project = project_link.split('/')

        proj_root = os.path.join(repo_dir, "java", org, project)
        for image in IMAGES:
            print(f"docker run --rm -it --mount type=bind,src=/home/projects/SoftwareTesting/FileLevel/TestFiltering,dst=/code --mount type=bind,src=/data,dst=/data {image} python3 get_java_logs.py {proj_root} /data/GitHubMining/TestFiltering/java/results/{org}_{project}.json {image} 2>&1 | tee /data/GitHubMining/TestFiltering/java/logs/{org}_{project}.txt")
            os.system(f"docker run --rm -it --mount type=bind,src=/home/projects/SoftwareTesting/FileLevel/TestFiltering,dst=/code --mount type=bind,src=/data,dst=/data {image} python3 get_java_logs.py {proj_root} /data/GitHubMining/TestFiltering/java/results/{org}_{project}.json {image} 2>&1 | tee /data/GitHubMining/TestFiltering/java/logs/{org}_{project}.txt")
import gzip
import multiprocessing
import os
import shutil
import hashlib
import time
import numpy as np
import re
import sys
import json
from multiprocessing import Pool
import shutil
import random
import glob
import subprocess
import xmltodict
sys.path.append('../')
from TestFramework.file_utils import *

def write_list(f, arr):
    started = False
    for line in arr:
        if started:
            f.write('\n')
        started = True
        f.write(line)


def filter_links(repo_links, language, output_dir, repo_dir):
    new_repos_links = []
    total_fps = 0
    for project_link in repo_links:
        project_link = project_link.split('\t')[0]
        if project_link.endswith('/'):
            project_link = project_link[:-1]
        *_, org, project = project_link.split('/')

        proj_root = os.path.join(repo_dir, language, org, project)

        filepairs_path = os.path.join(output_dir, language, 'FilePairs', 'filepairs_' + org + '__' + project + '.json')
        with open(filepairs_path, "r") as f:
            file_pairs = json.load(f)

        for i in range(len(file_pairs["code_filename"])):
            source_fn = file_pairs["code_filename"][i]
            test_fn = file_pairs["test_filename"][i]
            try:
                code_non_trivial = filter_file_java(source_fn) if language == "java" else 3 # for python there can be files without methods still tested
                test_non_trivial = filter_file_java(test_fn) if language == "java" else filter_file_python(test_fn)


                if test_non_trivial > 0 and code_non_trivial > 0:
                    print(project_link)
                    break
            except Exception as e:
                print(e)


        if len(file_pairs["code_filename"]) > 0:

            new_repos_links.append(project_link)

    return new_repos_links


if __name__ == '__main__':
    repo_dir = sys.argv[1] if len(sys.argv) > 1 else '/data/GitHubMining/RawDataSample/'
    train_test_output_dir = sys.argv[2] if len(sys.argv) > 2 else '/data/GitHubMining/'
    output_dir = sys.argv[3] if len(sys.argv) > 3 else '/data/GitHubMining/RawDataSampleOutput/'

    with open(os.path.join(train_test_output_dir, f"test_python.txt"), "r") as f:
        python_repos_links = f.read().split('\n')
    
    with open(os.path.join(train_test_output_dir, f"test_java.txt"), "r") as f:
        java_repos_links = f.read().split('\n')

    print(len(python_repos_links))
    print(len(java_repos_links))

    new_test_set_python = filter_links(python_repos_links, "python", output_dir, repo_dir)
    #new_test_set_java = filter_links(java_repos_links, "java", output_dir, repo_dir)
    
    # print(new_test_set_java)
    # print(new_test_set_python)
    # with open(os.path.join(train_test_output_dir, f"test_filtered_fp_python.txt"), "w") as f:
    #     write_list(f, new_test_set_python)
        
    
    # with open(os.path.join(train_test_output_dir, f"test_filtered_fp_java.txt"), "w") as f:
    #     write_list(f, new_test_set_java)
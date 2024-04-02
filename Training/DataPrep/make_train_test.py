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
from tqdm import tqdm
import shutil
import random
import argparse


TEST_SET_SIZE_PER_LANG =  10 # default: 500
MIN_PAIRS =  10 # default: 1000
MAX_PAIRS =  15 # default: 3000          


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--repo_dir", default='/data/GitHubMining/CurrentStateDeduplicated/')
    parser.add_argument("--train_test_output_dir", default='/data/GitHubMining/')
    parser.add_argument("--output_dir", default='/data/GitHubMining/Output/')
    parser.add_argument("--python_repos_file_path", default='../GitHubMining/python-top-repos.txt')
    parser.add_argument("--java_repos_file_path", default=None)  # '../GitHubMining/java-top-repos.txt')

    args = parser.parse_args()
    
    return args

def write_list(f, arr):
    started = False
    for line in arr:
        if started:
            f.write('\n')
        started = True
        f.write(line) 

if __name__ == '__main__':
    args = get_args()

    found_sample = False
    with open(args.python_repos_file_path) as f:
        python_repos_links = f.read().split('\n')

    if args.java_repos_file_path:
        with open(args.java_repos_file_path) as f:
            java_repos_links = f.read().split('\n')

    print(f"Finding test set with >{MIN_PAIRS} and <{MAX_PAIRS} pairs")
    while not found_sample:
        random.shuffle(python_repos_links)
        num_filepairs = 0
        for project_link in python_repos_links[:TEST_SET_SIZE_PER_LANG]:
            project_link = project_link.split('\t')[0]
            if project_link.endswith('/'):
                project_link = project_link[:-1]
            *_, org, project = project_link.split('/')

            filepairs_path = os.path.join(args.output_dir, "python", 'DeduplicatedFilePairs', 'filepairs_' + org + '__' + project + '.json')
            with open(filepairs_path, "r") as f:
                file_pairs = json.load(f)

            num_filepairs += len(file_pairs)

        if args.java_repos_file_path:
            for project_link in java_repos_links[:TEST_SET_SIZE_PER_LANG]:
                project_link = project_link.split('\t')[0]
                if project_link.endswith('/'):
                    project_link = project_link[:-1]
                *_, org, project = project_link.split('/')

                filepairs_path = os.path.join(args.output_dir, "java", 'DeduplicatedFilePairs', 'filepairs_' + org + '__' + project + '.json')
                with open(filepairs_path, "r") as f:
                    file_pairs = json.load(f)

                num_filepairs += len(file_pairs)

        if num_filepairs > MIN_PAIRS and num_filepairs < MAX_PAIRS:
            found_sample = True

    print("Found test set")
    python_test_set = python_repos_links[:TEST_SET_SIZE_PER_LANG]
    python_train_set = python_repos_links[TEST_SET_SIZE_PER_LANG:]
    
    java_test_set = java_repos_links[:TEST_SET_SIZE_PER_LANG]
    java_train_set = java_repos_links[TEST_SET_SIZE_PER_LANG:]

    with open(os.path.join(args.train_test_output_dir, f"test_python.txt"), "w") as f:
        write_list(f, python_test_set)

    with open(os.path.join(args.train_test_output_dir, f"train_python.txt"), "w") as f:
        write_list(f, python_train_set)
        
    if args.java_repos_file_path:
        with open(os.path.join(args.train_test_output_dir, f"test_java.txt"), "w") as f:
            write_list(f, java_test_set)

        with open(os.path.join(args.train_test_output_dir, f"train_java.txt"), "w") as f:
            write_list(f, java_train_set)
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


TEST_SET_SIZE_PER_LANG =  5 # default: 500
MIN_PAIRS =  1 # default: 1000
MAX_PAIRS =  100 # default: 3000          


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--repo_dir", help="Почему-то авторы кода решили ввести данный аргумент, \
                        но не используют его", default='/data/GitHubMining/CurrentStateDeduplicated/')
    parser.add_argument("--train_test_output_dir", help='Путь до папки, которая будет \
                            содержать текстовые файлы с разбиением на test и train', default='/data/GitHubMining/')
    parser.add_argument("--output_dir", help='Путь до папки, содержащей DeduplicatedFilePairs', 
                        default='/data/GitHubMining/Output/')
    parser.add_argument("--python_repos_file_path", help='текстовый файл, откуда будут браться \
                        названия склонированных репозиториев', default='../GitHubMining/python-top-repos.txt')
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
        # random.shuffle(python_repos_links) # ! Так как я использую не весь список спаршенных репозиторие а только первые 1500, то я убрал шафл
        num_filepairs = 0
        for project_link in python_repos_links[:TEST_SET_SIZE_PER_LANG]:
            project_link = project_link.split('\t')[0]
            if project_link.endswith('/'):
                project_link = project_link[:-1]
            *_, org, project = project_link.split('/')

            filepairs_path = os.path.join(args.output_dir, "python", 'DeduplicatedFilePairs', 
                                          'filepairs_' + org + '__' + project + '.json')
            try:
                with open(filepairs_path, "r") as f:
                    file_pairs = json.load(f)
            except Exception as e:
                print(e)
                continue

            num_filepairs += len(file_pairs)

        if args.java_repos_file_path:
            for project_link in java_repos_links[:TEST_SET_SIZE_PER_LANG]:
                project_link = project_link.split('\t')[0]
                if project_link.endswith('/'):
                    project_link = project_link[:-1]
                *_, org, project = project_link.split('/')

                filepairs_path = os.path.join(args.output_dir, "java", 'DeduplicatedFilePairs', 
                                              'filepairs_' + org + '__' + project + '.json')
                with open(filepairs_path, "r") as f:
                    file_pairs = json.load(f)

                num_filepairs += len(file_pairs)

        if num_filepairs > MIN_PAIRS and num_filepairs < MAX_PAIRS:
            found_sample = True

    print("Found test set")
    python_test_set = python_repos_links[:TEST_SET_SIZE_PER_LANG]
    python_train_set = python_repos_links[TEST_SET_SIZE_PER_LANG:]
    
    if args.java_repos_file_path:
        java_test_set = java_repos_links[:TEST_SET_SIZE_PER_LANG]
        java_train_set = java_repos_links[TEST_SET_SIZE_PER_LANG:]

    with open(os.path.join(args.train_test_output_dir, f"test_python.txt"), "w") as f:
        write_list(f, python_test_set)

    with open(os.path.join(args.train_test_output_dir, f"train_python.txt"), "w") as f:
        print(os.path.join(args.train_test_output_dir, f"train_python.txt"))
        write_list(f, python_train_set)
        
    if args.java_repos_file_path:
        with open(os.path.join(args.train_test_output_dir, f"test_java.txt"), "w") as f:
            write_list(f, java_test_set)

        with open(os.path.join(args.train_test_output_dir, f"train_java.txt"), "w") as f:
            write_list(f, java_train_set)
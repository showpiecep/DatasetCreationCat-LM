import gzip
import multiprocessing
import os
import shutil
import hashlib
import time
from typing import Literal
import numpy as np
import re
import sys
import json
from multiprocessing import Pool
from tqdm import tqdm
import shutil
import pandas as pd
import argparse


SEP_TOKEN = "<|codetestpair|>"


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--repo_dir", default='/data/GitHubMining/CurrentState/')
    parser.add_argument("--train_dir", default='/data/GitHubMining/CurrentStateProcessed/train/')
    parser.add_argument("--test_dir", default=None)  # '/data/GitHubMining/CurrentStateProcessed/test/')
    parser.add_argument("--output_dir", default='/data/GitHubMining/Output/')
    parser.add_argument("--train_test_list_path", default='/data/GitHubMining/')
    parser.add_argument("--pl", default='python')

    return parser.parse_args()


"""
Flattening all paths at this step.
"""
def copy_with_concat(repo_dir: str, 
                     copy_dir: str, 
                     pl: Literal["python", "java"], 
                     org: str, 
                     project: str, 
                     file_pairs_df: pd.DataFrame):
    """

    Args:
        repo_dir (str): Корневая директория для взятия данных
        copy_dir (str): Корневая директория для перенос пар
        pl (Literal[&quot;python&quot;, &quot;java&quot;]): _description_
        org (str): _description_
        project (str): _description_
        file_pairs_df (pd.DataFrame): _description_
    """
    base_dir = os.path.join(repo_dir, pl, org, project)  # Получаем путь до директории 
    copy_dir = os.path.join(copy_dir, pl, org, project)  # Путь для копирования пары
    os.makedirs(copy_dir, exist_ok=True)

    special_files = set()

    suffix = ".py" if pl == "python" else ".java"
    for index, row in file_pairs_df.iterrows():
        code_file_path = row["code_filename"]
        test_file_path = row["test_filename"]
        special_files.add(code_file_path)
        special_files.add(test_file_path)

        with open(code_file_path, errors='ignore') as code_file:
            code_content = code_file.read()
        with open(test_file_path, errors="ignore") as test_file:
            test_content = test_file.read()
        
        # --- Получаем пары ---
        new_content = code_content + SEP_TOKEN + test_content

        code_name = code_file_path.split("/")[-1][-len(suffix):]
        test_name = test_file_path.split("/")[-1]

        combined_path = f"Filepair_{index}_{code_name}__{test_name}"
        with open(f"{copy_dir}/{combined_path}", "w") as f:
            f.write(new_content)

    for path, subdirs, files in os.walk(base_dir):
        for name in files:
            file_path = f"{path}/{name}"
            copy_path = path.replace(base_dir, copy_dir)
            
            if file_path not in special_files:
                os.makedirs(copy_path, exist_ok=True)
                shutil.copyfile(f"{path}/{name}", f"{copy_path}/{name}")


if __name__ == '__main__':
    args = get_args()
    
    with open(os.path.join(args.train_test_list_path, f"train_{args.pl}.txt"), "r") as f:
        train_list = f.read().split('\n')

    with open(os.path.join(args.train_test_list_path, f"test_{args.pl}.txt"), "r") as f:
        test_list = f.read().split('\n')


    for project_link in tqdm(train_list):
        project_link = project_link.split('\t')[0]
        if project_link.endswith('/'):
            project_link = project_link[:-1]
        *_, org, project = project_link.split('/')
        filepairs_path = os.path.join(args.output_dir, args.pl, 'DeduplicatedFilePairs', 
                                      'filepairs_' + org + '__' + project + '.json')
        filepairs_df =  pd.read_json(filepairs_path)       
        copy_with_concat(args.repo_dir, args.train_dir, args.pl, org, project, filepairs_df)

    if args.test_dir:
        for project_link in tqdm(test_list):
            project_link = project_link.split('\t')[0]
            if project_link.endswith('/'):
                project_link = project_link[:-1]
            *_, org, project = project_link.split('/')
            filepairs_path = os.path.join(args.output_dir, args.pl, 'FilePairs', 'filepairs_' + org + '__' + project + '.json')
            filepair_df = pd.read_json(filepairs_path)
            copy_with_concat(args.repo_dir, args.test_dir, args.pl, org, project, filepairs_df)
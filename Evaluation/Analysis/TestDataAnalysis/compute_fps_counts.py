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
sys.path.append('../')
from TestFramework.file_utils import *

def compute_fp_counts(curr_data, language, output_dir):
    total_fps_filtered = 0
    total_fps = 0
    for org in curr_data:
        for project in curr_data[org]:
            filepairs_path = os.path.join(output_dir, language, 'FilePairs', 'filepairs_' + org + '__' + project + '.json')
            with open(filepairs_path, "r") as f:
                file_pairs = json.load(f)

            total_fps += len(file_pairs["code_filename"])
            for i in range(len(file_pairs["code_filename"])):
                source_fn = file_pairs["code_filename"][i]
                test_fn = file_pairs["test_filename"][i]
                try:
                    code_non_trivial = filter_file_java(source_fn) if language == "java" else 3 # for python there can be files without methods still tested
                    test_non_trivial = filter_file_java(test_fn) if language == "java" else filter_file_python(test_fn)


                    if test_non_trivial > 1 and code_non_trivial > 1:
                        total_fps_filtered += 1
                except Exception as e:
                    #print(e)
                    pass

    print(total_fps)
    return total_fps_filtered


def compute_fp_arr(curr_data, language, output_dir):
    fps_arr = []
    for org in curr_data:
        for project in curr_data[org]:
            filepairs_path = os.path.join(output_dir, language, 'FilePairs', 'filepairs_' + org + '__' + project + '.json')
            with open(filepairs_path, "r") as f:
                file_pairs = json.load(f)

            curr_fp_filtered = 0
            for i in range(len(file_pairs["code_filename"])):
                source_fn = file_pairs["code_filename"][i]
                test_fn = file_pairs["test_filename"][i]
                try:
                    code_non_trivial = filter_file_java(source_fn) if language == "java" else 3 # for python there can be files without methods still tested
                    test_non_trivial = filter_file_java(test_fn) if language == "java" else filter_file_python(test_fn)


                    if test_non_trivial > 1 and code_non_trivial > 1:
                        curr_fp_filtered += 1
                except Exception as e:
                    #print(e)
                    pass
            fps_arr.append(curr_fp_filtered)
            

    return sorted(fps_arr)

if __name__ == '__main__':
    repo_dir = sys.argv[1] if len(sys.argv) > 1 else '/data/GitHubMining/RawDataSample/'
    train_test_output_dir = sys.argv[2] if len(sys.argv) > 2 else '/data/GitHubMining'
    output_dir = sys.argv[3] if len(sys.argv) > 3 else '/data/GitHubMining/RawDataSampleOutput/'

    with open(os.path.join(train_test_output_dir, f"test_exec_filtered.json"), "r") as f:
        train_test_filtered = json.load(f)

    with open(os.path.join(train_test_output_dir, "TestFramework", f"python_filepairs.json"), "r") as f:
        python_fps = json.load(f)

    total_fps_py = compute_fp_counts(train_test_filtered["python"], "python", output_dir)
    print(total_fps_py)
    total_fps_java = compute_fp_counts(train_test_filtered["java"], "java", output_dir)
    print(total_fps_java)

    arr = compute_fp_arr(python_fps, "python", output_dir)
    print(arr)
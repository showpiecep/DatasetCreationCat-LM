import os
import sys
import time
import random
import json
from tqdm import tqdm
import sentencepiece as spm
import pandas as pd
random.seed(12)

def load_filepair_data(filepath):
    with open(filepath) as json_data:
        data = json.load(json_data)
        data.pop('num_tokens_codefile', None)
        data.pop('num_tokens_testfile', None)
    df = pd.DataFrame.from_dict(data, orient='columns')
    return df


# get all file paths in the project
def get_project_filepaths(project_dir):
    all_project_file_paths = list()
    for (dirpath, _, filenames) in os.walk(project_dir):
        all_project_file_paths += [os.path.join(dirpath, file) for file in filenames]
    return all_project_file_paths


def sanitize(text):
    # Set up reserved tokens.
    SPACE_TOKEN = '▁'  # Note: not a regular underscore, but the SPM unicode symbol for a space
    TAB_TOKEN = chr(1)  # Assign rarely used ASCII chars for tabs and newlines. Can also pick rare unicode characters.
    NEWLINE_TOKEN = chr(2)
    text = text.replace('\n', NEWLINE_TOKEN)
    text = text.replace('\t', TAB_TOKEN)
    text = text.replace(' ', SPACE_TOKEN)
    return text


sp = spm.SentencePieceProcessor(model_file=f'vocabulary_10l.model')
def get_num_tokens(filename):
    num_tokens = -1
    with open(filename, errors='ignore') as f:
        file_content = f.read()
        num_tokens = len(sp.encode(sanitize(file_content)))
    return num_tokens


def get_metadata_after_dedup(repos_dir, pl, org, project, output_dir):
    after_metadata_dir = os.path.join(output_dir, pl, 'DeduplicatedMetaData/')
    os.makedirs(after_metadata_dir, exist_ok=True)

    project_dir = os.path.join(repos_dir, pl, org, project)
    metadata_filename = 'metadata_' + org + '__' + project + '.json'

    try:
        all_project_file_paths = get_project_filepaths(project_dir)
        metadata_df = pd.DataFrame(index=list(range(len(all_project_file_paths))), columns=['organization', 'project', 'filename', 'file_type'])
        metadata_df['organization'] = [org]*len(all_project_file_paths)
        metadata_df['project'] = [org]*len(all_project_file_paths)
        metadata_df['filename'] = all_project_file_paths
        metadata_df['file_type'] = metadata_df['filename'].apply(lambda x: 'test' if 'test' in x.lower() else 'code')
        metadata_df['num_tokens'] = metadata_df['filename'].apply(get_num_tokens)
        metadata_df.to_json(os.path.join(after_metadata_dir, metadata_filename), orient='records')       
        # seg fault for python/361way/python/
        # https://github.com/pandas-dev/pandas/issues/14256
    except Exception as e:
        print("Exception getting metadata", org, project, e)
        

def get_filepairs_after_dedup(repos_dir, pl, org, project, output_dir):
    
    before_filepairs_dir = os.path.join(output_dir, pl, 'FilePairs')
    after_filepairs_dir = os.path.join(output_dir, pl, 'DeduplicatedFilePairs/')
    project_dir = os.path.join(repos_dir, pl, org, project)
    filepairs_filename = 'filepairs_' + org + '__' + project + '.json'

    try:
        all_project_file_paths = get_project_filepaths(project_dir)
        filepairs_df = load_filepair_data(os.path.join(before_filepairs_dir, filepairs_filename))

        filepairs_df = filepairs_df[['code_filename', 'test_filename']]

        filepairs_df['code_filename'] = filepairs_df['code_filename'].apply(lambda x: x.replace('/CurrentState/','/CurrentStateDeduplicated/'))
        filepairs_df['test_filename'] = filepairs_df['test_filename'].apply(lambda x: x.replace('/CurrentState/','/CurrentStateDeduplicated/'))
            
        filepairs_df['code_exists_after_dedup'] = filepairs_df['code_filename'].apply(lambda x: x in all_project_file_paths)
        filepairs_df['test_exists_after_dedup'] = filepairs_df['test_filename'].apply(lambda x: x in all_project_file_paths)        
        filepairs_df = filepairs_df[(filepairs_df['code_exists_after_dedup'] == True) & (filepairs_df['test_exists_after_dedup'] == True)]
        filepairs_df = filepairs_df.reset_index()
        
        filepairs_df = filepairs_df[['code_filename', 'test_filename']]
        filepairs_df['code_tokens'] = filepairs_df['code_filename'].apply(get_num_tokens)
        filepairs_df['test_tokens'] = filepairs_df['test_filename'].apply(get_num_tokens)
        
        filepairs_df['sum_tokens'] = filepairs_df['code_tokens'] + filepairs_df['test_tokens']
        filepairs_df.to_json(os.path.join(after_filepairs_dir, filepairs_filename), orient='records')
    
    except Exception as e:
        print("Exception getting file pairs", org, project, e)
        

if __name__ == '__main__':

    project_path = sys.argv[1] if len(sys.argv) > 1 else '/data/GitHubMining/CurrentState/python/pandas-dev/pandas/'
    pl = sys.argv[2] if len(sys.argv) > 2 else 'python'
    
    if project_path.endswith('/'):
        project_path = project_path[:-1]
    *_, org, project = project_path.split('/')

    print(f"Processing {pl}/{org}/{project}")

    repos_dir = './data/GitHubMining/CurrentStateDeduplicated/'
    output_dir = './data/GitHubMining/Output/'

    os.makedirs(output_dir, exist_ok=True)
   
    get_metadata_after_dedup(repos_dir, pl, org, project, output_dir)
    get_filepairs_after_dedup(repos_dir, pl, org, project, output_dir)
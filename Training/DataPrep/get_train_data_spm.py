import os
import time
import random
from tqdm import tqdm
random.seed(12)

def get_sample_lines(file_path):
    samples = []
    k = 10
    with open(file_path, errors='ignore') as f:
        file_content = f.read() 
        lines = file_content.split('\n')

        while len(samples) != k:
            index = random.randrange(len(lines))
            line = lines[index]
            if len(line.strip()) > 0:
                samples.append(line)
    return samples


def get_spm_train_data(input_dir, output_filepath):
    
    output_file = open(output_filepath, 'a') 
    count_projects = 0
    count_files = 0
    count_empty_projects = 0
    for pl in ['python', 'java']:
        print(f'Sampling {pl} files')
        repos_list_path = f'../GitHubMining/{pl}-top-repos.txt'

        with open(repos_list_path) as f:
            repo_links_list = f.read().split('\n')
        
        for project_link in tqdm(repo_links_list):
            project_link = project_link.split('\t')[0]
            if project_link.endswith('/'):
                project_link = project_link[:-1]
            *_, org, project = project_link.split('/')
        
            project_dir = os.path.join(input_dir, pl, org, project)
            count_projects += 1
            # get all file paths in the project
            all_project_file_paths = list()
            for (dirpath, _, filenames) in os.walk(project_dir):
                all_project_file_paths += [os.path.join(dirpath, file) for file in filenames]
            
            count_files += len(all_project_file_paths)
            if len(all_project_file_paths) == 0:
                count_empty_projects += 1

            for file_path in all_project_file_paths:
                samples = get_sample_lines(file_path)
                output_file.write('\n'.join(samples) + '\n')

        print(f'count_projects {pl}: {count_projects}')
        print(f'count_empty_projects {pl}: {count_empty_projects}')
        print(f'count_files {pl}: {count_files}')
                
    print(f'count_projects: {count_projects}')
    print(f'count_empty_projects: {count_empty_projects}')
    print(f'count_files: {count_files}')
            

if __name__ == '__main__':

    input_dir = '/data/GitHubMining/CurrentStateDeduplicated/'
    output_filepath = '/data/GitHubMining/spm_train_data_10l.txt'
    #output_filepath = './spm_train_data.txt'

    get_spm_train_data(input_dir, output_filepath)

  
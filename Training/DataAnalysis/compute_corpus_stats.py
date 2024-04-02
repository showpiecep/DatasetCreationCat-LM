import os
import json
import sys
import traceback

STATS_COLUMNS = ('organization', 'project', 'filename', 'file_type', 'preamble_num_tokens')

def get_num_tokens_preamble(filename):
    num_tokens = -1
    with open(filename, errors='ignore') as f:
        file_content = f.read()
        file_lines = file_content.split("\n")
        root = ast.parse(file_content)
        classes = [(n.lineno, n.end_lineno) for n in root.body if isinstance(n, ast.ClassDef)]
        num_tokens = get_num_tokens_start_of_file(file_lines)
        for class_info in classes:
            num_tokens += get_num_tokens_class(class_info, file_lines)
    return num_tokens


def get_num_tokens_start_of_file(file_lines):
    found_method_or_class = False
    num_tokens = 0
    for line in file_lines:
        line = line.strip()
        if line.startswith("#"):
            continue
        if line.startswith("def") or line.startswith("class"):
            break
        num_tokens += len(re.split('\s+', line))
    return num_tokens

def get_num_tokens_class(class_info, file_lines):
    lines_cut = file_lines[class_info[0]-1:]
    num_tokens = 0
    for line in lines_cut:
        line = line.strip()
        if line.startswith("def") and not line.startswith("def __init__"):
            break
        num_tokens += len(re.split('\s+', line))
    return num_tokens

# TODO: currently only getting scores for paired files, extend to all files
def main(repo_dir, file_pairs_dir, org, project):
    project_path = os.path.join(repo_dir, org, project)
    file_pairs_path = os.path.join(output_dir, 'FilePairs', 'filepairs_' + org + '__' + project + '.json')
    corpus_stats_path = os.path.join(output_dir, 'CorpusStats', 'stats_' + org + '__' + project + '.json')

    if os.path.exists(corpus_stats_path):
        print(f"Extracted stats already!!!")
        return

    corpus_stats = {key: [] for key in STATS_COLUMNS}
    if os.path.exists(file_pairs_path):
        with open(file_pairs_path, "r") as f:
            file_pairs = json.load(f)
        try:
            # get all files
            for code_file in file_pairs["code_filename"]:
                code_file_path = os.path.join(project_path, code_file.split(f"{org}/{project}/")[1])
                num_preamble_tokens = get_num_tokens_preamble(code_file_path)
                corpus_stats['organization'].append(org)
                corpus_stats['project'].append(project)
                corpus_stats['filename'].append(code_file_path)
                corpus_stats['file_type'].append('code')
                corpus_stats['preamble_num_tokens'].append(num_preamble_tokens)
            for test_file in file_pairs["test_filename"]:
                test_file_path = os.path.join(project_path, test_file.split(f"{org}/{project}/")[1])
                num_preamble_tokens = get_num_tokens_preamble(test_file_path)
                corpus_stats['organization'].append(org)
                corpus_stats['project'].append(project)
                corpus_stats['filename'].append(test_file_path)
                corpus_stats['file_type'].append('test')
                corpus_stats['preamble_num_tokens'].append(num_preamble_tokens)
            
            with open(corpus_stats_path, 'w') as f:
                json.dump(corpus_stats, f)               
        
        except Exception as e:
            print("Exception extracting file pairs", org, project, e)
            traceback.print_exc()
    else:
        print(f"No metadata for project {project}, org {org}")


if __name__ == '__main__':
    repo_dir = sys.argv[1] if len(sys.argv) > 1 else '/data/GitHubMining/CurrentState/python/'
    output_dir = sys.argv[2] if len(sys.argv) > 2 else '/data/GitHubMining/Output/python/'
    project_path = sys.argv[3] if len(sys.argv) > 3 else '/data/GitHubMining/CurrentState/python/dabeaz/python-cookbook/'
    
    if project_path.endswith('/'):
        project_path = project_path[:-1]
    *_, org, project = project_path.split('/')

    print("Processing {0}/{1}".format(org, project))
    main(repo_dir, output_dir, org, project)

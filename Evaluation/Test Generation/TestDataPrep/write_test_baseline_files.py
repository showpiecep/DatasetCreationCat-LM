import sys
from tree_sitter import Language, Parser
import os
import json
import shutil

# Load tree-sitter-java grammar
Language.build_library(
    'build/my-languages.so',
    ['tree-sitter-java']
)
JAVA_LANGUAGE = Language('build/my-languages.so', 'java')
parser = Parser()
parser.set_language(JAVA_LANGUAGE)

def load_data(filename):
    with open(filename, errors='ignore') as f_in:
        file_content = f_in.read()
    return file_content

def find_test_methods(tree):
    test_methods = []
    class_declaration = None
    for node in tree.root_node.children:
        if node.type == 'class_declaration':
            class_declaration = node
            for child in node.children[-1].children:
                if child.type == 'method_declaration':
                    if any(x.type == 'modifiers' and "@Test" in str(x.text) for x in child.children):
                        test_methods.append(child)
                    elif any(x.type == 'identifier' and "test" in str(x.text).lower() for x in child.children):
                        test_methods.append(child)

    return test_methods, class_declaration

def extract_code_from_tests(java_code):
    tree = parser.parse(bytes(java_code, 'utf8'))
    test_methods, class_declaration = find_test_methods(tree)
    test_lines = []
    method_lines = []
    if len(test_methods) > 0:
        for test_method in test_methods:
            start_line = test_method.start_point[0]
            end_line = test_method.end_point[0] + 1

            code_lines = java_code.split('\n')
            method_lines.append("\n".join(code_lines[start_line:end_line]))
            test_lines.append('\n'.join(code_lines[:end_line]))
    return test_lines, method_lines

def write_code_lines_to_files(code_lines, output_path, eof_snippet_path, test_filename):
    eof_data = load_data(eof_snippet_path)
    for i, lines in enumerate(code_lines):
        with open(os.path.join(output_path, f"{test_filename}_{i+1}.java"), 'w') as f:
            f.write(lines)
            f.write(eof_data)
            f.write("\n}")

def main(filepairs):    
    print(filepairs)
    for org in filepairs:
        print(f'org {org}')
        for project in filepairs[org]:
            print(f'\tproject {project}')
            for fp_index, filepair in enumerate(filepairs[org][project]):
                print(f'\t\tfp_index {fp_index}')
                test_filepath = filepair[1]                
                output_path = f"/data/GitHubMining/Generated_TestOutputs/java/{org}/{project}/filepair{fp_index}/incremental_test_files"
                eof_sippet_filepath = f"/data/GitHubMining/Generated_TestOutputs/java/{org}/{project}/filepair{fp_index}/eof_snippet.txt"
                baselines_path = f"/data/GitHubMining/Generated_TestOutputs/java/{org}/{project}/filepair{fp_index}"

                if os.path.exists(output_path):
                    shutil.rmtree(output_path)
                
                os.makedirs(output_path, exist_ok=True)
                test_filename = test_filepath.split('/')[-1][:-5]

                print(f'\t\t\ttest_filepath: {test_filepath}')
                print(f'\t\t\toutput_path: {output_path}')
                with open(test_filepath, 'r') as f:
                    java_code = f.read()
                code_lines, method_lines = extract_code_from_tests(java_code)
                
                with open(os.path.join(baselines_path, f"{test_filename}_first_test_text.java"), 'w') as f:
                    f.write(method_lines[0])
                
                with open(os.path.join(baselines_path, f"{test_filename}_last_test_text.java"), 'w') as f:
                    f.write(method_lines[-1])
                write_code_lines_to_files(code_lines, output_path, eof_sippet_filepath, test_filename)
            print()

if __name__ == "__main__":
    aggregation_dir = sys.argv[1] if len(sys.argv) > 1 else '/data/GitHubMining/TestFramework/'
    
    java_fps_path = os.path.join(aggregation_dir, "java_filepairs.json")

    with open(java_fps_path, "r") as f:
        java_fps = json.load(f)

    main(java_fps)

            
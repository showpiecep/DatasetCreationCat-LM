import sys
import pandas as pd
import os
import json

def add_extra_brace(source_fp, last_test_closing_code_fp, dest_fp):
    with open(source_fp, 'r') as source:
        with open(dest_fp, 'w') as dest:
            for line in source:
                dest.write(line)
            with open(last_test_closing_code_fp, 'r') as f:
                for line in f:
                    dest.write(line)
            dest.write("}")


def add_source_context(source_code_fp, source_fp, last_test_closing_code_fp):
    new_lines = ""
    with open(source_code_fp, 'r') as source_code:
        with open(source_fp, 'r') as source:
            for line in source_code:
                new_lines += line
            new_lines += "\n<|codetestpair|>\n"
            for line in source:
                new_lines += line
    with open(last_test_closing_code_fp, 'r') as f:
        for line in f:
            new_lines += line

    return new_lines


def read_file(filepath, last_test_closing_code_fp):
    new_lines = ""
    with open(filepath, 'r') as f:
        for line in f:
            new_lines += line
    
    with open(last_test_closing_code_fp, 'r') as f:
        for line in f:
            new_lines += line
    
    return new_lines

def get_context_and_baseline_files(code_filepath, test_filepath, output_path): 
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    code_filename = code_filepath.split('/')[-1][:-5]
    test_filename = test_filepath.split('/')[-1][:-5]

    preamble_no_context_fp = "preamble_nocontext.java"
    last_test_no_context_fp = "last_test_nocontext.java"
    extra_test_no_context_fp = "extratest_nocontext.java"
    last_test_closing_code_fp = "last_test_closing_code.java"
    first_test_no_context_fp = "first_test_nocontext.java"

    os.system(f"python3 get_preamble_context.py {test_filepath} {preamble_no_context_fp}")
    os.system(f"python3 remove_last_method.py {test_filepath} {last_test_no_context_fp}")
    os.system(f"python3 remove_final_braces.py {test_filepath} {extra_test_no_context_fp}")
    os.system(f"python3 get_last_test_closing_code.py {test_filepath} {last_test_closing_code_fp}")
    os.system(f"python3 remove_after_first_method.py {test_filepath} {first_test_no_context_fp}")
    

    preamble_baseline_fp = f"{output_path}/{test_filename}_preamble_baseline.java"
    whole_file_baseline_fp = f"{output_path}/{test_filename}_baseline.java"
    without_last_test_baseline_fp = f"{output_path}/{test_filename}_without_last_test_baseline.java"
    first_method_baseline_fp = f"{output_path}/{test_filename}_first_test_baseline.java"
    last_test_closing_code_baseline_fp = f"{output_path}/eof_snippet.txt"

    os.system(f"cp {test_filepath} {whole_file_baseline_fp}")
    os.system(f"cp {last_test_closing_code_fp} {last_test_closing_code_baseline_fp}")
    add_extra_brace(preamble_no_context_fp, last_test_closing_code_fp, preamble_baseline_fp)
    add_extra_brace(last_test_no_context_fp, last_test_closing_code_fp, without_last_test_baseline_fp)
    add_extra_brace(first_test_no_context_fp, last_test_closing_code_fp, first_method_baseline_fp)

    # with code context
    output = add_source_context(code_filepath, preamble_no_context_fp, last_test_closing_code_fp) + '<|end_prompt|>\n'
    output += add_source_context(code_filepath, last_test_no_context_fp, last_test_closing_code_fp) + '<|end_prompt|>\n'
    output += add_source_context(code_filepath, extra_test_no_context_fp, last_test_closing_code_fp) + '<|end_prompt|>\n'
    
    # without code context
    output += read_file(preamble_no_context_fp, last_test_closing_code_fp) + '\n<|end_prompt|>\n'
    output += read_file(last_test_no_context_fp, last_test_closing_code_fp) + '\n<|end_prompt|>\n'
    output += read_file(extra_test_no_context_fp, last_test_closing_code_fp) + '\n<|end_prompt|>\n'
    print(output)

    output_context_filename = f"{output_path}/{code_filename}-{test_filename}_contexts.txt"
    with open(output_context_filename, 'w') as f_out:
        f_out.write(output)


def main(filepairs):
    
    print(filepairs)
    for org in filepairs:
        print(f'org {org}')
        for project in filepairs[org]:
            print(f'\tproject {project}')
            for fp_index, filepair in enumerate(filepairs[org][project]):
                print(f'\t\tfp_index {fp_index}')
                code_filepath = filepair[0]
                test_filepath = filepair[1]
                print(f'\t\tcode_filepath {code_filepath}')
                print(f'\t\ttest_filepath {test_filepath}')
                
                output_path = f"/data/GitHubMining/Generated_TestOutputs/java/{org}/{project}/filepair{fp_index}"

                print(f'\t\t\tcode_filepath: {code_filepath}')
                print(f'\t\t\ttest_filepath: {test_filepath}')
                print(f'\t\t\toutput_path: {output_path}')
                get_context_and_baseline_files(code_filepath, test_filepath, output_path)
            print()

if __name__ == "__main__":
    aggregation_dir = sys.argv[1] if len(sys.argv) > 1 else '/data/GitHubMining/TestFramework/'
    
    java_fps_path = os.path.join(aggregation_dir, "java_filepairs.json")

    with open(java_fps_path, "r") as f:
        java_fps = json.load(f)

    main(java_fps)

            
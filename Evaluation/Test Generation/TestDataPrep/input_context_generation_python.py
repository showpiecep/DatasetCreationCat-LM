import os
import sys
import time
import traceback
import json
from ast_utils import get_python_program_graph, get_all_method_defs_from_graph

def get_preamble_context(method_defs, test_file_content):
    for method in method_defs:
        #print('method', method)
        if "test" in method:
            #print('found first test method', method)
            break
    first_test_method = method_defs[method]
    first_test_method_start_lineno = int(first_test_method['lineno'].split('-')[0])
    test_file_content = test_file_content.split('\n')
    context = '\n'.join(test_file_content[:first_test_method_start_lineno-1])
    #print('get_preamble_context\n',context)
    return context


def get_first_test_context(method_defs, test_file_content):
    for method in method_defs:
        #print('method', method)
        if "test" in method:
            #print('found first test method', method)
            break
    first_test_method = method_defs[method]
    first_test_method_end_lineno = int(first_test_method['lineno'].split('-')[1])
    test_file_content = test_file_content.split('\n')
    context = '\n'.join(test_file_content[:first_test_method_end_lineno])
    #print('get_first_test_context\n',context)
    return context


def get_extra_test_context(method_defs, test_file_content):
    #context = test_file_content
    last_method = method_defs[list(method_defs.keys())[-1]]
    last_method_end_lineno = int(last_method['lineno'].split('-')[1])
    test_file_content = test_file_content.split('\n')
    context = '\n'.join(test_file_content[:last_method_end_lineno])
    #print('get_extra_test_context\n',context)
    return context


def get_last_test_context(method_defs, test_file_content):
    if len(method_defs.keys()) > 1:
        last_but_one_method = method_defs[list(method_defs.keys())[-2]]
    else:
        print('get_last_test_context == get_preamble_context since len(method_defs.keys())=',len(method_defs.keys()))
        return get_preamble_context(method_defs, test_file_content)
    last_but_one_method_end_lineno = int(last_but_one_method['lineno'].split('-')[1])
    test_file_content = test_file_content.split('\n')
    context = '\n'.join(test_file_content[:last_but_one_method_end_lineno])
    #print('get_last_test_context\n',context)
    return context


def get_eof_snippet(method_defs, test_file_content):
    last_method = method_defs[list(method_defs.keys())[-1]]
    last_method_end_lineno = int(last_method['lineno'].split('-')[1])
    test_file_content = test_file_content.split('\n')
    eof_snippet = '\n'.join(test_file_content[last_method_end_lineno:])
    print(f'eof_snippet:\n {eof_snippet}')
    return eof_snippet


def get_incremental_test_files(method_defs, test_file_content, eof_snippet, test_filename, output_path):
    test_count = 1
    output_path = f'{output_path}/incremental_test_files/'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    test_file_content = test_file_content.split('\n')
    for method in method_defs:
        if "test" in method:
            method_end_lineno = int(method_defs[method]['lineno'].split('-')[1])
            context = '\n'.join(test_file_content[:method_end_lineno])
            context += '\n' + eof_snippet
            with open(f'{output_path}/{test_filename}_{test_count}.py', 'w') as f_out:
                f_out.write(context)
            test_count += 1
    print(f'\t\t\tnum_tests: {test_count}')


def get_first_test_method(method_defs, test_file_content, test_filename, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    test_file_content = test_file_content.split('\n')
    for method in method_defs:
        if "test" in method:
            method_body = method_defs[method]['body']            
            with open(f'{output_path}/{test_filename}_first_test_text.py', 'w') as f_out:
                f_out.write(method_body)
            break
    print(f'\t\t\tfirst test:\n {method_body}')

    

def get_last_test_method(method_defs, test_file_content, test_filename, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    test_file_content = test_file_content.split('\n')
    last_method = method_defs[list(method_defs.keys())[-1]]
    method_body = last_method['body']       
    with open(f'{output_path}/{test_filename}_last_test_text.py', 'w') as f_out:
        f_out.write(method_body)
    print(f'\t\t\tlast test:\n {method_body}')


def get_context_and_baseline_files(code_filepath, test_filepath, output_path): 
    code_filename = code_filepath.split('/')[-1][:-3]
    test_filename = test_filepath.split('/')[-1][:-3]
    output_context_filename = f"{output_path}/{code_filename}-{test_filename}_contexts.txt"
    output_baseline_preamble_filename = f"{output_path}/{test_filename}_preamble_baseline.py"
    output_baseline_firsttest_filename = f"{output_path}/{test_filename}_first_test_baseline.py"
    output_baseline_lasttest_filename = f"{output_path}/{test_filename}_without_last_test_baseline.py"
    output_code_filename =f"{output_path}/{code_filename}.py"
    output_baseline_test_filename = f"{output_path}/{test_filename}_baseline.py"
    output_eof_snippet_filename = f"{output_path}/eof_snippet.txt"
    
    try:
        test_file_graph, test_file_content = get_python_program_graph(test_filepath)
        test_method_defs = get_all_method_defs_from_graph(test_file_graph, test_file_content)
        '''
        for method in method_defs:
            print(method)
            print(method_defs[method])
            print('\n')
        '''
    except Exception as e:
        print("Exception getting code graph in",test_filename, "--", e)
        traceback.print_exc()

    preamble_context = get_preamble_context(test_method_defs, test_file_content)
    
    first_test_context = get_first_test_context(test_method_defs, test_file_content)
    
    last_test_context = get_last_test_context(test_method_defs, test_file_content)
    
    extra_test_context = get_extra_test_context(test_method_defs, test_file_content)
    
    eof_snippet = get_eof_snippet(test_method_defs, test_file_content)
    
    get_incremental_test_files(test_method_defs, test_file_content, eof_snippet, test_filename, output_path)
    
    get_first_test_method(test_method_defs, test_file_content, test_filename, output_path)
    
    get_last_test_method(test_method_defs, test_file_content, test_filename, output_path)
    
    
    with open(code_filepath, errors='ignore') as f_in:
        code_file = f_in.read()

    # with code context
    output = code_file + '\n' + "<|codetestpair|>\n" + preamble_context + '\n<|end_prompt|>\n'
    output += code_file + '\n' + "<|codetestpair|>\n" + last_test_context + '\n<|end_prompt|>\n'
    output += code_file + '\n' + "<|codetestpair|>\n" + extra_test_context + '\n<|end_prompt|>\n'
    
    # without code context
    output += preamble_context + '\n<|end_prompt|>\n'
    output += last_test_context + '\n<|end_prompt|>\n'
    output += extra_test_context + '\n<|end_prompt|>\n'
    
    print(f'\t\t\t\toutput_context: {output}')
    # create output path
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # save context
    with open(output_context_filename, 'w') as f_out:
        f_out.write(output)

    # save baseline files 
    #eof snippet
    with open(output_eof_snippet_filename, 'w') as f_out:
        f_out.write(eof_snippet)    
    # code file
    with open(output_code_filename, 'w') as f_out:
        f_out.write(code_file)
    # just preamble
    with open(output_baseline_preamble_filename, 'w') as f_out:
        f_out.write(preamble_context)
    # preamble + first test
    first_test_context += '\n' + eof_snippet
    with open(output_baseline_firsttest_filename, 'w') as f_out:
        f_out.write(first_test_context)
    # all but last test
    last_test_context += '\n' + eof_snippet
    with open(output_baseline_lasttest_filename, 'w') as f_out:
        f_out.write(last_test_context)
    # all tests
    extra_test_context += '\n' + eof_snippet
    with open(output_baseline_test_filename, 'w') as f_out:
        f_out.write(extra_test_context)
    


def main():
    with open('/data/GitHubMining/TestFramework/python_filepairs.json') as f_in:
        filepairs = json.load(f_in)
    
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
                
                output_path = f"/data/GitHubMining/Generated_TestOutputs/python/{org}/{project}/filepair{fp_index}"
                print(f'\t\t\tcode_filepath: {code_filepath}')
                print(f'\t\t\ttest_filepath: {test_filepath}')
                print(f'\t\t\toutput_path: {output_path}')
                get_context_and_baseline_files(code_filepath, test_filepath, output_path)
                
            print()

    


if __name__ == '__main__':
    main()    
    
# sudo python3 -u input_context_generation_python.py | sudo tee output_python_contexts.txt
# sudo python3 -u input_context_generation_python.py | sudo tee output_python_incremental_tests.txt
# sudo python3 -u input_context_generation_python.py | sudo tee output_python_gold_tests.txt

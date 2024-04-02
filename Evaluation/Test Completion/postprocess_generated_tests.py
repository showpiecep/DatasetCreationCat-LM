import os
import sys
import time
import json
import traceback
import re


def load_data(filename):
    with open(filename, errors='ignore') as f_in:
        file_content = f_in.read()
    return file_content


def get_first_statement(text):
    stripped_text = text.replace("}", "").strip()

    if stripped_text.startswith('package') or stripped_text.startswith('import') or stripped_text.startswith('public class'):
        print('\t\t\t\t\t\tERROR: new file, no statement generated')
        return ''
    
    first_statement =  f"{text.split(';')[0]};".strip()

    matches = re.findall(r'(["\'])(.*?)\1', first_statement)
    for match in matches:
        first_statement = first_statement.replace(f"{match[0]}{match[1]}{match[0]}", '"STR"')
    
    return first_statement

def postprocess_outputs(code_filepath, test_filepath, generation_output_path, num_samples):
    code_filename = code_filepath.split('/')[-1][:-5]
    test_filename = test_filepath.split('/')[-1][:-5]
    generations_file = f"{generation_output_path}/{test_filename}-{code_filename}_outputs.txt"
    
    file_content = load_data(generations_file)
    output_samples = file_content.split('\n')
    test_statements_mapping = {}
    unique_statements = set()
    count = 0
    # get the generated tests
    for i, sample in enumerate(output_samples):
        if i % num_samples == 0:
            unique_statements = set()

        if sample == '':
            continue
        # print('for sample ',i)
        output_dict = json.loads(sample)
        generated_text = output_dict['text'] 
        first_statement = get_first_statement(generated_text) 
        # # if generated test is a duplicate
        
        if "".join(first_statement) in unique_statements:
            continue
        else:
            test_statements_mapping[i] = first_statement
            unique_statements.add("".join(first_statement))
            count += 1
    
    with open(f"{generation_output_path}/teco_statements.json" , 'w') as f_out:
        json.dump(test_statements_mapping, f_out)

    print(f'\t\t\t\tSTATS:{generation_output_path} generated:{len(output_samples)} unique:{count}')    
    return test_statements_mapping




def main(teco_completions_path, temp, num_samples, fps_path, teco_gold_statements_path, output_path):
    # tokenizer = SubtokenizerBPE(AutoTokenizer.from_pretrained("/code/teco/_work/subtokenizer/codet5"))

    with open(fps_path, 'r') as f_in:
        filepairs = json.load(f_in)


    """
    code_filepath= "/data/GitHubMining/RawDataSample/python/elarivie/pyReaderWriterLock/readerwriterlock/rwlock_async.py"
    test_filepath= "/data/GitHubMining/RawDataSample/python/elarivie/pyReaderWriterLock/tests/test_rwlock_async.py"
    output_path= "/data/GitHubMining/Generated_TestOutputs/python/elarivie/pyReaderWriterLock/filepair0/t0.2_n10"
    eof_sippet_filepath= "/data/GitHubMining/Generated_TestOutputs/python/elarivie/pyReaderWriterLock/filepair0/eof_snippet.txt"
    postprocess_outputs(code_filepath, test_filepath, output_path, eof_sippet_filepath,  pl)
    """
    #print(filepairs)
    error_list = []
    filepairs_map = {}
    for filepair in filepairs:
        fp_index = filepair["id"]
        print(f'\t\tfp_index {fp_index}')
        code_filepath = filepair["source_file"]
        test_filepath = filepair["test_file"]
        print(f'\t\tcode_filepath {code_filepath}')
        print(f'\t\ttest_filepath {test_filepath}')
        generation_output_path = f"{teco_completions_path}/{fp_index}/t{temp}_n{num_samples}"
        
        code_filename = code_filepath.split('/')[-1][:-5]
        test_filename = test_filepath.split('/')[-1][:-5]

        generations_file = f"{generation_output_path}/{test_filename}-{code_filename}_outputs.txt"

        print(f'\t\t\tcode_filepath: {code_filepath}')
        print(f'\t\t\ttest_filepath: {test_filepath}')
        print(f'\t\t\toutput_path: {generation_output_path}')
        '''
        mypath = f"/data/GitHubMining/Generated_TestOutputs/python/{org}/{project}/filepair{fp_index}/t{temp}_n{num_samples}"
        files = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
        for file in files:
            #if file.startswith('t0.2_n10') and file.endswith('.py'):
            if file.endswith('.py'):
                os.remove(os.path.join(mypath, file))
                print(f'removed {file}')                
        '''
        try:
            filepairs_map[fp_index] = postprocess_outputs(code_filepath, test_filepath, generation_output_path, num_samples)
        except Exception as e:
            error_list.append(f"{generations_file}\n")
            print("Exception postprocessing outputs", generation_output_path, e)
            traceback.print_exc()
        
    with open(f"{output_path}/teco_preds_{temp}.json", 'w') as f_out:
        json.dump(filepairs_map, f_out)

    with open(f"/data/GitHubMining/Generated_TestOutputs/errors/teco_errors_{temp}.txt", 'w') as f_out:
        f_out.writelines(error_list)

    with open(teco_gold_statements_path, 'r') as f_in:
        gold_stmts = f_in.readlines()
        gold_stmts_map = {}
        for ind, gold_stmt in enumerate(gold_stmts):
            gold_stmts_map[ind] = json.loads(gold_stmt)
    
    with open(f"{output_path}/teco_gold.json", 'w') as f_out:
        json.dump(gold_stmts_map, f_out)

if __name__ == '__main__':
    teco_completions_path = sys.argv[1] if len(sys.argv) > 1 else "/data/GitHubMining/Generated_TestOutputs/TecoContexts"
    temp = sys.argv[2] if len(sys.argv) > 2 else 0.2
    num_samples = sys.argv[3] if len(sys.argv) > 3 else 10
    fps_path = sys.argv[4] if len(sys.argv) > 4 else "/data/GitHubMining/TestFramework/teco_fps.json"
    teco_gold_statements_path = sys.argv[5] if len(sys.argv) > 5 else "/code/teco/_work/setup/CSNm/eval-any-stmt/test/gold_stmts.jsonl"
    output_path = sys.argv[6] if len(sys.argv) > 6 else "/data/GitHubMining/TextMetrics/Teco"

    num_samples = int(num_samples)
    main(teco_completions_path, temp, num_samples, fps_path, teco_gold_statements_path, output_path)

#sudo python3 -u postprocess_generated_tests.py | sudo tee output_python_postprocess_test.txt
#sudo python3 -u postprocess_generated_tests.py | sudo tee output_python_postprocess_t0.2_n10_512.txt
#sudo python3 -u postprocess_generated_tests.py | sudo tee output_python_postprocess_t0.8_n10.txt
#sudo python3 -u postprocess_generated_tests.py | sudo tee output_java_postprocess_t0.2_n10.txt
#sudo python3 -u postprocess_generated_tests.py | sudo tee output_java_postprocess_t0.8_n10.txt

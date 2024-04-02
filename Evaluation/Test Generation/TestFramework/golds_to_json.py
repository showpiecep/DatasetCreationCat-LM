import os
import sys
import time
import json
import traceback
import re
from pygments_utils import tokenize_code

def main(completions_path, frameworks_path, pl, output_path):
    # tokenizer = SubtokenizerBPE(AutoTokenizer.from_pretrained("/code/teco/_work/subtokenizer/codet5"))

    #with open(f'/data/GitHubMining/TestFramework/{pl}_filepairs_old.json') as f_in:
    with open(f'{frameworks_path}/{pl}_filepairs.json') as f_in:
        filepairs = json.load(f_in)
    
    """
    code_filepath= "/data/GitHubMining/RawDataSample/python/elarivie/pyReaderWriterLock/readerwriterlock/rwlock_async.py"
    test_filepath= "/data/GitHubMining/RawDataSample/python/elarivie/pyReaderWriterLock/tests/test_rwlock_async.py"
    output_path= "/data/GitHubMining/Generated_TestOutputs/python/elarivie/pyReaderWriterLock/filepair0/t0.2_n10"
    eof_sippet_filepath= "/data/GitHubMining/Generated_TestOutputs/python/elarivie/pyReaderWriterLock/filepair0/eof_snippet.txt"
    postprocess_outputs(code_filepath, test_filepath, output_path, eof_sippet_filepath,  pl)
    """
    #print(filepairs)
    fp_golds = {}
    for org in filepairs:
        fp_golds[org] = {}
        print(f'org {org}')
        for project in filepairs[org]:
            fp_golds[org][project] = {}
            print(f'\tproject {project}')
            for fp_index, filepair in enumerate(filepairs[org][project]):
                fp_golds[org][project][fp_index] = {}
                print(f'\t\tfp_index {fp_index}')
                code_filepath = filepair[0]
                test_filepath = filepair[1]
                print(f'\t\tcode_filepath {code_filepath}')
                print(f'\t\ttest_filepath {test_filepath}')
                baseline_output_path = f"{completions_path}/{pl}/{org}/{project}/filepair{fp_index}"
                
                print(f'\t\t\tcode_filepath: {code_filepath}')
                print(f'\t\t\ttest_filepath: {test_filepath}')
                print(f'\t\t\toutput_path: {baseline_output_path}')
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
                    test_filename = test_filepath.split('/')[-1][:-5] if pl == 'java' else test_filepath.split('/')[-1][:-3]
                    extension = 'java' if pl == 'java' else 'py'
                    first_test_file = os.path.join(baseline_output_path, f"{test_filename}_first_test_text.{extension}")
                    last_test_file = os.path.join(baseline_output_path, f"{test_filename}_last_test_text.{extension}")
                    first_test = open(first_test_file).read()
                    last_test = open(last_test_file).read()
                    first_test_tokens = tokenize_code(first_test)
                    last_test_tokens = tokenize_code(last_test)
                    fp_golds[org][project][fp_index]['first_test_tokens'] = first_test_tokens
                    fp_golds[org][project][fp_index]['last_test_tokens'] = last_test_tokens
                except Exception as e:
                    print("Exception postprocessing outputs", baseline_output_path, e)
                    traceback.print_exc()
    
    with open(f'{output_path}/{pl}_filepairs_golds.json', 'w') as f_out:
        json.dump(fp_golds, f_out)

if __name__ == '__main__':
    completions_path = sys.argv[1] if len(sys.argv) > 1 else "/data/GitHubMining/Generated_TestOutputs"
    pl = sys.argv[2] if len(sys.argv) > 2 else 'java'
    frameworks_path = sys.argv[3] if len(sys.argv) > 3 else "/data/GitHubMining/TestFramework"
    output_path = sys.argv[4] if len(sys.argv) > 4 else "/data/GitHubMining/TextMetrics/TestGeneration"

    main(completions_path, frameworks_path, pl, output_path)

#sudo python3 -u postprocess_generated_tests.py | sudo tee output_python_postprocess_test.txt
#sudo python3 -u postprocess_generated_tests.py | sudo tee output_python_postprocess_t0.2_n10_512.txt
#sudo python3 -u postprocess_generated_tests.py | sudo tee output_python_postprocess_t0.8_n10.txt
#sudo python3 -u postprocess_generated_tests.py | sudo tee output_java_postprocess_t0.2_n10.txt
#sudo python3 -u postprocess_generated_tests.py | sudo tee output_java_postprocess_t0.8_n10.txt

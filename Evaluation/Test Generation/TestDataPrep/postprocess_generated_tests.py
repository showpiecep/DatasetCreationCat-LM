import os
import sys
import time
import json
import traceback
import re
from comby import Comby

def load_data(filename):
    with open(filename, errors='ignore') as f_in:
        file_content = f_in.read()
    return file_content


def get_first_method(text, pl):
    if pl == 'python':
        #print(text)
        
        tests = text.split("def ")
        #print(tests)
        first_test = ''
        for i in range(len(tests)):
            
            if 'test' in tests[i] and "):" in tests[i]:
                first_test += "def " + tests[i].split('@')[0]
                break
            else:
                first_test += tests[i]
        #print('first test', first_test)
            
        # new file (start with imports), no tests generated
        if first_test.strip().startswith('import') or first_test.strip().startswith('from'):
            print('\t\t\t\t\t\tERROR: new file, no test generated')
            first_test = ''
        
        # new java file, no tests generated
        if 'java' in text or 'Copyright' in text or first_test.strip().startswith('package'):
            print('\t\t\t\t\t\tERROR: new JAVA file')
            first_test = ''
        
        # new class
        if first_test.strip().startswith('class'):
            print('\t\t\t\t\t\tERROR: new class, no test generated')
            first_test = ''
            
    
    elif pl == 'java':
        # find the index of the last occurrence of import, package, and public class
        stripped_text = text.replace("}", "").strip()

        if stripped_text.startswith('package') or stripped_text.startswith('import') or stripped_text.startswith('public class'):
            print('\t\t\t\t\t\tERROR: new file, no test generated')
            return ''
        
        comby = Comby()
        comby_template = 'void :[name](:[args]):[exceptions]:[a~[ \n\t]*]{...}'
        matches = comby.matches(text, comby_template, language=".java")

        matches_arr = [m for m in matches]
        
        if len(matches_arr) == 0:
            test_annotations = text.split("@Test")
            if len(test_annotations) <= 2:
                updated_text = text.split("}\n")[0]
                not_test = "Copyright" in updated_text or ("test" not in updated_text and "Test" not in updated_text)
                if not_test:
                    print('\t\t\t\t\t\tERROR: new file, no test generated')
                return '' if not_test else updated_text
            return test_annotations[0] + "@Test" + test_annotations[1].split("@")[0]
        else:
            matched_text = matches_arr[0].matched
            curr_text =matched_text.encode('utf-8').decode('unicode_escape')
            new_text = text.split(curr_text)[0] + curr_text
            if "Copyright" in new_text:
                print('\t\t\t\t\t\tERROR: new file, no test generated')
                return ''
            return new_text
    return first_test

def postprocess_outputs(code_filepath, test_filepath, generation_output_path, eof_sippet_filepath, pl, num_samples):
    if pl == 'python':
        code_filename = code_filepath.split('/')[-1][:-3]
        test_filename = test_filepath.split('/')[-1][:-3]
    elif pl == 'java':
        code_filename = code_filepath.split('/')[-1][:-5]
        test_filename = test_filepath.split('/')[-1][:-5]
    generations_file = f"{generation_output_path}/{code_filename}-{test_filename}_outputs.txt"
    
    file_content = load_data(generations_file)
    eof_snippet = load_data(eof_sippet_filepath)
    output_samples = file_content.split('\n')
    test_methods= []
    count = 0
    # get the generated tests
    test_mapping = {}
    test_set = set()
    for i, sample in enumerate(output_samples):
        print('for sample ',i)
        if i % num_samples == 0:
            test_set = set()

        if sample == '':
            continue
        output_dict = json.loads(sample)
        context = output_dict['context']        
        generated_text = output_dict['text'] 
        first_gen_method = get_first_method(generated_text, pl) 
        # if generated test is a duplicate

        if first_gen_method in test_set or len(first_gen_method) == 0:
            continue
        else:
            test_methods.append(first_gen_method)
            output = context + '\n' + first_gen_method  
            test_mapping[i] = first_gen_method
            test_set.add(first_gen_method)
            #print(output)
            test_file_content = output.split('<|codetestpair|>')[-1]
            test_file_content += '\n' + eof_snippet
            if pl == "java":
                # add closing brace in java
                test_file_content += '\n}\n'
            extension = "java" if pl == "java" else "py"
            with open(f"{generation_output_path}/{test_filename}__n{str(i)}.{extension}" , 'w') as f_out:
                f_out.write(test_file_content)
            count += 1
        
    print(f'\t\t\t\tSTATS:{generation_output_path} generated:{len(output_samples)} unique:{count}')    
    return test_mapping




def main(completions_path, pl, temp, num_samples, frameworks_path, output_path):
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
    fp_mapping = {}
    error_list = []
    setting = f"t{temp}_n{num_samples}"
    for org in filepairs:
        fp_mapping[org] = {}
        print(f'org {org}')
        for project in filepairs[org]:
            fp_mapping[org][project] = {}
            print(f'\tproject {project}')
            for fp_index, filepair in enumerate(filepairs[org][project]):
                print(f'\t\tfp_index {fp_index}')
                code_filepath = filepair[0]
                test_filepath = filepair[1]
                print(f'\t\tcode_filepath {code_filepath}')
                print(f'\t\ttest_filepath {test_filepath}')
                generation_output_path = f"{completions_path}/{pl}/{org}/{project}/filepair{fp_index}/{setting}"
                eof_sippet_filepath = f"{completions_path}/{pl}/{org}/{project}/filepair{fp_index}/eof_snippet.txt"
                
                if pl == 'python':
                    code_filename = code_filepath.split('/')[-1][:-3]
                    test_filename = test_filepath.split('/')[-1][:-3]
                elif pl == 'java':
                    code_filename = code_filepath.split('/')[-1][:-5]
                    test_filename = test_filepath.split('/')[-1][:-5]
                generations_file = f"{generation_output_path}/{code_filename}-{test_filename}_outputs.txt"


                print(f'\t\t\tcode_filepath: {code_filepath}')
                print(f'\t\t\ttest_filepath: {test_filepath}')
                print(f'\t\t\toutput_path: {generation_output_path}')
                print(f'\t\t\eof_sippet_filepath: {eof_sippet_filepath}')
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
                    fp_mapping[org][project][fp_index] = postprocess_outputs(code_filepath, test_filepath, generation_output_path, eof_sippet_filepath, pl, num_samples)                    
                except Exception as e:
                    error_list.append(f"{generations_file}\n")
                    print("Exception postprocessing outputs", generation_output_path, e)
                    traceback.print_exc()

    with open(f"/data/GitHubMining/Generated_TestOutputs/errors/{pl}_errors_{temp}.txt", 'w') as f_out:
        f_out.writelines(error_list)

    with open(f'{output_path}/{pl}_{setting}_filepairs_preds.json', 'w') as f_out:
        json.dump(fp_mapping, f_out)

if __name__ == '__main__':
    completions_path = sys.argv[1] if len(sys.argv) > 1 else "/data/GitHubMining/Generated_TestOutputs"
    pl = sys.argv[2] if len(sys.argv) > 2 else 'java'
    temp = sys.argv[3] if len(sys.argv) > 3 else 0.2
    num_samples = sys.argv[4] if len(sys.argv) > 4 else 10
    frameworks_path = sys.argv[5] if len(sys.argv) > 5 else "/data/GitHubMining/TestFramework"
    output_path = sys.argv[6] if len(sys.argv) > 6 else "/data/GitHubMining/TextMetrics/TestGeneration"

    num_samples = int(num_samples)
    main(completions_path, pl, temp, num_samples, frameworks_path, output_path)

#sudo python3 -u postprocess_generated_tests.py | sudo tee output_python_postprocess_test.txt
#sudo python3 -u postprocess_generated_tests.py | sudo tee output_python_postprocess_t0.2_n10.txt
#sudo python3 -u postprocess_generated_tests.py | sudo tee output_python_postprocess_t0.8_n10.txt
#sudo python3 -u postprocess_generated_tests.py | sudo tee output_java_postprocess_t0.2_n10.txt
#sudo python3 -u postprocess_generated_tests.py | sudo tee output_java_postprocess_t0.8_n10.txt

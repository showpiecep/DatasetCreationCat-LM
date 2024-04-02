import os
import sys
import time
import json
import traceback
import re
import pandas as pd
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
    generations_file = f"{generation_output_path}/no_code_context_output_n10_t0.2"
    
    generations_df = pd.read_json(generations_file)
    eof_snippet = load_data(eof_sippet_filepath)
    test_methods= []
    count = 0
    # get the generated tests
    test_mapping = {}
    test_set = set()
    for i in range(len(generations_df)):
        print('for sample ',i)
        if i % num_samples == 0:
            test_set = set()

        if generations_df.loc[i,'generation'] == '':
            continue
        context = generations_df.loc[i,'prompt']        
        generated_text = generations_df.loc[i,'generation'] 
        #print('context')
        #print(context)
        #print('generated_text')
        #print(generated_text)
        
        first_gen_method = get_first_method(generated_text, pl) 

        # if generated test is a duplicate
        if first_gen_method in test_set or len(first_gen_method) == 0:
            continue
        else:
            test_methods.append(first_gen_method)
            test_set.add(first_gen_method)
            test_mapping[i] = first_gen_method
            output = context + '\n' + first_gen_method       
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
        
    print(f'\t\t\t\tSTATS:{generation_output_path} generated:{len(generations_df)} unique:{count}')    

    return test_mapping



def main():
    temp = 0.2
    num_samples = 10
    pl = 'java'
    model_type = "multi"
    model_size = '16B'

    with open(f'/data/GitHubMining/TestFramework/{pl}_filepairs.json') as f_in:
        filepairs = json.load(f_in)
    
    setting = f"codegen-{model_size}-{model_type}_t{temp}_n{num_samples}"
    #print(filepairs)
    fp_mapping = {}
    error_list = []
    for org in filepairs:
        print(f'org {org}')
        fp_mapping[org] = {}
        for project in filepairs[org]:
            print(f'\tproject {project}')
            fp_mapping[org][project] = {}
            for fp_index, filepair in enumerate(filepairs[org][project]):
                print(f'\t\tfp_index {fp_index}')
                code_filepath = filepair[0]
                test_filepath = filepair[1]
                print(f'\t\tcode_filepath {code_filepath}')
                print(f'\t\ttest_filepath {test_filepath}')
                eof_sippet_filepath = f"/data/GitHubMining/Generated_TestOutputs/{pl}/{org}/{project}/filepair{fp_index}/eof_snippet.txt"
                generation_output_path = f"/data/GitHubMining/Generated_TestOutputs/{pl}/{org}/{project}/filepair{fp_index}/{setting}"
                
                print(f'\t\t\tcode_filepath: {code_filepath}')
                print(f'\t\t\ttest_filepath: {test_filepath}')
                print(f'\t\t\toutput_path: {generation_output_path}')
                print(f'\t\t\eof_sippet_filepath: {eof_sippet_filepath}')

                try:
                    fp_mapping[org][project][fp_index] = postprocess_outputs(code_filepath, test_filepath, generation_output_path, eof_sippet_filepath,  pl, num_samples)
                except Exception as e:
                    error_list.append(f"{generation_output_path}/no_code_context_output_n10_t0.2\n")
                    print("Exception postprocessing outputs", generation_output_path, e)
                    traceback.print_exc()

    with open(f"/data/GitHubMining/Generated_TestOutputs/errors/{pl}_codegen-{model_type}-{model_size}_errors_{temp}.txt", 'w') as f_out:
        f_out.writelines(error_list)


    with open(f'/data/GitHubMining/TextMetrics/TestGeneration/{pl}_{setting}_filepairs_preds.json', 'w') as f_out:
        json.dump(fp_mapping, f_out)

if __name__ == '__main__':
    main()

#sudo python3 -u postprocess.py | sudo tee output_python_postprocess_t0.8_n10.txt
# python3 -u postprocess.py | tee output_java_postprocess_t0.2_n10.txt

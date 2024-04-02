import os
import json 

def generate_config_files(code_filepath, test_filepath, output_path, temp, num_samples, pl):
    if pl == 'python':
        code_filename = code_filepath.split('/')[-1][:-3]
        test_filename = test_filepath.split('/')[-1][:-3]
    elif pl == 'java':
        code_filename = code_filepath.split('/')[-1][:-5]
        test_filename = test_filepath.split('/')[-1][:-5]
    generation_output = f"{output_path}/t{temp}_n{num_samples}"
    sample_input_file = f"{output_path}/{code_filename}-{test_filename}_contexts.txt"
    sample_output_file = f"{generation_output}/{code_filename}-{test_filename}_outputs.txt"
    configfile_output = f"{output_path}/text_generation_{pl}_t{temp}_n{num_samples}.yml"
    
    # create output path
    if not os.path.exists(generation_output):
        os.makedirs(generation_output)
    
    config = f"""{{
    "text-gen-type": "input-file",
    "maximum_tokens": 512,
    "temperature": {temp},
    "top_p": 0.0,
    "top_k": 0,
    "recompute": false,
    "num-samples": {num_samples},
    "sample-input-file": "{sample_input_file}",
    "sample-output-file": "{sample_output_file}"
}}"""
    print(config)
    with open(configfile_output,'w') as f_out: 
        f_out.write(str(config))

    return configfile_output

def main(pl, temp, num_samples):
    
    with open(f'/data/GitHubMining/TestFramework/{pl}_filepairs.json') as f_in:
        filepairs = json.load(f_in)
    
    print(filepairs)
    config_paths = []
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
                
                output_path = f"/data/GitHubMining/Generated_TestOutputs/{pl}/{org}/{project}/filepair{fp_index}"
                print(f'\t\t\tcode_filepath: {code_filepath}')
                print(f'\t\t\ttest_filepath: {test_filepath}')
                print(f'\t\t\toutput_path: {output_path}')
                config_paths.append(generate_config_files(code_filepath, test_filepath, output_path, temp, num_samples, pl))

    print(config_paths)
    with open(f"/code/Code/gpt-neox/data/{pl}_config_paths_t{temp}_n{num_samples}.txt" ,'w') as f_out: 
        f_out.write('\n'.join(config_paths))
           

if __name__ == '__main__':
    
    main(pl='python', temp=0.2, num_samples=10)    
    main(pl='java', temp=0.2, num_samples=10)    
    
# sudo python3 -u input_config_generation.py | sudo tee output_configs_n10_t0.2_java.txt
# sudo python3 -u input_config_generation.py | sudo tee output_configs_n10_t0.8_java.txt
# sudo python3 -u input_config_generation.py | sudo tee output_configs_n10_t0.2_python.txt
# sudo python3 -u input_config_generation.py | sudo tee output_configs_n10_t0.8_python.txt


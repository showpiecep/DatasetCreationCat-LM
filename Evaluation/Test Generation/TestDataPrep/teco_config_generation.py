import os
import json 
import glob

def generate_config_files(output_path, temp, num_samples):
    sample_input_file = glob.glob(output_path+"/*_contexts.txt")[0]
    generation_output = f"{output_path}/t{temp}_n{num_samples}"
    sample_output_file = f"{generation_output}/{sample_input_file.split('/')[-1].replace('contexts','outputs')}"
    configfile_output = f"{output_path}/text_generation_teco_t{temp}_n{num_samples}.yml"
    
    # create output path
    if not os.path.exists(generation_output):
        os.makedirs(generation_output)
    
    config = f"""{{
    "text-gen-type": "input-file",
    "maximum_tokens": 128,
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

def main(temp, num_samples):
    
    config_paths = []
    for i in range(1000):
        print(f'index {i}')
        
        output_path = f"/data/GitHubMining/Generated_TestOutputs/TecoContexts/{i}"
        config_paths.append(generate_config_files(output_path, temp, num_samples))

    print(config_paths)
    with open(f"/code/Code/gpt-neox/data/teco_config_paths_t{temp}_n{num_samples}.txt" ,'w') as f_out: 
        f_out.write('\n'.join(config_paths))
           

if __name__ == '__main__':
    num_samples = 10
   
    #main(temp=0.2, num_samples=10)    
    main(temp=0.8, num_samples=10)    
    
# sudo python3 -u teco_config_generation.py | sudo tee output_configs_n10_t0.2_teco.txt
# sudo python3 -u teco_config_generation.py | sudo tee output_configs_n10_t0.8_teco.txt


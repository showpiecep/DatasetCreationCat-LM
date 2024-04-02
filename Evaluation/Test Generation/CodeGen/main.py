from transformers import CodeGenForCausalLM, CodeGenTokenizerFast
import traceback
import os
import torch
import sys
import time
import json

class print_time:
    def __init__(self, desc):
        self.desc = desc

    def __enter__(self):
        print(self.desc)
        self.t = time.time()

    def __exit__(self, type, value, traceback):
        print(f'{self.desc} took {time.time()-self.t:.02f}s')
        
        
def prompt_codegen(tokenizer, model, input_ids, max_tokens, number_of_samples, temp):
    #print("Input:\n" + 100 * '-')
    #print(input_text)
    #input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to("cuda")
    len_input = input_ids.shape[1]
    input_ids = input_ids.to("cuda")
    
    print('input_ids.shape',input_ids.shape)
    sample_outputs = model.generate(
        input_ids,
        do_sample=True, 
        #max_length=seq_length, 
        max_new_tokens = max_tokens,
        top_k=50, 
        top_p=0.95,
        temperature=temp, 
        num_return_sequences=number_of_samples
    )

    print("Output:\n" + 100 * '-')
    outputs = []
    for i, sample_output in enumerate(sample_outputs):
        generated_output = sample_output[len_input:] #ignore input, only extract generated output
        print(f'sample_output.shape: {sample_output.shape}, len_input: {len_input}, generated_output.shape: {generated_output.shape}')
        #output = tokenizer.decode(sample_output, skip_special_tokens=True)
        generated_output = tokenizer.decode(generated_output, skip_special_tokens=True)
        #print(f"{i}: {output}")
        #print(f"generated_output {i}: {generated_output}")
        #output = output.split(input_text)[-1]      
        #print(f"{i}: {output.strip()}")
        outputs.append(generated_output)

    return outputs

DATA_COLUMNS = ('org', 'project', 'fp_index', 'prompt', 'num_sample', 'generation')

def generate_tests_codegen(org, project, fp_index, prompt_file, output_path, tokenizer, model):
    
    seq_length = 2048
    maximum_tokens = 512
    number_of_samples = 10
    temp = 0.2 

    with open(prompt_file, "r") as f:
        prompts = f.read()
        prompts = prompts.split('<|end_prompt|>')
    prompts = [p.strip() for p in prompts]
    prompts = [p for p in prompts if len(p) > 0]
    print('num unique prompts', len(prompts))
    print('num samples per prompt', number_of_samples)
    
    data = {key: [] for key in DATA_COLUMNS}

    for prompt in prompts:
        # no code context case
        if '<|codetestpair|>' not in prompt:
            
            with print_time(f'sanitize input if num tokens > 2048'):
                input_ids = tokenizer(prompt, return_tensors="pt").input_ids
                print(f'input_ids.shape {input_ids.shape}')
                if input_ids.shape[1] >= (seq_length - maximum_tokens):
                    print('Warning!!  >= (seq_length - maximum_tokens)')
                    num_excess_tokens = input_ids.shape[1] - (seq_length - maximum_tokens) + 2 
                    print(f'BEFORE: input_ids.shape {input_ids.shape}')
                    input_ids = input_ids[:, num_excess_tokens:]
                    print(f'AFTER: input_ids.shape {input_ids.shape}')
                #input_text = tokenizer.decode(input_ids[0], skip_special_tokens=True)
                
               
            # for 16B: prompt 1 at a time
            for i in range(number_of_samples):
                with print_time(f'prompt codegen using {prompt_file}'):
                    output = prompt_codegen(tokenizer, model, input_ids, maximum_tokens, 1, temp)[0]
                data['org'].append(org)
                data['project'].append(project)
                data['fp_index'].append(fp_index)
                data['prompt'].append(prompt)
                data['num_sample'].append(i)
                data['generation'].append(output)
            
            '''
            with print_time(f'prompt codegen using {prompt_file}'):
                outputs = prompt_codegen(tokenizer, model, input_text, seq_length, number_of_samples, temp)
               
            for i, output in enumerate(outputs):
                data['org'].append(org)
                data['project'].append(project)
                data['fp_index'].append(fp_index)
                data['prompt'].append(input_text)
                data['num_sample'].append(i)
                data['generation'].append(output)
            '''
        # store metadata 
    print(f'saving to {output_path}/no_code_context_output_n{number_of_samples}_t{temp}')
    with open(f'{output_path}/no_code_context_output_n{number_of_samples}_t{temp}', 'w') as f:
        json.dump(data, f)    


def main(model_name):
    
    temp = 0.2
    num_samples = 10
    pl = 'python'
    print('model_name', model_name)
    with open(f'/data/GitHubMining/TestFramework/{pl}_filepairs.json') as f_in:
    #with open(f'./{pl}_filepairs.json') as f_in:
        filepairs = json.load(f_in)
    
    with print_time('Load tokenizer and pretrained model'):
        checkpoint = f"Salesforce/{model_name}"
        tokenizer = CodeGenTokenizerFast.from_pretrained(checkpoint, cache_dir="/huggingfacedata/codegen/")
        model = CodeGenForCausalLM.from_pretrained(checkpoint, cache_dir="/huggingfacedata/codegen/", device_map="auto", torch_dtype=torch.float16)
    
   
    #print(filepairs)
    for org in filepairs:
        print(f'org {org}')
        for project in filepairs[org]:
            print(f'\tproject {project}')
            for fp_index, filepair in enumerate(filepairs[org][project]):
                if org == 'dagster-io':
                    fp_index = 7
                elif org == 'upb-lea':
                    fp_index = 2
                elif org == 'simaki':
                    fp_index = 1
                print(f'\t\tfp_index {fp_index}')
                code_filepath = filepair[0]
                test_filepath = filepair[1]
                print(f'\t\tcode_filepath {code_filepath}')
                print(f'\t\ttest_filepath {test_filepath}')
                generation_output_path = f"/data/GitHubMining/Generated_TestOutputs/{pl}/{org}/{project}/filepair{fp_index}/{model_name}_t{temp}_n{num_samples}_v3"
                # create output path
                if not os.path.exists(generation_output_path):
                    os.makedirs(generation_output_path)
                if pl == 'python':
                    code_filename = code_filepath.split('/')[-1][:-3]
                    test_filename = test_filepath.split('/')[-1][:-3]
                elif pl == 'java':
                    code_filename = code_filepath.split('/')[-1][:-5]
                    test_filename = test_filepath.split('/')[-1][:-5]
                prompt_file = f"/data/GitHubMining/Generated_TestOutputs/{pl}/{org}/{project}/filepair{fp_index}/{code_filename}-{test_filename}_contexts.txt"
                print(f'\t\t\tprompt_file: {test_filepath}')                
                print(f'\t\t\toutput_path: {generation_output_path}')

                try:
                    generate_tests_codegen(org, project, fp_index, prompt_file, generation_output_path, tokenizer, model)
                except Exception as e:
                    print("Exception postprocessing outputs", generation_output_path, e)
                    traceback.print_exc()
                

if __name__ == '__main__':
    for model_name in ['codegen-16B-multi']:
        main(model_name)

# python3 -u main.py 2>&1 | tee output_prompt_codegen2B_python_t0.2_n10.txt
# python3 -u main.py 2>&1 | tee output_prompt_codegen2B_java_t0.2_n10.txt
# python3 -u main.py 2>&1 | tee output_prompt_codegen2B_java_t0.2_n10_v2.txt
# python3 -u main.py 2>&1 | tee output_prompt_codegen16B_python_t0.2_n10.txt
# python3 -u main.py 2>&1 | tee output_prompt_codegen16B_java_t0.2_n10.txt

# python3 -u main.py 2>&1 | tee output_prompt_codegen2B-mono_python_t0.2_n10.txt
# python3 -u main.py 2>&1 | tee output_prompt_codegen16B-mono_python_t0.2_n10.txt

# python3 -u main.py 2>&1 | tee output_prompt_codegen_python_errors_v3.txt

# python3 -u main.py 2>&1 | tee output_prompt_codegen_java_t0.2_n10_v3.txt
# python3 -u main.py 2>&1 | tee output_prompt_codegen-16B-multi_python_t0.2_n10_v3.txt
# python3 -u main.py 2>&1 | tee output_prompt_codegen-16B-mono_python_t0.2_n10_v3.txt
import os
import pandas as pd
#from github import Github
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import seaborn as sns

from matplotlib_venn import venn2


plt.rc('font', size=16)          # controls default text sizes
plt.rc('axes', titlesize=16)     # fontsize of the axes title
plt.rc('axes', labelsize=16)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=16)    # fontsize of the tick labels
plt.rc('ytick', labelsize=16)    # fontsize of the tick labels
plt.rc('legend', fontsize=16)    # legend fontsize
plt.rc('figure', titlesize=16)  # fontsize of the figure title
plt.rcParams["figure.figsize"] = (8,4)

def plot_sum_tokens_histogram(python_tokens, java_tokens, title):

    bins=[0, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, max(max(python_tokens), max(java_tokens))]
    
    python_hist_data, bin_edges = np.histogram(python_tokens, bins) 
    java_hist_data, bin_edges = np.histogram(java_tokens, bins)
    
    print(f'histogram distribution for {title}:', ['{}-{}: {}'.format(bins[i], bins[i+1], j) for i,j in enumerate(python_hist_data)])
    print(f'<1024: {sum(python_hist_data[:4])/sum(python_hist_data)}, 1024-2048: {python_hist_data[4]/sum(python_hist_data)}, 2048-4096: {python_hist_data[5]/sum(python_hist_data)}, 4096-8192: {python_hist_data[6]/sum(python_hist_data)}, 8192-16384: {python_hist_data[7]/sum(python_hist_data)}, 8192-16384: {sum(python_hist_data[8:])/sum(python_hist_data)}' )
    
    print(f'histogram distribution for {title}:', ['{}-{}: {}'.format(bins[i], bins[i+1], j) for i,j in enumerate(java_hist_data)])
    print(f'<1024: {sum(java_hist_data[:4])/sum(java_hist_data)}, 1024-2048: {java_hist_data[4]/sum(java_hist_data)}, 2048-4096: {java_hist_data[5]/sum(java_hist_data)}, 4096-8192: {java_hist_data[6]/sum(java_hist_data)}, 8192-16384: {java_hist_data[7]/sum(java_hist_data)}, 8192-16384: {sum(java_hist_data[8:])/sum(java_hist_data)}' )
    fig, ax = plt.subplots()
    x_axis = np.arange(len(python_hist_data))

    
    # Plot the histogram heights against integers on the x axis
    plt.bar(x_axis+0.25, python_hist_data, width=0.5,label='Python', color='skyblue', hatch='\\', edgecolor='white') 
    plt.bar(x_axis-0.25,java_hist_data, width=0.5, label='Java', color='pink', hatch='/', edgecolor='white') 
    #plt.bar(x_axis, python_hist_data,label='python', color='blue', alpha=0.5) 
    #plt.bar(x_axis,java_hist_data, label='java', color='pink', alpha=0.5) 
    
    # Set the ticks to the middle of the bars
    ax.set_xticks([0.5+i for i,j in enumerate(python_hist_data)])
    #ax.set_xticks([i for i,j in enumerate(python_hist_data)])
    # Set the xticklabels to a string that tells us what the bin edges were
    ax.set_xticklabels(['{}'.format(bins[i+1]) for i,j in enumerate(python_hist_data)], rotation = 30)
    #ax.set_title('Distribution of projects based on tokens')
    plt.xlabel('Number of Tokens')
    plt.ylabel('Number of File Pairs')
    plt.legend()
    plt.tight_layout()
    plt.savefig(title + '.png',bbox_inches='tight')
    plt.clf()
'''
root@eb4b4ff0ba22:/code/Code/SoftwareTesting/FileLevel/DataAnalysis# python3 data_analysis.py 
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 147970/147970 [02:23<00:00, 1029.90it/s]
412880
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 48882/48882 [01:13<00:00, 662.78it/s]
743882
histogram distribution for sum_tokens: ['0-128: 440', '128-256: 3285', '256-512: 10927', '512-1024: 34428', '1024-2048: 75699', '2048-4096: 105286', '4096-8192: 90929', '8192-16384: 55888', '16384-689052: 35998']
<1024: 0.11887231156752567, 1024-2048: 0.18334382871536523, 2048-4096: 0.255003875217981, 4096-8192: 0.2202310598721178, 8192-16384: 0.13536136407672933, 8192-16384: 0.08718756055028096
histogram distribution for sum_tokens: ['0-128: 240', '128-256: 7791', '256-512: 19730', '512-1024: 72643', '1024-2048: 195690', '2048-4096: 218764', '4096-8192: 138964', '8192-16384: 62021', '16384-689052: 28039']
<1024: 0.1349730199144488, 1024-2048: 0.2630659163684563, 2048-4096: 0.2940842768073431, 4096-8192: 0.1868091982330531, 8192-16384: 0.0833747825595995, 8192-16384: 0.037692806117099215

< 2048: 30.21+ 39.79

'''

def plot_sum_tokens_distribution(python_tokens, java_tokens, title):
    '''
    # Create two data sets
    x = np.random.randn(1000)
    y = np.random.randn(1000)

    # Define the custom bins
    bins = np.linspace(-3, 3, 10)

    # Plot the histograms
    sns.histplot(x, bins=bins, alpha=0.5, label='x')
    sns.histplot(y, bins=bins, alpha=0.5, label='y')

    # Plot the density functions
    sns.kdeplot(x, label='x density')
    sns.kdeplot(y, label='y density')

    # Add a legend
    plt.legend()

    plt.savefig(title + '.png')
    plt.clf()
    '''
    bins=[0, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, max(max(python_tokens), max(java_tokens))]
    
    # Plot the histograms
    sns.histplot(python_tokens, bins=bins, alpha=0.5, label='Python')
    sns.histplot(java_tokens, bins=bins, alpha=0.5, label='Java')

    # Add a legend
    plt.legend()

    plt.savefig(title + '.png')
    plt.clf()


def get_token_counts(filepairs_dir, repos_file):
    with open(repos_file) as f:
        repo_links_list = f.read().split('\n')
    sum_tokens_lst = []

    for i, repo_link_line in enumerate(tqdm(repo_links_list)):
        repo_link = repo_link_line.split('\t')[0]
        org = repo_link.split('/')[-2] 
        project = repo_link.split('/')[-1] 

        filepair_filepath = os.path.join(filepairs_dir, 'filepairs_' + org + '__' + project + '.json')
        if org == '361way':
            continue
        
        try:
            filepairs_df = pd.read_json(filepair_filepath)   
            if len(filepairs_df) > 0:
                sum_tokens_lst.extend(filepairs_df['sum_tokens'])
                
        except Exception as e:
            print("Exception loading df", org, project, e)
            #traceback.print_exc() 
    
    return sum_tokens_lst

#plt.rcParams["figure.figsize"] = (12,12)
def plot_venn_diagram():
    #venn2(subsets = (11352546, 1853994, 1156763), set_labels = ('Group A', 'Group B'), set_colors=('purple', 'skyblue'), alpha = 0.7)
    v = venn2(subsets = (11352546, 1853994, 1156763), set_labels = ('Code files', 'Test files'), set_colors=('lightcoral', 'skyblue'), alpha = 0.7)
    v.get_patch_by_id('11').set_color('palegreen')
    p1 = v.get_patch_by_id('11')
    p1.set_hatch('x')
    p1.set_edgecolor('white')
    p1.set_alpha(1.0)
    p2 = v.get_patch_by_id('10')
    p2.set_hatch('\\')
    p2.set_edgecolor('white')
    p2.set_alpha(1.0)
    
    p3 = v.get_patch_by_id('01')
    p3.set_hatch('/')
    p3.set_edgecolor('white')
    p3.set_alpha(1.0)
    plt.rcParams["figure.figsize"] = (12,12)
    plt.rcParams.update({'font.size': 22})
    plt.savefig('files_venn.png')
    plt.clf()


#plt.rcParams.update({'font.size': 16})
#plt.rcParams["figure.figsize"] = (8,4)
def plot_star_file_distribution(python_df, java_df, output_file):
    
    k = 1000
    total_code_files_py = []
    total_test_files_py = []
    total_file_pairs_py = []
    total_code_files_java = []
    total_test_files_java = []
    total_file_pairs_java = []
    x = list(range(100))
    python_df = python_df.sort_values(by=['num_stars'],ascending=False)
    java_df = java_df.sort_values(by=['num_stars'],ascending=False)
    
    python_df_split = np.array_split(python_df, 100)
    java_df_split = np.array_split(java_df, 100)
    
    for i in range(len(python_df_split)):
        df = python_df_split[i]
        #print('python', i, len(df), len(python_df)/100)
        total_code_files_py.append(df['num_code_files'].sum())
        total_test_files_py.append(df['num_test_files'].sum())
        total_file_pairs_py.append(df['num_file_pairs'].sum())
        
    for i in range(len(java_df_split)):
        df = java_df_split[i]
        #print('java', i, len(df), len(java_df)/100)
        total_code_files_java.append(df['num_code_files'].sum())
        total_test_files_java.append(df['num_test_files'].sum())
        total_file_pairs_java.append(df['num_file_pairs'].sum())
        

    print('total_code_files_py',total_code_files_py[-10:])
    print('total_test_files_py',total_test_files_py[-10:])
    print('total_file_pairs_py',total_file_pairs_py[-10:])
    print('total_code_files_java',total_code_files_java[-10:])
    print('total_test_files_java',total_test_files_java[-10:])
    print('total_file_pairs_java',total_file_pairs_java[-10:])
    plt.plot(x[:-1], total_code_files_py[:-1], label = "Python code files", color='mediumblue')
    plt.plot(x[:-1], total_test_files_py[:-1], label = "Python test files", color='royalblue')
    plt.plot(x[:-1], total_file_pairs_py[:-1], label = "Python file pairs", color='lightsteelblue')
    plt.plot(x[:-1], total_code_files_java[:-1], label = "Java code files", color='teal')
    plt.plot(x[:-1], total_test_files_java[:-1], label = "Java test files", color='darkturquoise')
    plt.plot(x[:-1], total_file_pairs_java[:-1], label = "Java File pairs", color='paleturquoise')

    plt.xlabel("Project Percentiles")
    plt.ylabel("Total File Counts")
    plt.legend()
    plt.xticks(list(range(0,101,10)), list(range(0,101,10)), rotation=30)
    plt.savefig(output_file, bbox_inches='tight')
    plt.clf()


    
if __name__ == '__main__':
    input_dir = '/data/GitHubMining/Output/'
        
    python_filepairs_dir = os.path.join(input_dir, 'python', 'DeduplicatedFilePairs/')
    python_metadata_dir = os.path.join(input_dir, 'python', 'DeduplicatedMetaData/')
    python_repos_file = '../GitHubMining/python-top-repos.txt'

    java_filepairs_dir = os.path.join(input_dir, 'java', 'DeduplicatedFilePairs/')
    java_metadata_dir = os.path.join(input_dir, 'java', 'DeduplicatedMetaData/')
    java_repos_file = '../GitHubMining/java-top-repos.txt'

    plot_venn_diagram()
    
    python_tokens = get_token_counts(python_filepairs_dir, python_repos_file)
    print(len(python_tokens))
    java_tokens = get_token_counts(java_filepairs_dir, java_repos_file)
    print(len(java_tokens))
    
    #plot_sum_tokens_distribution(python_tokens, java_tokens, 'sum_tokens_dist')
    plot_sum_tokens_histogram(python_tokens, java_tokens, 'sum_tokens')
    
    java_df = pd.read_csv('Output/java_data_distribution_after_dedup.csv')
    python_df = pd.read_csv('Output/python_data_distribution_after_dedup.csv')
    
    plot_star_file_distribution(python_df,java_df, 'star_file_distribution.png')
    
    
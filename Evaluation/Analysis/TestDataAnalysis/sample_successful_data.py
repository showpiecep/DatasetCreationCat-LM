import sys
import os
import pandas as pd


def sample_df(df, generation_root, N=10):
    samples = df.sample(n=N)
    for i, row in samples.iterrows():
        print(f'org {row["Organization"]}')
        print(f'\tproject {row["Project"]}')
        print(f'\t\tcode_filepath {row["Source Filename"]}')
        print(f'\t\ttest_filepath {row["Test Filename"]}')
        label_prefix, label_suffix = row["Label"].rsplit("_", 1)
        test_prefix, ending = row["Test Filename"].rsplit("/", 1)[1].split(".")
        generation_path = os.path.join(generation_root, row["Organization"], row["Project"], f"filepair{row['Filepair Index']}", label_prefix, f"{test_prefix}__n{label_suffix}.{ending}")
        print(f'\t\t\tgeneration_path {generation_path}')
        print(f'\t\tcoverage {row["Coverage"]}')
        with open(generation_path, "r") as f:
            last_mtd = f.read().rsplit("def ", 1)[1]
            print(f'\t\tlast_mtd len {len("def "+last_mtd)}')

if __name__ == '__main__':
    framework_dir = sys.argv[1] if len(sys.argv) > 1 else '/data/GitHubMining/TestFramework'
    root_dir = sys.argv[1] if len(sys.argv) > 1 else '/data/GitHubMining'

    python_csv_path = os.path.join(framework_dir, "python_coverage_results.csv")

    df = pd.read_csv(python_csv_path)
    df_filtered = df[df['Status'] == 'SUCCESS']
    df_filtered = df_filtered[df['Coverage'] != "NOT FOUND"][df["Coverage"] != "0.0"]

    preamble_labels = [f"t0.2_n10_{i}" for i in range(10)]
    all_but_one_labels = [f"t0.2_n10_{i}" for i in range(10, 20)]
    extra_test_labels = [f"t0.2_n10_{i}" for i in range(20, 30)]

    df_preamble = df_filtered.loc[df["Label"].isin(preamble_labels)]
    df_all_but_one = df_filtered.loc[df["Label"].isin(all_but_one_labels)]
    df_extra_test = df_filtered.loc[df["Label"].isin(extra_test_labels)]

    generation_root = os.path.join(root_dir, "Generated_TestOutputs", "python_old")

    print("PREAMBLE -------------------------------")
    sample_df(df_preamble, generation_root)

    print("ALL BUT ONE -------------------------------")
    sample_df(df_all_but_one, generation_root)

    print("EXTRA TEST -------------------------------")
    sample_df(df_extra_test, generation_root)

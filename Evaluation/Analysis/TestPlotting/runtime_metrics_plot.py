import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the JSON data
MODES = {"java" : {
            "first_test": [
            ("codegen-2B-multi_t0.2_n10_v2,first_test,False","CodeGen-multi-2B"), 
            ("codegen-16B-multi_t0.2_n10,first_test,False","CodeGen-multi-16B"), 
            ("t0.2_n10,first_test,True", "CAT-LM")
            ],
            "last_test": [
            ("codegen-2B-multi_t0.2_n10_v2,last_test,False","CodeGen-multi-2B"), 
            ("codegen-16B-multi_t0.2_n10,last_test,False","CodeGen-multi-16B"), 
            ("t0.2_n10,last_test,True", "CAT-LM")
            ],
            "extra_test": [
            ("codegen-2B-multi_t0.2_n10_v2,extra_test,False","CodeGen-multi-2B"), 
            ("codegen-16B-multi_t0.2_n10,extra_test,False","CodeGen-multi-16B"), 
            ("t0.2_n10,extra_test,True", "CAT-LM")
            ]
        },
        "python" : {
            "first_test": [
            ("codegen-2B-multi_t0.2_n10,first_test,False","CodeGen-multi-2B"), 
            ("codegen-16B-multi_t0.2_n10,first_test,False","CodeGen-multi-16B"), 
            ("codegen-2B-mono_t0.2_n10,first_test,False","CodeGen-mono-2B"), 
            ("codegen-16B-mono_t0.2_n10,first_test,False","CodeGen-mono-16B"), 
            ("t0.2_n10,first_test,True", "CAT-LM"),
            ],
            "last_test": [
            ("codegen-2B-multi_t0.2_n10,last_test,False","CodeGen-multi-2B"), 
            ("codegen-16B-multi_t0.2_n10,last_test,False","CodeGen-multi-16B"), 
            ("codegen-2B-mono_t0.2_n10,last_test,False","CodeGen-mono-2B"), 
            ("codegen-16B-mono_t0.2_n10,last_test,False","CodeGen-mono-16B"), 
            ("t0.2_n10,last_test,True", "CAT-LM"),
            ],
            "extra_test": [
            ("codegen-2B-multi_t0.2_n10,extra_test,False","CodeGen-multi-2B"), 
            ("codegen-16B-multi_t0.2_n10,extra_test,False","CodeGen-multi-16B"),
            ("codegen-2B-mono_t0.2_n10,extra_test,False","CodeGen-mono-2B"),  
            ("codegen-16B-mono_t0.2_n10,extra_test,False","CodeGen-mono-16B"), 
            ("t0.2_n10,extra_test,True", "CAT-LM"),
            ]
        }
}

MODE_MAPPING = {"first_test": "First test", "last_test": "Last test", "extra_test": "Extra test"}

TOTALS = {
    "python": {"first_test": 1120, "last_test": 930, "extra_test": 1230},
    "java": {"first_test": 270, "last_test": 180, "extra_test": 270}
}

PLS = ["java", "python"]


for pl in PLS:
    data = json.load(open(f"/data/GitHubMining/TestFramework/TestingLLM/{pl}/asserts_completion_metrics_ds.json", "r"))

    filtered_data = []
    pl_modes = MODES[pl]
    print(pl_modes)
    for mode in pl_modes:
        mode_list = pl_modes[mode]
        for key, val in mode_list:
            if key in data:
                percentage = round(data[key]["passing"] / TOTALS[pl][mode] * 100, 2)
                filtered_data.append({"mode": MODE_MAPPING[mode], "tool": val, "passing": data[key]["passing"], "percentage_passing": percentage})

    # Convert the JSON data to a Pandas DataFrame
    df = pd.DataFrame(filtered_data)
    # Create a seaborn bar plot
    plt.figure(figsize=(6, 6))
    sns.set(style="white",font_scale=1.3)
    cp = sns.color_palette("pastel")
    colors = [cp[1], cp[2], cp[0], cp[3], cp[4]] if pl == "java" else [cp[1], cp[2], cp[3], cp[4], cp[0]]
    print(colors)

    ax = sns.barplot(x='mode', y='passing', hue='tool', data=df, palette=colors)
    patterns = ['/', '\\', 'x', '.', ''] if pl == "python" else ['/', '\\', '']

    # Apply patterns to the bars
    for bar, pattern in zip(ax.containers, patterns):
        for patch in bar.patches:
            patch.set_hatch(pattern)

    # # Add a legend and labels
    ax.legend(loc='upper left')
    if pl == "python":
        ax.set_ylim([0, 120])
    elif pl=="java":
        ax.set_ylim([0, 35])

    plt.xlabel("")
    plt.ylabel("# of passing generations")
    # plt.title(f"Passing completions for all modes in {pl.title()}")
    plt.tight_layout()
    # # Show the plot
    plt.savefig(f"passing_{pl}.pdf")
    plt.savefig(f"passing_{pl}.png")

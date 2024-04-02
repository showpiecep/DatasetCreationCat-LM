import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.patheffects as path_effects

pl = "python"
data = json.load(open(f"/data/GitHubMining/TestFramework/TestingLLM/{pl}/asserts_completion_metrics_fp.json", "r"))

MODE_MAPPING = {"first_test": "First test", "last_test": "Last test", "extra_test": "Extra test"}

df_arr = []
colors = sns.color_palette("pastel")


for fp in data:
    if "t0.2_n10" in fp and "True" in fp:
        mode = fp.split(",")[1]
        fp_data = data[fp]
        if not np.isnan(fp_data["all_cov_improvement"]) and not np.isnan(fp_data["all_human_cov_improvement"]):
            df_arr.append({"mode": MODE_MAPPING[mode], "CAT-LM cov impr.": fp_data["all_cov_improvement"], "Human cov impr.": fp_data["all_human_cov_improvement"]})

df = pd.DataFrame(df_arr)
df_melted = pd.melt(df, id_vars=['mode'], value_vars=['CAT-LM cov impr.', 'Human cov impr.'], var_name='metric', value_name='value')
print(df_melted)

sns.set(style="whitegrid",font_scale=1.3)
sns.set_palette([colors[0], colors[1]])
plt.figure(figsize=(6, 4))
# Creating the violin plots
ax = sns.violinplot(x='mode', y='value', hue='metric', data=df_melted, split=True, scale='count', inner="quartile", cut=0, order=["First test", "Last test", "Extra test"])

patterns = ['', 'x']

# Apply patterns to violin plot with hue
n_categories = len(df_melted['mode'].unique())
n_hues = len(df_melted['value'].unique())
for i, collection in enumerate(ax.collections[:n_categories * n_hues]):
    path_data = collection.get_paths()[0]

    # Create a new patch with the same path data, hatch pattern, and hatch color
    hatch_patch = plt.matplotlib.patches.PathPatch(
        path_data, hatch=patterns[i % len(patterns)], fill=False, linewidth=0, edgecolor='white'
    )

    # Add the new patch to the plot
    ax.add_artist(hatch_patch)

for i, collection in enumerate(ax.collections[:n_categories * n_hues]):
    collection.set_edgecolor("#737373")

legend_handles = []
for i, (pattern, hue) in enumerate(zip(patterns, df_melted['metric'].unique())):
    legend_handles.append(mpatches.Patch(facecolor=colors[i], edgecolor='white', hatch=pattern, label=hue))

# Customizing the plot
# plt.title(f'CAT-LM vs Human Coverage Improvement ({pl.title()})')
plt.ylabel('Coverage Improvement')
plt.xlabel('')
plt.legend(title='', handles=legend_handles)

# Show the plot
plt.savefig(f"stacked_{pl}.pdf")
plt.savefig(f"stacked_{pl}.png")

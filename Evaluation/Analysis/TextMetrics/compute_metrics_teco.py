import sys
import json
from metrics import *
from tqdm import tqdm
import os
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'TestFramework'))
from pygments_utils import tokenize_code

def compute_metrics(preds, golds, eval_lang, pl):
    code_bleu_met = code_bleu(preds, golds, eval_lang)
    bleu_met = bleu(preds, golds)
    xmatch_met = exact_match(preds, golds)
    edit_sim_met = edit_sim(preds, golds)
    # cb_score = codebert_score(["".join(golds)], ["".join(preds)], pl)
    rouge_f = rouge_l(golds, preds)["f"]
    rouge_p = rouge_l(golds, preds)["p"]
    rouge_r = rouge_l(golds, preds)["r"]
    return {"code_bleu": code_bleu_met, "bleu": bleu_met, "xmatch": xmatch_met, "edit_sim": edit_sim_met, "rouge_f": rouge_f, "rouge_p": rouge_p, "rouge_r": rouge_r}


if __name__ == "__main__":
    preds_path = sys.argv[1] if len(sys.argv) > 1 else "/data/GitHubMining/TextMetrics/Teco/teco_preds_0.8.json"
    golds_path = sys.argv[2] if len(sys.argv) > 2 else "/data/GitHubMining/TextMetrics/Teco/teco_gold.json"
    output_path = sys.argv[3] if len(sys.argv) > 3 else "/data/GitHubMining/TextMetrics/Teco/teco_metrics_0.8.json"
    pl = sys.argv[4] if len(sys.argv) > 4 else "java"

    with open(preds_path, 'r') as json_file:
        preds = json.load(json_file)
    
    with open(golds_path, 'r') as json_file:
        golds = json.load(json_file)

    eval_lang = "Java8" if pl == "java" else "Python3"
    
    metrics_map = {}

    for ind in tqdm(golds):
        if ind in preds:
            gold_toks = golds[ind]
            example_preds = preds[ind]
            metrics_map[ind] = {}
            for example_ind in example_preds:
                pred_toks = tokenize_code(example_preds[example_ind])
                metrics_map[ind][example_ind] = compute_metrics(pred_toks, gold_toks, eval_lang, pl)                    
    
    with open(output_path, 'w') as json_file:
        json.dump(metrics_map, json_file)
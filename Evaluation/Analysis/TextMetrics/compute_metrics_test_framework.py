import sys
import json
from metrics import *
from tqdm import tqdm
import os
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'TestFramework'))
from pygments_utils import tokenize_code

def compute_metrics(preds, golds, lang, pl):
    code_bleu_met = code_bleu(preds, golds, lang)
    bleu_met = bleu(preds, golds)
    xmatch_met = exact_match(preds, golds)
    edit_sim_met = edit_sim(preds, golds)
    # cb_score = codebert_score(["".join(golds)], ["".join(preds)], pl)
    rouge_f = rouge_l(golds, preds)["f"]
    rouge_p = rouge_l(golds, preds)["p"]
    rouge_r = rouge_l(golds, preds)["r"]
    return {"code_bleu": code_bleu_met, "bleu": bleu_met, "xmatch": xmatch_met, "edit_sim": edit_sim_met, "rouge_f": rouge_f, "rouge_p": rouge_p, "rouge_r": rouge_r}


if __name__ == "__main__":
    preds_path = sys.argv[1] if len(sys.argv) > 1 else "/data/GitHubMining/TextMetrics/TestGeneration/java_0.2_10_filepairs_preds.json"
    golds_path = sys.argv[2] if len(sys.argv) > 2 else "/data/GitHubMining/TextMetrics/TestGeneration/java_filepairs_golds.json"
    output_path = sys.argv[3] if len(sys.argv) > 3 else "/data/GitHubMining/TextMetrics/TestGeneration/java_0.2_10_metrics.json"
    pl = sys.argv[4] if len(sys.argv) > 4 else "java"

    with open(preds_path, 'r') as json_file:
        preds = json.load(json_file)
    
    with open(golds_path, 'r') as json_file:
        golds = json.load(json_file)

    eval_lang = "Java8" if pl == "java" else "Python3"
    
    metrics_map = {}

    for org in tqdm(golds):
        orgs_golds = golds[org]
        metrics_map[org] = {}
        for proj in orgs_golds:
            proj_golds = orgs_golds[proj]
            metrics_map[org][proj] = {}
            for ind in proj_golds:
                if ind in preds[org][proj]:
                    gold_toks_dir = proj_golds[ind]
                    example_preds = preds[org][proj][ind]
                    metrics_map[org][proj][ind] = {}
                    for example_ind in example_preds:
                        pred_toks = tokenize_code(example_preds[example_ind])
                        int_example_ind = int(example_ind)
                        is_first_test = int_example_ind < 10 or int_example_ind >= 30 and int_example_ind < 40
                        is_last_test = int_example_ind >= 10 and int_example_ind < 20 or int_example_ind >= 40 and int_example_ind < 50
                        if is_first_test:
                            gold_toks = gold_toks_dir["first_test_tokens"]
                            metrics_map[org][proj][ind][int_example_ind] = compute_metrics(pred_toks, gold_toks, eval_lang, pl)
                        elif is_last_test:
                            gold_toks = gold_toks_dir["last_test_tokens"]
                            metrics_map[org][proj][ind][int_example_ind] = compute_metrics(pred_toks, gold_toks, eval_lang, pl)
    
    with open(output_path, 'w') as json_file:
        json.dump(metrics_map, json_file)
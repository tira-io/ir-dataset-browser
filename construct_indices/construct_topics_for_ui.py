from tira.rest_api_client import Client
from tira.tirex import IRDS_TO_TIREX_DATASET
from tqdm import tqdm
import ir_measures
import ir_datasets
from statistics import median
import json
import numpy as np

tira = Client()
datasets = {i: ir_datasets.load(i) for i in ['antique/test', 'argsme/2020-04-01/touche-2020-task-1', 'argsme/2020-04-01/touche-2021-task-1', 'cord19/fulltext/trec-covid', 'cranfield', 'msmarco-passage/trec-dl-2019/judged', 'msmarco-passage/trec-dl-2020/judged', 'vaswani', ]}
tira_runs = [
    "ir-benchmarks/tira-ir-starter/BM25 Re-Rank (tira-ir-starter-pyterrier)",
    "ir-benchmarks/tira-ir-starter/MonoT5 Base (tira-ir-starter-gygaggle)",
    "ir-benchmarks/tira-ir-starter/MonoT5 Large (tira-ir-starter-gygaggle)",
    "ir-benchmarks/tira-ir-starter/DirichletLM Re-Rank (tira-ir-starter-pyterrier)",
    "ir-benchmarks/tira-ir-starter/TASB msmarco-distilbert-base-dot (tira-ir-starter-beir)"
]

def process_dataset(dataset_name, qrels):
    dataset = datasets[dataset_name]
    ret = {}

    for i in dataset.queries_iter():
        ret[str(i.query_id)] = {"dataset": dataset_name, "query_id": str(i.query_id), "default_text": i.default_text()}

    measures = [ir_measures.nDCG@10, ir_measures.P@10, ir_measures.Judged@10]
    for tira_run in tqdm(tira_runs, desc=f"Processing {dataset_name}"):
        run = ir_measures.read_trec_run(tira.get_run_output(tira_run, IRDS_TO_TIREX_DATASET[dataset_name]) + '/run.txt')

        for i in ir_measures.iter_calc(measures, qrels, run):
            measure = str(i.measure)
            qid = str(i.query_id)
            if qid not in ret:
                continue

            if 'min_' + measure not in ret[qid] or ret[qid]['min_' + measure] > i.value:
                ret[qid]['min_' + measure] = i.value

            if 'max_' +measure not in ret[qid] or ret[qid]['max_' + measure] < i.value:
                ret[qid]['max_' + measure] = i.value
            
            if 'median_' + measure not in ret[qid]:
                ret[qid]['median_' + measure] = []

            ret[qid]['median_' + measure] += [i.value]

    for i in ret:
        for j in measures:
            if 'median_' + str(j) in ret[i]:
                ret[i]['var_' + str(j)] = np.var(ret[i]['median_' + str(j)])
                ret[i]['median_' + str(j)] = median(ret[i]['median_' + str(j)])


    for i in ret:
        for j in measures:
            for t in ['min_', 'max_', 'median_', 'var_']:
                if t + str(j) in ret[i]:
                    ret[i][t + str(j)] = float("{:.3f}".format(ret[i][t + str(j)]))
    

    return [i for i in ret.values() if len(i) > 3]


if __name__ == '__main__':
    data = []

    for dataset_name in datasets:
        qrels = list(datasets[dataset_name].qrels_iter())
        data += process_dataset(dataset_name, qrels)

    json.dump(data,  open('ui/src/topics.json', 'w'), indent=4)

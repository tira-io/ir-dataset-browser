from tira.rest_api_client import Client
from tira.tirex import IRDS_TO_TIREX_DATASET
from tqdm import tqdm
import ir_measures
import ir_datasets
from statistics import median
import json
import numpy as np
from construct_indexes import parse_run_details

tira = Client()
datasets = {i: ir_datasets.load(i) for i in [
    #'antique/test', 'argsme/2020-04-01/touche-2020-task-1', 'argsme/2020-04-01/touche-2021-task-1', 'cord19/fulltext/trec-covid', 'cranfield', 'msmarco-passage/trec-dl-2019/judged', 'msmarco-passage/trec-dl-2020/judged', 
                                             'vaswani', ]}

qrels = {n: list(d.qrels_iter()) for n, d in datasets.items()}

MEASURES = [ir_measures.nDCG@10, ir_measures.P@10, ir_measures.Judged@10]

tira_runs = [
    "ir-benchmarks/tira-ir-starter/BM25 Re-Rank (tira-ir-starter-pyterrier)",
    "ir-benchmarks/tira-ir-starter/MonoT5 Base (tira-ir-starter-gygaggle)",
    "ir-benchmarks/tira-ir-starter/MonoT5 Large (tira-ir-starter-gygaggle)",
    "ir-benchmarks/tira-ir-starter/DirichletLM Re-Rank (tira-ir-starter-pyterrier)",
    "ir-benchmarks/tira-ir-starter/TASB msmarco-distilbert-base-dot (tira-ir-starter-beir)"
]


def process_dataset(dataset_name):
    dataset = datasets[dataset_name]
    ret = {}

    for i in dataset.queries_iter():
        ret[str(i.query_id)] = {"dataset": dataset_name, "query_id": str(i.query_id), "default_text": i.default_text()}

    for tira_run in tqdm(tira_runs, desc=f"Processing {dataset_name}"):
        run = ir_measures.read_trec_run(tira.get_run_output(tira_run, IRDS_TO_TIREX_DATASET[dataset_name]) + '/run.txt')

        for i in ir_measures.iter_calc(MEASURES, qrels[dataset_name], run):
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
        for j in MEASURES:
            if 'median_' + str(j) in ret[i]:
                ret[i]['var_' + str(j)] = np.var(ret[i]['median_' + str(j)])
                ret[i]['median_' + str(j)] = median(ret[i]['median_' + str(j)])


    for i in ret:
        for j in MEASURES:
            for t in ['min_', 'max_', 'median_', 'var_']:
                if t + str(j) in ret[i]:
                    ret[i][t + str(j)] = float("{:.3f}".format(ret[i][t + str(j)]))
    

    return [i for i in ret.values() if len(i) > 3]


def relevance_vector(qid, run, qrels):
    ret = []
    qrels = {i.doc_id: i.relevance for i in qrels if i.query_id == qid}

    for i in run:
        if len(ret) > 10:
            break
        if str(i.query_id) == qid:
            # TODO: Add unit test that run is already sorted.
            ret += [str(qrels.get(i.doc_id, 'U'))]

    return ret

def create_run_details(dataset_name):
    dataset = datasets[dataset_name]
    ret = {}
    qid_to_default_text = {str(i.query_id): i.default_text() for i in dataset.queries_iter()}

    for tira_run in tqdm(tira_runs, desc=f"Construct details on runs: {dataset_name}"):
        run = [i for i in ir_measures.read_trec_run(tira.get_run_output(tira_run, IRDS_TO_TIREX_DATASET[dataset_name]) + '/run.txt')]

        for i in ir_measures.iter_calc(MEASURES, qrels[dataset_name], run):
            measure = str(i.measure)
            qid = str(i.query_id)

            if qid not in qid_to_default_text:
                continue

            if qid not in ret:
                ret[qid] = {"dataset": dataset_name, "qid": qid, "default_text": qid_to_default_text[qid], 'runs': {}}

            if tira_run not in ret[qid]['runs']:
                ret[qid]['runs'][tira_run] = {'name': tira_run}

            ret[qid]['runs'][tira_run][measure] = float("{:.3f}".format(i.value))
        
        for qid in ret:
            ret[qid]['runs'][tira_run]['relevance'] = relevance_vector(qid, run, qrels[dataset_name])

    for qid in ret:
        ret[qid]['runs'] = [i for i in ret[qid]['runs'].values()]

    return [i for i in ret.values()]


def main():
    runs = []
    for dataset_name in datasets:
        runs += create_run_details(dataset_name)

    with open('ui/run-details.jsonl', 'w') as f:
        for l in runs:
            f.write(json.dumps(l) + '\n')
    runs = parse_run_details('ui/run-details.jsonl')
    data = []

    for dataset_name in datasets:
        data += process_dataset(dataset_name)
    
    for i in data:
        i['run_details'] = {'start': runs[i['dataset']][i['query_id']]['start'], 'end': runs[i['dataset']][i['query_id']]['end'] - 1, 'path': 'run-details.jsonl'}

    json.dump(data,  open('ui/src/topics.json', 'w'), indent=4)


if __name__ == '__main__':
    main()

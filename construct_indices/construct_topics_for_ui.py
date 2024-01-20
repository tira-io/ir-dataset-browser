#!/usr/bin/env python3
from tira.rest_api_client import Client
from tira.tirex import IRDS_TO_TIREX_DATASET
from tira.ir_datasets_util import ir_dataset_from_tira_fallback_to_original_ir_datasets
from tqdm import tqdm
import ir_measures
ir_datasets = ir_dataset_from_tira_fallback_to_original_ir_datasets()
from statistics import median
import json
import numpy as np
from construct_indexes import parse_run_details, extract_from_remote
import pandas as pd
import gzip

tira = Client()
datasets = {i: ir_datasets.load(i) for i in [

    #'antique/test', 'argsme/2020-04-01/touche-2020-task-1', 'argsme/2020-04-01/touche-2021-task-1', 'cranfield', 'msmarco-passage/trec-dl-2019/judged', 'msmarco-passage/trec-dl-2020/judged',
    'ir-lab-jena-leipzig-wise-2023/validation-20231104-training',
    #'vaswani', 
                                             #'cord19/fulltext/trec-covid', 
                                             ]}

datasets_to_index = {
    'antique/test': 'static/indexes/antique.json.gz',
    'argsme/2020-04-01/touche-2020-task-1': 'static/indexes/argsme.json.gz',
    'argsme/2020-04-01/touche-2021-task-1': 'static/indexes/argsme.json.gz',
    'cranfield': 'static/indexes/cranfield.json.gz',
    'vaswani': 'static/indexes/vaswani.json.gz',
    'msmarco-passage/trec-dl-2019/judged': 'static/indexes/ms-marco.json.gz',
    'msmarco-passage/trec-dl-2020/judged': 'static/indexes/ms-marco.json.gz',
}

qrels = {n: list(d.qrels_iter()) for n, d in datasets.items()}

MEASURES = [ir_measures.nDCG@10, ir_measures.P@10, ir_measures.Judged@10]
# We only report the median
RANK_NOT_RETRIEVED = 99999

tira_runs = [
#    "ir-benchmarks/tira-ir-starter/BM25 Re-Rank (tira-ir-starter-pyterrier)",
#    "ir-benchmarks/tira-ir-starter/MonoT5 Base (tira-ir-starter-gygaggle)",
#    "ir-benchmarks/tira-ir-starter/MonoT5 Large (tira-ir-starter-gygaggle)",
#    "ir-benchmarks/tira-ir-starter/DirichletLM Re-Rank (tira-ir-starter-pyterrier)",
#    "ir-benchmarks/tira-ir-starter/TASB msmarco-distilbert-base-dot (tira-ir-starter-beir)"


"ir-lab-jena-leipzig-wise-2023/geometric-tortoise/silent-fork",
"ir-lab-jena-leipzig-wise-2023/geometric-tortoise/rounded-teak",
"ir-lab-jena-leipzig-wise-2023/geometric-tortoise/clear-solenoid",
"ir-lab-jena-leipzig-wise-2023/geometric-tortoise/nippy-skin",
"ir-lab-jena-leipzig-wise-2023/geometric-tortoise/recent-cordon",
"ir-lab-jena-leipzig-wise-2023/geometric-tortoise/fast-upload",

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

def run_with_derived_rank(run):
    df = pd.DataFrame([{'query_id': i.query_id, 'doc_id': i.doc_id, 'score': i.score} for i in ir_measures.read_trec_run(run)])

    df = df.sort_values(["query_id", "score", "doc_id"], ascending=[True,False,False]).reset_index()
    df["rank"] = 1
    df["rank"] = df.groupby("query_id")["rank"].cumsum()

    return df

def create_qrel_details(dataset_name, run_files):
    ret = {}
    run_to_qid_to_docid_to_rank = {i: {} for i in run_files}

    for run_name in tqdm(run_files, 'Analyse runs for qrel details'):
        for _, i in run_with_derived_rank(run_files[run_name]).iterrows():
            if i.query_id not in run_to_qid_to_docid_to_rank[run_name]:
                run_to_qid_to_docid_to_rank[run_name][i.query_id] = {}

            if i.doc_id not in run_to_qid_to_docid_to_rank[run_name][i.query_id]:
                run_to_qid_to_docid_to_rank[run_name][i.query_id][i.doc_id] = int(i['rank'])

    doc_id_to_offset = json.load(gzip.open(datasets_to_index[dataset_name], 'rt'))

    for i in qrels[dataset_name]:
        qid = str(i.query_id)
        if qid not in ret:
            ret[qid] = {"dataset": dataset_name, "qid": qid, 'qrels': []}

        ranks = [run_to_qid_to_docid_to_rank[run_name][qid].get(i.doc_id, RANK_NOT_RETRIEVED) for run_name in run_files if qid in run_to_qid_to_docid_to_rank[run_name]]
        median_rank, retrieved_in_100, retrieved_in_10 = None, None, None
        if ranks:
            median_rank = median(ranks)
            retrieved_in_100 = len([i for i in ranks if i <= 100])
            retrieved_in_10 = len([i for i in ranks if i <= 10])

        ret[qid]['qrels'] += [{'qid': i.query_id, 'relevance': i.relevance, 'doc_id': i.doc_id, 'retrieved_in_100': retrieved_in_100, 'median_rank': median_rank, 'retrieved_in_10': retrieved_in_10, 'doc_id_to_offset': doc_id_to_offset[i.doc_id]}]

    return [i for i in ret.values()]

def main():
    static_indexes = json.load(open('ui/src/document_indexes.json'))
    example_docs = {}
    for dataset in datasets:
        with gzip.open(datasets_to_index[dataset], 'rt') as f:
            print(dataset)
            l = f.read(1000)
            l = json.loads("{" + l[1:].split('}')[0] + '}}')
            doc_id = list(l.keys())[0]
            example_doc = json.loads(extract_from_remote(static_indexes[datasets_to_index[dataset]], l[doc_id]['start'], l[doc_id]['end']))

            if doc_id != example_doc['docno']:
                raise ValueError(f'Expected doc_id {doc_id} but found {example_doc["docno"]}.')

            example_docs[dataset] = {doc_id: example_doc}

    json.dump(example_docs, open('ui/src/example-documents.json', 'w'), indent=4)

    runs = []
    for dataset_name in datasets:
        runs += create_run_details(dataset_name)

    with open('ui/run-details.jsonl', 'w') as f:
        for l in runs:
            f.write(json.dumps(l) + '\n')

    qrels = []
    for dataset_name in datasets:
        run_name_to_run_file = {i: tira.get_run_output(i, IRDS_TO_TIREX_DATASET[dataset_name]) + '/run.txt' for i in tira_runs}
        qrels += create_qrel_details(dataset_name, run_name_to_run_file)

    with open('ui/qrel-details.jsonl', 'w') as f:
        for l in qrels:
            f.write(json.dumps(l) + '\n')

    topics = []
    for dataset_name in datasets:
        for i in datasets[dataset_name].queries_iter():
            topic = {"dataset": dataset_name, "qid": str(i.query_id), "default_text": i.default_text()}
            try:
                topic['description'] = i.description
                topic['narrative'] = i.narrative
            except:
                pass

            topics += [topic]

    with open('ui/topic-details.jsonl', 'w') as f:
        for l in topics:
            f.write(json.dumps(l) + '\n')

    topics = parse_run_details('ui/topic-details.jsonl')
    runs = parse_run_details('ui/run-details.jsonl')
    qrels = parse_run_details('ui/qrel-details.jsonl')
    data = []

    for dataset_name in datasets:
        data += process_dataset(dataset_name)
    
    for i in data:
        i['run_details'] = {'start': runs[i['dataset']][i['query_id']]['start'], 'end': runs[i['dataset']][i['query_id']]['end'] - 1, 'path': 'run-details.jsonl'}
        i['qrel_details'] = {'start': qrels[i['dataset']][i['query_id']]['start'], 'end': qrels[i['dataset']][i['query_id']]['end'] - 1, 'path': 'qrel-details.jsonl'}
        i['topic_details'] = {'start': topics[i['dataset']][i['query_id']]['start'], 'end': topics[i['dataset']][i['query_id']]['end'] - 1, 'path': 'qrel-details.jsonl'}

    json.dump(data,  open('ui/src/topics.json', 'w'), indent=4)


if __name__ == '__main__':
    main()

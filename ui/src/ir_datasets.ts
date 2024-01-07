import * as topics from './topics.json'
import * as example_documents from './example-documents.json'

export default topics

let data_access = {
'databases': {
    'argsme/2020-04-01/touche-2020-task-1': 'https://files.webis.de/data-in-progress/dataset-explorer-in-progress/argsme/argsme.db',
    'argsme/2020-04-01/touche-2021-task-1': 'https://files.webis.de/data-in-progress/dataset-explorer-in-progress/argsme/argsme.db',
    'msmarco-passage/trec-dl-2019/judged': 'https://files.webis.de/data-in-progress/dataset-explorer-in-progress/ms-marco/ms-marco.db',
    'msmarco-passage/trec-dl-2020/judged': 'https://files.webis.de/data-in-progress/dataset-explorer-in-progress/ms-marco/ms-marco.db',
  },
  'documents': {
    'argsme/2020-04-01/touche-2020-task-1': 'https://files.webis.de/data-in-progress/dataset-explorer-in-progress/argsme/documents.jsonl',
    'argsme/2020-04-01/touche-2021-task-1': 'https://files.webis.de/data-in-progress/dataset-explorer-in-progress/argsme/documents.jsonl',

    'msmarco-passage/trec-dl-2019/judged': 'https://files.webis.de/data-in-progress/dataset-explorer-in-progress/ms-marco/documents.jsonl',
    'msmarco-passage/trec-dl-2020/judged': 'https://files.webis.de/data-in-progress/dataset-explorer-in-progress/ms-marco/documents.jsonl',
    'antique/test': 'https://files.webis.de/data-in-progress/dataset-explorer-in-progress/antique/documents.jsonl',
    'cranfield': 'https://files.webis.de/data-in-progress/dataset-explorer-in-progress/cranfield/documents.jsonl',
    'vaswani': 'https://files.webis.de/data-in-progress/dataset-explorer-in-progress/vaswani/documents.jsonl',
  }
}

export { data_access, example_documents }
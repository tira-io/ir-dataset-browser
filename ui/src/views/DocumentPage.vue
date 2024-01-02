<template>
  <h2>Document {{ doc_id }} on Dataset {{ ir_dataset }}</h2>
  <v-divider/>

  {{ text }}
</template>

<script lang="ts">
import {execute_get, extractFromUrl} from "@/utils";
import { createDbWorker } from "sql.js-httpvfs"

const workerUrl = new URL(
  "sql.js-httpvfs/dist/sqlite.worker.js",
  import.meta.url,
);
const wasmUrl = new URL(
  "sql.js-httpvfs/dist/sql-wasm.wasm",
  import.meta.url,
);


export default {
  data: () => ({
    ir_dataset: extractFromUrl('dataset'),
    doc_id: extractFromUrl('doc_id'),
    databases: {
      'argsme/2020-04-01/touche-2020-task-1': 'https://files.webis.de/data-in-progress/dataset-explorer-in-progress/argsme/argsme.db',
      'argsme/2020-04-01/touche-2021-task-1': 'https://files.webis.de/data-in-progress/dataset-explorer-in-progress/argsme/argsme.db',
      'msmarco-passage/trec-dl-2019/judged': 'https://files.webis.de/data-in-progress/dataset-explorer-in-progress/ms-marco/ms-marco.db',
      'msmarco-passage/trec-dl-2020/judged': 'https://files.webis.de/data-in-progress/dataset-explorer-in-progress/ms-marco/ms-marco.db',
    },
    documents: {
      'argsme/2020-04-01/touche-2020-task-1': 'https://files.webis.de/data-in-progress/dataset-explorer-in-progress/argsme/documents.jsonl',
      'argsme/2020-04-01/touche-2021-task-1': 'https://files.webis.de/data-in-progress/dataset-explorer-in-progress/argsme/documents.jsonl',

      'msmarco-passage/trec-dl-2019/judged': 'https://files.webis.de/data-in-progress/dataset-explorer-in-progress/ms-marco/documents.jsonl',
      'msmarco-passage/trec-dl-2020/judged': 'https://files.webis.de/data-in-progress/dataset-explorer-in-progress/ms-marco/documents.jsonl',
    },
    text: 'loading...',
  }),
  methods: {
    async load_document_id() {
      console.log(this.databases[this.ir_dataset])
      const config = {
        from: "inline",
        config: {
          serverMode: "full", // file is just a plain old full sqlite database
          requestChunkSize: 4096, // the page size of the  sqlite database (by default 4096)
          url: this.databases[this.ir_dataset],
        },
      }

      const maxBytesToRead = 10 * 1024 * 1024;
      const worker = await createDbWorker([config], workerUrl.toString(), wasmUrl.toString(), maxBytesToRead);

      let result = await worker.db.exec(`select * from documents where id = ?`, [this.doc_id])//[0]['values'];
      result = result[0]['values'][0]
      result = result[1] + '-' + (result[2] -1)
      execute_get(this.documents[this.ir_dataset], result).then((i) => this.text = i);

      //execute_get(this.documents[this.ir_dataset], '70105-70847').then((i) => this.text = i);
      //execute_get(this.documents['argsme/2020-04-01/touche-2020-task-1'], '203105782-203106329').then((i) => this.text = i);*/
    },
  },
  beforeMount() {
    this.load_document_id();
  },
}
</script>

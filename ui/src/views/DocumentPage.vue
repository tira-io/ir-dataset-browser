<template>
  <v-row class="ma-2">
    <v-col cols="4">
      <v-autocomplete clearable label="Select dataset &hellip;" v-model="ir_dataset" :items="uniqueElements(topics, 'dataset')"/>
    </v-col>
    <v-col cols="4">
      <v-text-field clearable :disabled="!ir_dataset" label="Document IDs (comma seperated) &hellip;" v-model="doc_ids"/>
    </v-col>

    <v-col cols="4">
      <v-btn block size="large" :disabled="!ir_dataset || !doc_ids" color="primary" @click="load_document_id">Load</v-btn>
    </v-col>
  </v-row>

  <v-row class="ma-2" v-if="ir_dataset && (!texts || !texts[ir_dataset] || !texts[ir_dataset][doc_id_iter[0]] || texts[ir_dataset][doc_id_iter[0]] == 'loading...')">
    <v-col cols="4"/>
    <v-col cols="4">Example Document ID: {{ Object.keys(texts[ir_dataset])[0] }}</v-col>
    <v-col cols="4"/>
  </v-row>

  <v-divider v-if="texts[ir_dataset]"/>

  <div v-if="texts[ir_dataset]" v-for="doc_id of doc_id_iter">
    <div v-if="texts[ir_dataset][doc_id] && texts[ir_dataset][doc_id] != 'loading...'">  
      <h1 class="font-weight-bold text-h2 text-center justify-center py-6">Document: {{doc_id}}</h1>
      <v-textarea readonly class="ma-2" v-model="texts[ir_dataset][doc_id]['text']" label="Default Text"/>
    </div>
  </div>
</template>

<script lang="ts">
import { extractFromUrl, uniqueElements, updateUrl } from "@/utils"
import { load_document } from "@/random_document_access"
import { data_access, example_documents } from "@/ir_datasets"
import topics from '@/ir_datasets';


export default {
  data: () => ({
    topics: topics.default,
    ir_dataset: extractFromUrl('dataset'),
    doc_ids: extractFromUrl('doc_ids'),
    example_doc_id: '<TBD>',
    texts: {...example_documents.default},
  }),
  methods: {
    async load_document_id() {
      updateUrl(null, this.ir_dataset, null, this.doc_ids);

      if (!(this.ir_dataset in data_access.databases)) {
        this.ir_dataset = null;
      }

      if (!(this.ir_dataset in this.texts)) {
        this.texts[this.ir_dataset] = {}
      }

      for (let doc_id of this.doc_id_iter) {
        if (this.ir_dataset && doc_id && !(doc_id in this.texts[this.ir_dataset])) {
          load_document(this.ir_dataset, doc_id).then(i => this.texts[this.ir_dataset][doc_id] = {'text': i.text})
        }
      }
    },
    uniqueElements(element: any[], key: string) {
      return uniqueElements(element, key)
    },
  },
  computed: {
    doc_id_iter() {
      return this.doc_ids ? this.doc_ids.split(',') : []
    },
  },
  watch: {
    ir_dataset: function () { this.load_document_id() }
  },
  beforeMount() {
    this.load_document_id();
  },
}
</script>

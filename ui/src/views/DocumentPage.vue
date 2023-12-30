<template>
  <h2>Document {{ doc_id }} on Dataset {{ ir_dataset }}</h2>
  <v-divider/>

  {{ text }}
</template>

<script lang="ts">
import {get, extractFromUrl} from "@/utils";

export default {
  data: () => ({
    ir_dataset: extractFromUrl('ir_dataset_id'),
    doc_id: extractFromUrl('doc_id'),
    text: 'loading...',
  }),
  beforeMount() {
    get('/api/docs?ir_dataset_id=' + this.ir_dataset + '&doc_id=' + this.doc_id, this)
  },
}
</script>

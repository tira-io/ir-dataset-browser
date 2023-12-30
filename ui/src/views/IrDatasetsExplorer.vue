<template>
  <h1 class="font-weight-bold text-h2 text-center justify-center py-6">
    ir_datasets Explorer
  </h1>

  <div class="d-flex">
    <v-data-table v-model="selected_topics" :items="filtered_topics" item-value="query_id" :headers="headers" show-select hover dense>
    <template v-slot:header.dataset="{ header }">
      <v-text-field clearable label="Filter datasets &hellip;" prepend-inner-icon="mdi-magnify" variant="underlined" v-model="dataset_filter"/>
      Dataset
    </template>
    <template v-slot:header.query_id="{ header }">
      <v-text-field clearable label="Filter number &hellip;" prepend-inner-icon="mdi-magnify" variant="underlined" v-model="topic_num_filter"/>
      Num
    </template>
    <template v-slot:header.default_text="{ header }">
      <v-text-field clearable label="Filter queries &hellip;" prepend-inner-icon="mdi-magnify" variant="underlined" v-model="query_filter"/>
      Query
    </template>
    <template v-slot:footer.prepend>
        <v-select menu-icon="mdi-cog" variant="plain" :items="['Dataset', 'Topic', 'Query', 'nDCG@10 (Best)', 'nDCG@10 (Median)', 'nDCG@10 (Worst)']" hide-headers multiple style="max-width: 100px;" class="ma-2">
          <template v-slot:selection="{ item, index }"/>
        </v-select>
      </template>
    </v-data-table>
  </div>


  <div class="d-flex" v-if="!selected_topics">
    Please select topics for browsing in the table above.
  </div>

  <div v-if="selected_topics">
    <v-card color="primary">
    <v-card-title class="text-center justify-center py-6">
      <h1 class="font-weight-bold text-h2">
        Browse {{ selected_topics }} Topics
      </h1>
    </v-card-title>

    <v-tabs v-model="tab" bg-color="primary">
      <v-tab value="details">Details</v-tab>
      <v-tab value="qrels">Relevance Judgments</v-tab>
      <v-tab value="runs">Runs</v-tab>
    </v-tabs>
  </v-card>
  </div>
</template>

<script lang="ts">
import topics from '@/ir_datasets';
import {extractFromUrl, updateUrl} from "@/utils";

export default {
  name: "ir-datasets-explorer",
  components: {},
  data() {
    return {
      topic_num_filter: extractFromUrl('topic'),
      dataset_filter: extractFromUrl('dataset'),
      query_filter: extractFromUrl('query'),
      tab: null,
      selected_topics: null,
      topics: topics,
      headers: [
        { title: 'Dataset', value: 'dataset', sortable: false},
        { title: 'Num', value: 'query_id', sortable: false},
        { title: 'Query', value: 'default_text', sortable: false},
        { title: 'nDCG@10', value: 'measure', align: 'center', children: [{ title: 'Best', value: 'best_ndcg_cut_10', sortable: true}, { title: 'Median', value: 'median_ndcg_cut_10', sortable: true}, { title: 'Worst', value: 'worst_ndcg_cut_10', sortable: true}]}
      ]
    }
  },
  methods: {
    updateFilter() {
      updateUrl(this.topic_num_filter, this.dataset_filter, this.query_filter);
    }
  },
  beforeMount() {
  },
  watch: {
    topic_num_filter: function () { this.updateFilter() },
    dataset_filter: function () { this.updateFilter() },
    query_filter: function () { this.updateFilter() },
  },
  computed: {
    filtered_topics() {
      let topics = this.topics
      if (this.topic_num_filter) {
        topics = topics.filter(topic => topic.query_id.includes(this.topic_num_filter))
      }

      if (this.dataset_filter) {
        topics = topics.filter(topic => topic.dataset.includes(this.dataset_filter))
      }

      if (this.query_filter) {
        topics = topics.filter(topic => topic.default_text.includes(this.query_filter))
      }

      return topics;
    }
  }
}
</script>

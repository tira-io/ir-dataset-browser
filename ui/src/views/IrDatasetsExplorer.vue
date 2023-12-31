<template>
  <h1 class="font-weight-bold text-h2 text-center justify-center py-6">
    ir_datasets Explorer
  </h1>

  <div class="d-flex">
    <v-data-table v-model="selected_topics" :items="filtered_topics" item-value="query_id" :headers="filtered_headers" show-select hover dense>
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
        <v-select menu-icon="mdi-cog" variant="plain" v-model="selected_headers" item-title="name" item-value="value" :items="available_headers" hide-headers multiple style="max-width: 100px;" class="ma-2">
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
import {is_mobile} from "@/main";

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
      selected_headers: is_mobile() ? ['dataset', 'default_text'] : ['dataset', 'query_id', 'default_text', 'max_ndcg_cut_10', 'median_ndcg_cut_10', 'min_ndcg_cut_10'],
      available_headers: [
        {name: 'Dataset', value: 'dataset'},
        {name: 'Topic', value: 'query_id'},
        {name: 'Query', value: 'default_text'},
        {name: 'nDCG@10 (Maximum)', value: 'max_ndcg_cut_10'},
        {name: 'nDCG@10 (Median)', value: 'median_ndcg_cut_10'},
        {name: 'nDCG@10 (Minimum)', value: 'min_ndcg_cut_10'},
        {name: 'Unjudged@10 (Maximum)', value: 'max_unjudged_cut_10'},
        {name: 'Unjudged@10 (Median)', value: 'median_unjudged_cut_10'},
        {name: 'Unjudged@10 (Minimum)', value: 'min_unjudged_cut_10'},
        {name: 'Precision@10 (Maximum)', value: 'max_precision_cut_10'},
        {name: 'Precision@10 (Median)', value: 'median_precision_cut_10'},
        {name: 'Precision@10 (Minimum)', value: 'min_precision_cut_10'}
      ],
      headers: [
        { title: 'Dataset', value: 'dataset', sortable: false},
        { title: 'Num', value: 'query_id', sortable: false},
        { title: 'Query', value: 'default_text', sortable: false},

        { title: 'nDCG@10', value: 'ndcg_cut_10', align: 'center', children: [{ title: 'Maximum', value: 'max_ndcg_cut_10', sortable: true}, { title: 'Median', value: 'median_ndcg_cut_10', sortable: true}, { title: 'Minimum', value: 'min_ndcg_cut_10', sortable: true}]},
        { title: 'Unjudged@10', value: 'unjudged_cut_10', align: 'center', children: [{ title: 'Maximum', value: 'max_unjudged_cut_10', sortable: true}, { title: 'Median', value: 'median_unjudged_cut_10', sortable: true}, { title: 'Minimum', value: 'min_unjudged_cut_10', sortable: true}]},

        { title: 'Precision@10', value: 'precision_cut_10', align: 'center', children: [{ title: 'Maximum', value: 'max_precision_cut_10', sortable: true}, { title: 'Median', value: 'median_precision_cut_10', sortable: true}, { title: 'Minimum', value: 'min_precision_cut_10', sortable: true}]},
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
    },
    filtered_headers() {
      let headers = this.headers
      if (this.selected_headers.length > 0) {
        headers = headers.filter(header => this.selected_headers.includes(header.value))
      }
      var add_separator = false
      for (let header of this.headers) {
        header = {...header}
        if (!header.children) {
          continue
        }
        header.children = header.children.filter(child => this.selected_headers.includes(child.value))

        if (header.children.length > 0) {
          if (add_separator) {
            headers.push({title: '', value: header.value + '_sep', sortable: false})
          }
          add_separator = true

          headers.push(header)
        }
      }

      return headers
    }
  }
}
</script>

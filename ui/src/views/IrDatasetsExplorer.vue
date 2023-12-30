<template>
  <div class="d-flex">
    <v-data-table v-model="selected_topics" :items="topics" item-value="query_id" show-select hover>
    <template v-slot:header.query_id="{ header }">
      <v-text-field clearable label="Filter number &hellip;" prepend-inner-icon="mdi-magnify" variant="underlined" v-model="dataset_filter"/>
      Num
    </template>
    <template v-slot:header.dataset="{ header }">
      <v-text-field clearable label="Filter datasets &hellip;" prepend-inner-icon="mdi-magnify" variant="underlined" v-model="topic_num_filter"/>
      Dataset
    </template>
      
    <template v-slot:header.default_text="{ header }">
      <v-text-field clearable label="Filter queries &hellip;" prepend-inner-icon="mdi-magnify" variant="underlined" v-model="query_filter"/>
      Query
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
export default {
  name: "ir-datasets-explorer",
  components: {},
  data() {
    return {
      topic_num_filter: null,
      dataset_filter: null,
      query_filter: null,
      tab: null,
      selected_topics: null,
      topics: [
        {'dataset': 'argsme/2020-04-01/touche-2020-task-1', 'query_id': '1', 'default_text': 'test 1'},
        {'dataset': 'argsme/2020-04-01/touche-2020-task-1', 'query_id': '2', 'default_text': 'test 2'},
        {'dataset': 'argsme/2020-04-01/touche-2020-task-1', 'query_id': '3', 'default_text': 'test 3'},
        {'dataset': 'argsme/2020-04-01/touche-2020-task-1', 'query_id': '4', 'default_text': 'test 4'},
        {'dataset': 'argsme/2020-04-01/touche-2020-task-1', 'query_id': '5', 'default_text': 'test 5'},
        {'dataset': 'argsme/2020-04-01/touche-2020-task-1', 'query_id': '6', 'default_text': 'test 6'},
        {'dataset': 'argsme/2020-04-01/touche-2020-task-1', 'query_id': '7', 'default_text': 'test 7'},
        {'dataset': 'argsme/2020-04-01/touche-2020-task-1', 'query_id': '8', 'default_text': 'test 8'},
        {'dataset': 'argsme/2020-04-01/touche-2020-task-1', 'query_id': '9', 'default_text': 'test 9'},
        {'dataset': 'argsme/2020-04-01/touche-2020-task-1', 'query_id': '10', 'default_text': 'test 10'},
        {'dataset': 'argsme/2020-04-01/touche-2020-task-1', 'query_id': '11', 'default_text': 'test 11'},
        {'dataset': 'argsme/2020-04-01/touche-2020-task-1', 'query_id': '12', 'default_text': 'test 12'},
      ],
    }
  },
  beforeMount() {
  }
}
</script>

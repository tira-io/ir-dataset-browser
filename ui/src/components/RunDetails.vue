<template>
  <h3>Topic {{topics[0].query_id}} ({{topics[0].dataset}})</h3>

  <loading :loading="is_loading"/>

  <v-data-table v-model="selected_runs" :items="filtered_runs" :headers="headers" item-value="dataset_id_and_query_id_and_run_id" v-if="!is_loading" show-select hover dense>
    <template v-slot:item.relevance="{ item }">
      <dense-run-overview :judgments="item.relevance" />
    </template>
  </v-data-table>

  <!--<div class="d-flex" v-if="selected_runs">Reference run: {{ reference_run_id }}</div>-->
  <div class="d-flex" v-if="selected_runs && !is_loading">
    <v-row v-if="selected_runs" class="justify-center mx-2">
      <v-col :cols="columns" v-for="selected_run of selected_runs">
        <serp :run="selected_run" :topic="topics[0]" :topic_details="topic_details"/>
      </v-col>
    </v-row>
  </div>
</template>
  
<script lang="ts">
  import { get } from '@/utils'
  import DenseRunOverview from './DenseRunOverview.vue'
  import Serp from '@/components/Serp.vue'
  import {is_mobile} from "@/main";
  import Loading from './Loading.vue'
  
  export default {
    name: "run-details",
    props: ['topics'],
    components: {DenseRunOverview, Serp, Loading},
    watch: {
      topics(newValue) {this.fetchData()},
    },
    data() {
      return {
        cache: {'run-details.jsonl': {'start: 0 end: 100': {'runs': [{'name': 'does not exist', "P@10": 0.3, "nDCG@10": 0.203, "Judged@10": 0.3, 'relevance': ['U', '0', '1']}]}}},
        selected_runs: null,
        headers: [
          {title: 'System', value: 'name', sortable: true},
          {title: 'P@10', value: 'P@10', sortable: true},
          {title: 'nDCG@10', value: 'nDCG@10', sortable: true},
          {title: 'Judged@10', value: 'Judged@10', sortable: true},
          {title: 'Relevance', value: 'relevance', sortable: false}
        ],
        is_loading_per_topic: {},
      }
    },
    methods: {
      fetchData() {

        for (var topic of this.topics) {
          this.is_loading_per_topic[topic['run_details']] = true
          get(topic['run_details'], this).then(() => {
            this.is_loading_per_topic[topic['run_details']] = false
          })
        }
      },
    },
    computed: {
      filtered_runs() {
        let ret = []

        for (let topic of this.topics) {
          let entry = this.cache['run-details.jsonl'][topic['run_details']['start'] + '-' + topic['run_details']['end']]
          if (entry) {
            if (topic['dataset'] != entry['dataset']) {
                throw new Error('dataset mismatch')
            }

            if (topic['query_id'] != entry['qid']) {
                throw new Error('query_id mismatch')
            }

            for (var run of entry['runs']) {
              run = {...run}
              run['dataset'] = topic['dataset']
              run['query_id'] = topic['query_id']
              run['dataset_id_and_query_id_and_run_id'] = run['dataset'] + '____' + run['name'] + '____' + run['query_id']
              ret.push(run)
            }
          }
        }

        return ret;
      },
      is_loading() {
        if (!this.is_loading_per_topic) {
          return true
        }
        for (const [key, value] of Object.entries(this.is_loading_per_topic)) {
          if (value) {
            return true
          }
        }
        return false
      },
      columns() {
        if(is_mobile()) {
          return 12
        }

        return Math.floor(12 / this.selected_runs.length)
      },
      topic_details() {
        return this.cache['run-details.jsonl'][this.topics[0]['run_details']['start'] + '-' + this.topics[0]['run_details']['end']]
      },
    },
    beforeMount() {
      this.fetchData();
    }
  }
  </script>
  
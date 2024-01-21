<template>
  <h3>Topic {{topics[0].query_id}} ({{topics[0].dataset}})</h3>

  <v-data-table v-model="selected_runs" :items="filtered_runs" :headers="headers" show-select hover dense>
    <template v-slot:item.relevance="{ item }">
      <dense-run-overview :judgments="item.relevance" />
    </template>
  </v-data-table>
</template>
  
<script lang="ts">
  import { get } from '@/utils'
  import DenseRunOverview from './DenseRunOverview.vue'
  
  export default {
    name: "run-details",
    props: ['topics'],
    components: {DenseRunOverview},
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
        ]
      }
    },
    methods: {
      fetchData() {
        for (var topic of this.topics) {
          get(topic['run_details'], this)
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
              ret.push(run)
            }
          }
        }

        return ret;
      }
    },
    beforeMount() {
      this.fetchData();
    }
  }
  </script>
  
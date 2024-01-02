<template>
  <h3>Topic {{topics[0].query_id}} ({{topics[0].dataset}})</h3>

  <v-data-table v-model="selected_runs" :items="filtered_runs" show-select hover dense />
</template>
  
<script lang="ts">
  import { get } from '@/utils'
  
  export default {
    name: "run-details",
    props: ['topics'],
    watch: {
      topics(newValue) {this.fetchData()},
    },
    data() {
      return {
        cache: {'run-details.jsonl': {'start: 0 end: 100': {'runs': [{'name': 'does not exist', "P@10": 0.3, "nDCG@10": 0.203, "Judged@10": 0.3, 'relevance': ['U', '0', '1']}]}}},
        selected_runs: null
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
  
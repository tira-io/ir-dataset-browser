<template>
    <h1>Qrel Details</h1>
  
    <v-data-table v-model="selected_runs" :items="filtered_qrels" show-select hover dense />
  
    <h1>TODO: Add visualization(s) and implement the dummy columns.</h1>
  </template>
    
  <script lang="ts">
    import { get } from '@/utils'
    
    export default {
      name: "qrel-details",
      props: ['topics'],
      watch: {
        topics(newValue) {this.fetchData()},
      },
      data() {
        return {
          cache: {'qrel-details.jsonl': {'0-100': {'qrels': [{"qid": "93", "relevance": 1, "doc_id": "182", "retrieved_by": "?? / ??", "median_rank": "??", "var_rank": "??"}]}}},
          selected_runs: null
        }
      },
      methods: {
        fetchData() {
          for (var topic of this.topics) {
            get(topic['qrel_details'], this)
          }
        },
      },
      computed: {
        filtered_qrels() {
          let ret = []
  
          for (let topic of this.topics) {
            let entry = this.cache['qrel-details.jsonl'][topic['qrel_details']['start'] + '-' + topic['qrel_details']['end']]
            if (entry) {
              if (topic['dataset'] != entry['dataset']) {
                  throw new Error('dataset mismatch')
              }
  
              if (topic['query_id'] != entry['qid']) {
                  throw new Error('query_id mismatch')
              }
  
              for (var qrel of entry['qrels']) {
                qrel = {...qrel}
                qrel['dataset'] = topic['dataset']
                qrel['query_id'] = topic['query_id']
                ret.push(qrel)
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
    
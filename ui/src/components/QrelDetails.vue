<template>
    <h3>Topic {{topics[0].query_id}} ({{topics[0].dataset}})</h3>
  
    <v-data-table :items="filtered_qrels" :headers="filtered_headers" hover dense />
  </template>
    
  <script lang="ts">
    import { get } from '@/utils'
    
    export default {
      name: "qrel-details",
      props: ['topics', 'selected_qrel_headers'],
      watch: {
        topics(newValue) {this.fetchData()},
        selected_qrel_headers(newValue) {this.fetchData()},
      },
      data() {
        return {
          cache: {'qrel-details.jsonl': {'0-100': {'qrels': [{"qid": "93", "relevance": 1, "doc_id": "182", "retrieved_by": "?? / ??", "median_rank": "??", "var_rank": "??"}]}}},
          available_headers: [
            {title: 'Document', value: 'doc_id', sortable: true},
            {title: 'Relevance', value: 'relevance', sortable: true},
            {title: 'Median Rank', value: 'median_rank', sortable: true},
            {title: 'Retrieved (Top 10)', value: 'retrieved_in_10', sortable: true},
            {title: 'Retrieved (Top 100)', value: 'retrieved_in_100', sortable: true},
          ],
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
        }, filtered_headers() {
          return this.available_headers.filter((i) => this.selected_qrel_headers.includes(i.value))
        }
      },
      beforeMount() {
        this.fetchData();
      }
    }
    </script>
    
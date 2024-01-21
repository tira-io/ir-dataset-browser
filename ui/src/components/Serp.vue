<template>
  <div>
    <h3>{{ title }}</h3>
    <br>
    ToDo integrate DiffIR to render the runs :)
  </div>
<!--
  <v-row v-for="doc in ranking_2">
    <v-card class="ma-1 w-100 text-start" max-width="1500" :color="doc.color" variant="tonal" style="cursor: pointer;">
      <v-card-item>
        <span class="text-h6 mb-1">{{ doc.doc_id }}</span>
      </v-card-item>
    </v-card>
  </v-row>
-->
</template>

<script lang="ts">
import { get } from '@/utils'
import topics from '@/ir_datasets';

export default {
  name: "serp",
  props: ['run', 'topic'],
  watch: {
    topics(newValue) {this.fetchData()},
  },
  data() {
    return {
      ranking: [{'doc_id': '1', 'relevance': 1, 'color': 'green'}, {'doc_id': '2', 'relevance': 0, 'color': 'red'}, {'doc_id': '3', 'relevance': 'U', 'color': 'grey'}],
      cache: {
        'run-details.jsonl': {'start: 0 end: 100': {'runs': [{'name': 'does not exist', "P@10": 0.3, "nDCG@10": 0.203, "Judged@10": 0.3, 'relevance': ['U', '0', '1'], "docs": [{'doc_id': '1', 'doc_id_to_offset': {'start': 0, 'end': 0}}]}], 'dataset': '1', 'qid': '1'}}
      }
    }
  },
  methods: {
    fetchData() {
        get(this.topic_data['run_details'], this)
    },
  },
  computed: {
    title() {
      return this.run.split('____')[1].split('/')[2]
    },
    topic_data() {
      let expected_dataset = this.run.split('____')[0]
      for (let t of topics.default) {
        if (t.dataset == expected_dataset) {
          return t
        }
      }
    },
    ranking_2() {
      let entry = this.cache['run-details.jsonl'][this.topic_data['run_details']['start'] + '-' + this.topic_data['run_details']['end']]
      let run_id = this.run.split('____')[1]
      if (entry) {
        for (var run of entry['runs']) {
          if (run['name'] == run_id) {
            let ret = [...run['docs']]
            for (let i in ret) {
                ret[i]['color'] = 'grey'

                if (parseInt(run['relevance'][i]) > 0) {
                    ret[i]['color'] = 'green'
                }
                if (parseInt(run['relevance'][i]) <= 0) {
                    ret[i]['color'] = 'red'
                }
            }

            return ret
          }
        }
      }

      return []
    }
  },
  beforeMount() {
    this.fetchData();
  }
}
</script>

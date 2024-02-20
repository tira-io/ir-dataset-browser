<template>
<div>
  <h3>Topic {{topic.query_id}} ({{topic.dataset}})</h3>

  <loading :loading="is_loading"/>
  
  <span v-if="!is_loading"><b>Title: </b> {{title}}<br></span>
  <span v-if="!is_loading && description"><b>Description: </b> {{description}}<br></span>
  <span v-if="!is_loading && narrative"><b>Narrative: </b> {{narrative}}<br></span>
</div>
</template>
    
<script lang="ts">
  import { execute_get } from '@/utils'
  import Loading from './Loading.vue'

  export default {
    name: "topic-details",
    components: {Loading},
    props: ['topic'],
    watch: {
      topics(newValue) {this.fetchData()},
    },
    data() {
      return {
        title: '',
        description: '',
        narrative: '',
        is_loading: true
      }
    },
    methods: {
      fetchData() {
        this.is_loading = true
        this.title = ''
        this.description = ''
        this.narrative = ''
        if(this.topic['topic_details']['end']) {
          execute_get('topic-details.jsonl', this.topic['topic_details']['start'] + '-' + this.topic['topic_details']['end']).then(i => {
            this.title = i['default_text']
            this.description = i['description']
            this.narrative = i['narrative']
            this.is_loading = false
          });
        }
      },
    },
    beforeMount() {
      this.fetchData();
    }
  }
</script>
    
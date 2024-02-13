<template>
  <v-toolbar density="compact" title="ir_datasets Browser">
    <v-tabs v-if="!is_mobile">
      <v-tab to="/ir-dataset-browser/">About</v-tab>
      <v-tab to="/ir-dataset-browser/topics">Browse Topics</v-tab>
      <v-tab to="/ir-dataset-browser/docs">Browse Documents</v-tab>
      <v-tab to="/ir-dataset-browser/runs">Browse Runs</v-tab>
      <!--<v-tab to="/ir-dataset-browser/qrels">Browse Qrels</v-tab>-->
    </v-tabs>
    <v-menu v-if="is_mobile">
      <template v-slot:activator="{ props }">
        <v-btn icon="mdi-menu" v-bind="props"></v-btn>
      </template>
      <v-list>
        <v-list-item to="/ir-dataset-browser/">About</v-list-item>
        <v-list-item to="/ir-dataset-browser/topics">Browse Topics</v-list-item>
        <v-list-item to="/ir-dataset-browser/docs">Browse Documents</v-list-item>
        <v-list-item to="/ir-dataset-browser/runs">Browse Runs</v-list-item>
        <!--<v-list-item to="/ir-dataset-browser/qrels">Browse Qrels</v-list-item>-->
      </v-list>
    </v-menu>
  </v-toolbar>
  <router-view />
</template>

<script lang="ts">
import {ref} from 'vue'
import {is_mobile} from "@/main";

export default {
  data: () => ({
    text: 'loading...',
    is_mobile: is_mobile(),
  }),
  computed: {
    currentRouteName() {
      return this.$route;
    },
    urlSuffix() {
      return (ref(window.location).value.href + '?').split('?')[1]
    }
  }
}
</script>

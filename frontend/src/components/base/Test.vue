<template>
  <div style="margin: 100px;">
    <v-dialog v-model="dialog" width="500">
      <template v-slot:activator="{ on }">
        <v-btn color="red lighten-2" dark v-on="on">Click Me</v-btn>
      </template>

      <v-card>
        <v-card-title class="headline grey lighten-2" primary-title>영현이 자넨 해고야.</v-card-title>

        <v-img src="../../assets/toyh.jpg" />
        <v-divider></v-divider>

        <v-card-actions>
          <div class="flex-grow-1"></div>

          <v-btn @click="testing()">영현이 자네는 해고야</v-btn>
          <v-btn color="primary" text @click="dialog = false">I accept</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import Axios from "axios";

export default {
  data() {
    return {
      dialog: false
    };
  },
  methods: {
    testing() {
      Axios.get("/api/test/content/").then(ret => {
        console.log(ret);
      });
    }
  }
};
</script>
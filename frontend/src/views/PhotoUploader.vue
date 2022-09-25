<template>
  <div>
    <DragAndDrop
      dropTitle="Drop Image Files Here"
      @my-drop="
        if ($event['etype'] == 'image')
          load_files.push.apply(load_files, $event['files']);
        ImageUpload();
      "
    >
      <v-file-input
        class="hide"
        v-model="load_files"
        counter
        label="File input"
        multiple
        accept="image/png, image/jpeg, image/gif"
        placeholder="Select or drop files here"
        prepend-icon="mdi-file-music"
        :show-size="1000"
        type="file"
      >
      </v-file-input>
    </DragAndDrop>
    <v-row>
      <v-col v-for="item in image_items" :key="item" cols="auto">
        <v-card width="200px" height="200px" ripple>
          <v-img :src="item" width="100%" height="100%">
            <template v-slot:placeholder>
              <v-row class="fill-height ma-0" align="center" justify="center">
                <v-progress-circular indeterminate></v-progress-circular
              ></v-row>
            </template>
          </v-img>
        </v-card>
      </v-col>
    </v-row>
    <!-- テストボタン -->
    <v-btn color="blue-grey" class="ma-2 white--text" @click="GetUriList()">
      GET IMAGE_URI FROM STORAGE
      <v-icon right dark> mdi-file-replace </v-icon>
    </v-btn>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import axios from "axios";
import DragAndDrop from "../components/DragAndDrop.vue";
export default Vue.extend({
  components: { DragAndDrop },
  data() {
    return {
      load_files: [],
      image_items: []
    };
  },
  methods: {
    GetUriList() {
      axios
        .get("/api/get_images", { responseType: "json" })
        .then(response => {
          const n_response = JSON.parse(response.data);
          this.image_items.push.apply(this.image_items, n_response.fileList);
        })
        .catch(error => {
          console.log(error.response);
          alert("cant connect api server");
        });
    },
    ImageUpload() {
      console.log(this.load_files);
      for (const data in this.load_files) {
        console.log(data);
      }
    }
  }
});
</script>

<style scoped>
.hide {
  display: none;
}
</style>

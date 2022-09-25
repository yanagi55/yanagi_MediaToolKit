<template>
  <div>
    <DragAndDrop
      dropTitle="Audio Files"
      @my-drop="
        if ($event['type'] === 'audio/mpeg')
          load_files.push.apply(load_files, $event['files']);
      "
    >
      <v-file-input
        v-model="load_files"
        counter
        label="File input"
        multiple
        accept="audio/mpeg"
        placeholder="Select or drop files here"
        prepend-icon="mdi-file-music"
        :show-size="1000"
        type="file"
        @click:clear="button_disabled = true"
      >
        <template v-slot:selection="{ index, text }">
          <v-chip v-if="index < 20" label small>
            {{ text }}
          </v-chip>
          <span
            v-else-if="index === 20"
            class="text-overline grey--text text--darken-3 mx-2"
          >
            +{{ load_files.length - 20 }} File(s)
          </span>
        </template>
      </v-file-input>
    </DragAndDrop>

    <DragAndDrop
      dropTitle="Cover Image"
      @my-drop="
        if ($event['etype'] == 'image')
          load_images.push.apply(load_images, $event['files']),
            LoadImageCover();
      "
    >
      <v-file-input
        v-model="load_images"
        counter
        label="File input"
        multiple
        accept="image/png, image/jpeg, image/bmp"
        placeholder="Select or drop files here"
        prepend-icon="mdi-file-image"
        :show-size="1000"
        type="file"
        @change="LoadImageCover()"
        @click:clear="ResetImage()"
      >
      </v-file-input>
    </DragAndDrop>
    <v-img :src="image_preview" width="200px" height="200px"></v-img>

    <v-btn
      color="blue-grey"
      class="ma-2 white--text"
      @click="MultiReplaceAudioCover()"
      :loading="button_progress"
      :disabled="button_disabled"
    >
      REPLACE
      <v-icon right dark> mdi-file-replace </v-icon>
    </v-btn>
    <!-- <span>MAX:40MB</span> -->
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import DragAndDrop from "../components/DragAndDrop.vue";
import axios from "axios";

export default Vue.extend({
  components: { DragAndDrop },
  data() {
    return {
      load_files: [],
      load_images: [],
      image_preview: String(),
      button_progress: Boolean(false),
      button_disabled: Boolean(true)
    };
  },
  methods: {
    MultiReplaceAudioCover() {
      for (const data of this.load_files) {
        console.log(data);
        const form = new FormData();
        form.append("audio", data);
        form.append("image", this.load_images[0]);
        form.append("token", "tokentest");

        this.button_progress = true;
        axios
          .post("/api/embed_image_on_mp3", form, { responseType: "blob" })
          .then(response => {
            console.log("mp3 returned");
            const blob = new Blob([response.data]);
            const link = document.createElement("a");
            link.href = window.URL.createObjectURL(blob);
            const download_name = response.headers["content-disposition"].split(
              "filename*=utf-8''"
            )[1];
            link.download = decodeURI(download_name);
            link.click();
          })
          .catch(error => {
            console.log(error.response);
            alert("Error occurred in backend.");
          })
          .finally(() => {
            this.button_progress = false;
          });
      }
    },
    LoadImageCover() {
      if (this.load_images[0]) {
        this.image_preview = URL.createObjectURL(this.load_images[0]);
      }
    },
    ResetImage() {
      URL.revokeObjectURL(this.image_preview);
      this.image_preview = "";
      this.button_disabled = true;
    }
  },
  watch: {
    load_files() {
      if (this.load_files.length > 0 && this.load_images.length > 0) {
        this.button_disabled = false;
      }
    },
    load_images() {
      if (this.load_files.length > 0 && this.load_images.length > 0) {
        this.button_disabled = false;
      }
    }
  }
});
</script>


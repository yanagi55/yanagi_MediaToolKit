<template>
  <div
    @dragenter="drag_enter()"
    @dragleave="drag_leave()"
    @dragover.prevent
    @drop.prevent="drop_file($event)"
    :class="{ enter: ddCounter > 0 }"
  >
    <p>{{ dropTitle }}</p>
    <slot></slot>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  data() {
    return {
      ddCounter: Number(0)
      // dropTitle: String("")
    };
  },
  props: {
    dropTitle: String
  },
  methods: {
    drag_enter() {
      this.ddCounter++;
    },
    drag_leave() {
      this.ddCounter--;
    },
    drop_file(event: DragEvent) {
      this.ddCounter = 0;
      if (event.dataTransfer instanceof DataTransfer) {
        const files = event.dataTransfer.files;
        const type = event.dataTransfer.files[0].type;
        const etype = type.slice(0, 5);
        // console.log(files);
        // console.log(type);
        // console.log(etype);
        const arr = files[0].name.split(".");
        const ext = files[0].name.split(".")[arr.length - 1];
        // console.log(ext);

        this.$emit("my-drop", { files, type, etype, ext });
      }
    }
  }
});
</script>

<style>
.enter {
  border: 10px dotted powderblue;
}
</style>

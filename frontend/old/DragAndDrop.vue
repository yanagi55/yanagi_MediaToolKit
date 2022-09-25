<template>
  <div
    @dragenter="drag_enter"
    @dragleave="drag_leave"
    @dragover.prevent
    @drop.prevent="drop_file"
    :class="{ enter: ddCounter > 0 }"
  >
    <p>{{ dropTitle }}</p>
    <slot></slot>
  </div>
</template>

<script lang="coffee" type="text/coffeescript">
export default
    data:() ->
        ddCounter : 0 # drag and drop
    props:
        ['dropTitle']
    methods:
      drag_enter:() ->
          this.ddCounter++
      drag_leave:() ->
          this.ddCounter--
      drop_file:() ->
          this.ddCounter = 0
          files = [...event.dataTransfer.files]
          type = [...event.dataTransfer.files][0].type
          etype= type.slice(0, 5)

          # 親にドロップされたデータを渡す
          this.$emit('my-drop', {files, type, etype})

</script>

<style>
.enter {
  border: 10px dotted powderblue;
}
</style>

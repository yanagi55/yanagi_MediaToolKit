<template>
  <label>
    <div class="common_button">
      {{ btn_label }}
    </div>
    <form>
      <input class="hide" id="button" type="file" multiple="" />
    </form>
  </label>
</template>

<script lang="coffee" type="text/coffeescript">
export default
    data: ->
        msg: ''
    props:
        btn_label: ''

</script>

<style>
.common_button {
  margin: auto;
  padding: 6px;
  width: 80px;
  height: 20px;
  text-align: center;
  overflow: hidden;
  letter-spacing: -0.1em;
  user-select: none;
  cursor: pointer;
  border-radius: 4px;
  box-shadow: 0 4px 0 #ffcedc;
  background: white;
  color: #ff00b3;
  text-shadow: 0px 0px 20px #ff5495;
}
.hide {
  display: none;
}
</style>

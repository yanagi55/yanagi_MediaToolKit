<template>
  <div class="image_area">
    <img v-bind="$attrs" id="img" />
  </div>
</template>

<script lang="coffee" type="text/coffeescript">
export default
    props:
        data:() ->
            src: ''

    # data:() ->
    #     img_src : ''
    #     img_src_tmp : ''
    # props:
        # data:() ->
            # this.img_src: ''
</script>

<style scoped>
.image_area {
  margin: auto;
  width: 300px;
  height: 300px;

  border: 3px gray solid;
}
#img {
  width: auto;
  height: auto;
  max-width: 100%;
  max-height: 100%;
}
/* 
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
} */
/* .hide {
  display: none;
} */
</style>

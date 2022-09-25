<template>
  <!-- <CommonButton btn_label="LOAD" /> -->
  <div
    @dragenter="drag_enter"
    @dragleave="drag_leave"
    @dragover.prevent
    @drop.prevent="drop_file"
    :class="{ enter: ddCounter > 0 }"
  >
    <v-file-input
      v-model="files"
      counter
      label="File input"
      multiple
      accept="image/png, image/jpeg, image/bmp"
      placeholder="Select or drop files here"
      prepend-icon="mdi-camera"
      :show-size="1000"
      @change="send_data"
      type="file"
    >
      <template v-slot:selection="{ index, text }">
        <v-chip v-if="index < 2" label small>
          {{ text }}
        </v-chip>
        <span
          v-else-if="index === 2"
          class="text-overline grey--text text--darken-3 mx-2"
        >
          +{{ files.length - 2 }} File(s)
        </span>
      </template>
    </v-file-input>
    <!-- <v-btn
      :loading="loading"
      :disabled="loading"
      color="blue-grey"
      class="ma-2 white--text"
      @click="(loader = 'loading'), SendData()"
    >
      UPLOAD
      <v-icon right dark> mdi-file-replace </v-icon>
    </v-btn> -->
    <!-- 複数ファイル表示 -->
    <v-row>
      <v-col v-for="item in items" :key="item.name" cols="auto">
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
  </div>
</template>

<script lang="coffee" type="text/coffeescript">
import axios from 'axios'
# import CommonButton from '../components/CommonButton.vue'
export default
    # name: 'Home'
    # components: { CommonButton }
    data:() ->
        files: [] # input selected
        items: [] # total
        ddCounter : 0 # drag and drop

        overlay:false
        zIndex:0
        
    methods:
      send_data:(event) ->
          # this.PreviewImage()
          for data, index in this.files
              file = this.files[index]
              reader = new FileReader()
              reader.onload = ( (event) =>
                params = new FormData()
                params.append('image', event.target.result)
                params.append('fileName', file.name)
                axios
                .post('/api/post_image', params)
                .then(
                  (response) => ( 
                    this.items.push(response.data)
                    )
                )
              )
              reader.readAsDataURL(file)
              # ローカルプレビュー
              # this.img_src[index] = URL.createObjectURL(this.files[index])
      
      drag_enter:() ->
          this.ddCounter++
      drag_leave:() ->
          this.ddCounter--
      drop_file:() ->
          this.files = [...event.dataTransfer.files]
          this.send_data()
          this.ddCounter = 0
        
      # PreviewImage:() ->
        # this.filename = this.files[0].name
        # for data, index in this.files # n=ファイル情報 indexはindex
        #     this.img_src[index] = URL.createObjectURL(this.files[index])

    # watch:
    #   loading:() ->
    #     l = this.loader
    #     this[l] = !this[l]
    #     setTimeout( ( ()=>(this[l]=false) ), 1000)
    #     this.loader = null
</script>

<style>
.enter {
  border: 10px dotted powderblue;
}
</style>
<template>
  <div>
    <DragAndDrop
      dropTitle="Drop Image Files Here"
      @my-drop="
        if ($event['etype'] == 'image')
          load_files.push.apply(load_files, $event['files']);
        s3ImageUploader();
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
      <v-col v-for="item in image_items" :key="item.name" cols="auto">
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
      GET IMAGE_URI FROM RDB
      <v-icon right dark> mdi-file-replace </v-icon>
    </v-btn>
  </div>
</template>

<script lang="coffee" type="text/coffeescript">
import axios from 'axios'
import DragAndDrop from '@/components/DragAndDrop.vue'
export default
    components: { DragAndDrop }
    data:() ->
        load_files: [] # input selected
        # load_images: [] # loaded image binary
        image_items: []
        # image_preview: '' # <v-img src>, created Object
        # button_progress: false
        # button_disabled: true
    methods:
      GetUriList:() ->
          axios
            .get '/api/rdb_image_uri'
            .then (response) =>
                # console.log(response.data)
                n_response = JSON.parse([response.data])
                this.image_items.push.apply(this.image_items, n_response.img_list)
            .catch (error) =>
                console.log('error')

      s3ImageUploader:() ->
          for file, index in this.load_files
              this.GetSignedRequest(file)
      GetSignedRequest:(file) ->
          axios
            .get '/api/sign_s3?file_name='+file.name+'&file_type='+file.type
            .then (response) =>
                n_response = JSON.parse(response.data)
                this.UpLoadFile(file, n_response.data, n_response.url)
      UpLoadFile:(file, s3Data, url) ->
          postData = new FormData()
          for key of s3Data.fields
              postData.append(key, s3Data.fields[key])
          postData.append('file', file)
          axios
            .post s3Data.url, postData
            .then (response) =>
              console.log('posted')
              this.image_items.length=0
              this.GetUriList()
              # this.image_items.push(encodeURI(url))
              # console.log(encodeURI(url))
              this.load_files.length=0
            .catch (response) =>
              console.log('error')
          


      # ImageUploader:() -> # herokuのFastAPIにバイナリを送る
      #     for data, index in this.load_files
      #       form = new FormData()
      #       form.append('image', data)

      #       axios
      #         .post '/api/image_upload/', form, { responseType: 'blob' }
      #         .then (response) =>
      #             console.log('done! image pushed to fastapi.')
      #         .catch (error) =>
      #             alert('Error occurred in backend.')

          # clear
          # this.load_files.length = 0


      # GetImageFromS3:() ->
      #     this.GetSignedRequest(this.load_files[0])
      #     return





      MultiReplaceAudioCover:() ->
          for data, index in this.load_files
              form = new FormData()
              form.append('audio', data)
              form.append('image', this.load_images[0])
              form.append('token', 'tokentest')

              this.button_progress = true
              axios
                .post '/api/embed_image_on_mp3/', form, { responseType: 'blob' }
                .then (response) =>
                    console.log('Complete! MP3 returned.')
                    blob = new Blob([response.data])
                    link = document.createElement('a')
                    link.href = window.URL.createObjectURL(blob)
                    download_name = response.headers['content-disposition']
                      .split("filename*=utf-8''")[1]
                    link.download = decodeURI(download_name)
                    link.click()
                .catch (error) =>
                    alert('Error occurred in backend.')
                .finally () =>
                    this.button_progress = false # ローディング進捗のリセット
      
      ResetImage:() ->
          this.image_preview = URL.revokeObjectURL(this.load_images[0])
      LoadImageCover:(event) ->
          for data, index in this.load_images
              this.image_preview = URL.createObjectURL(data)
    # watch:
    #     load_files: (e) ->
    #       if ( this.load_files.length > 0 && this.load_images.length > 0 )
    #         this.button_disabled = false
    #     load_images: (e) ->
    #       if ( this.load_files.length > 0 && this.load_images.length > 0 )
    #         this.button_disabled = false
    #     # its not clean, but works.
</script>

<style scoped>
.hide {
  display: none;
}
</style>
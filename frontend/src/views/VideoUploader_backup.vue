<template>
  <v-app>
    <v-container>
      <v-flex xs12 sm6 offset-sm3>
        <v-stepper v-model="step_now" alt-labels outlined>
          <v-stepper-header class="elevation-0">
            <v-stepper-step
              :complete="step_now > 1"
              step="1"
              editable
              edit-icon="$complete"
            >
              ファイルを選択
            </v-stepper-step>
            <v-divider></v-divider>
            <v-stepper-step
              :complete="step_now > 2"
              step="2"
              editable
              edit-icon="$complete"
            >
              動画情報を入力
            </v-stepper-step>
            <v-divider></v-divider>
            <v-stepper-step
              :complete="step_now > 3"
              step="3"
              editable
              edit-icon="$complete"
            >
              入力内容の確認
            </v-stepper-step>
          </v-stepper-header>

          <v-divider></v-divider>

          <v-stepper-items>
            <v-stepper-content step="1">
              <small
                >※.tsファイルとstream.m3u8ファイルをすべて指定してください</small
              >
              <!-- <v-card class="mb-1" flat> -->
              <v-file-input
                v-model="load_files"
                counter
                label="Video Files"
                multiple
                :show-size="1000"
                type="file"
              >
              </v-file-input>
              <!-- </v-card> -->
              <div class="text-center mb-3">
                <v-btn color="primary" outlined @click="step_now = 2"
                  >NEXT</v-btn
                >
              </div>
              <!-- <v-spacer class="mb-3"></v-spacer> -->
              <!-- <v-btn text>Cancel</v-btn> -->
            </v-stepper-content>
            <v-stepper-content step="2">
              <small>※保存場所: {volume}/storage/video/public/{title}/</small>
              <!-- <v-card class="mb-12" height="200px"> -->
              <v-text-field
                label="タイトル(サーバー側の保存名)"
                v-model="videoTitle"
                required
              >
              </v-text-field>
              <v-text-field
                label="タイトル(サーバー側の保存名)"
                v-model="videoTitle"
                disabled
              >
              </v-text-field>
              <!-- </v-card> -->
              <div class="text-center mb-3">
                <v-btn outlined @click="step_now = 1" class="mr-1">BACK</v-btn>
                <v-btn outlined color="primary" @click="step_now = 3"
                  >NEXT</v-btn
                >
              </div>
              <!-- <v-spacer class="mb-3"></v-spacer> -->
            </v-stepper-content>

            <v-stepper-content step="3">
              <v-card>
                <v-card-text v-show="videoTitle">
                  <div v-show="videoTitle">
                    {{ videoTitle }}
                  </div>
                  <div v-show="load_files">
                    {{ load_files.length }} 個のファイル
                  </div>
                  <template v-for="item in load_files">
                    {{ item.name }}
                  </template>
                  <div class="text-center mt-5">
                    <v-btn @click="PostVideo()" disabled outlined>
                      アップロード
                      <v-icon right>mdi-upload</v-icon>
                    </v-btn>
                  </div>
                </v-card-text>
              </v-card>
            </v-stepper-content>
          </v-stepper-items>
        </v-stepper>
      </v-flex>

      <!-- old -->
      <!-- <v-flex xs12 sm6 offset-sm3>
        <v-card>
          <v-card-text>
            １．アップロードするファイル名を指定する
            <div class="ma-2">
              ※保存場所: {volume}/storage/video/public/{videoTitle}/
            </div>
            <v-text-field
              label="タイトル(サーバー側の保存名)"
              v-model="videoTitle"
              required
            >
            </v-text-field>
          </v-card-text>
        </v-card>
        <div class="mt-5"></div>
        <v-card>
          <v-card-text>
            ２．ファイル指定
            <div class="ma-2">
              ※.tsファイルとstream.m3u8ファイルを指定する
            </div>
            <v-file-input
              v-model="load_files"
              counter
              label="Video Files"
              multiple
              :show-size="1000"
              type="file"
            >
            </v-file-input>
          </v-card-text>
        </v-card>
        <div class="text-center mt-5">
          <v-btn @click="PostVideo()">
            アップロード
            <v-icon right>mdi-upload</v-icon>
          </v-btn>
        </div>
      </v-flex> -->
    </v-container>
  </v-app>
</template>

<script lang="ts">
import axios from "axios";
import Vue from "vue";
export default Vue.extend({
  data: () => {
    return {
      step_now: Number(1),
      videoTitle: String(),
      load_files: []
    };
  },
  methods: {
    test() {
      console.log("test");
    },
    PostVideo() {
      // 一度のPOSTで全部送るか、断片ごとにPOSTするか迷うが、
      // まずは断片ごとにPOSTする。
      // 作ったことがあるのと、負荷分散を望めるため。
      for (const data of this.load_files) {
        const form = new FormData();
        form.append("title", this.videoTitle);
        form.append("video", data);

        axios
          .post("/api/video_upload", form)
          .then(response => {
            console.log(response.data);
          })
          .catch(error => {
            console.log(error.response);
          })
          .finally(() => {
            // console.log("finally");
          });
      }
    }
    // videoSetup() {
    //   const video = document.getElementById("video") as HTMLMediaElement;
    //   const videoUrl = "/storage/video/output/stream.m3u8";
    //   if (video != null && Hls.isSupported()) {
    //     this.hls = new Hls();
    //     this.hls.loadSource(videoUrl);
    //     this.hls.attachMedia(video);
    //     // video.play();
    //   } else if (video.canPlayType("application/vnd.apple.mpegurl")) {
    //     video.src = videoUrl;
    //     video.addEventListener("canplay", () => {
    //       // video.play();
    //     });
    //   }
    // }
  }
  // mounted: function() {
  //   this.videoSetup();
  // }
});
</script>

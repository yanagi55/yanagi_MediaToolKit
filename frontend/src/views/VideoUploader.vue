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
            <DragAndDrop
              @my-drop="
                if ($event['ext'] === 'ts' || $event['ext'] === 'm3u8')
                  load_files.push.apply(load_files, $event['files']);
              "
            >
              <v-stepper-content step="1">
                <small
                  >※.tsファイルとstream.m3u8ファイルを、すべて指定してください<br />※重複チェックは未実装です。</small
                >
                <!-- <v-card class="mb-1" flat> -->
                <v-form ref="file_form">
                  <v-file-input
                    v-model="load_files"
                    counter
                    label="Video Files"
                    multiple
                    prepend-icon="mdi-movie-open"
                    :show-size="1000"
                    type="file"
                  >
                    <template v-slot:selection="{ index, text }">
                      <v-chip v-if="index < 10" label small>
                        {{ text }}
                      </v-chip>
                      <span
                        v-else-if="index === 10"
                        class="text-overline grey--text text--darken-3 mx-2"
                      >
                        +{{ load_files.length - 10 }} File(s)
                      </span>
                    </template>
                  </v-file-input>
                </v-form>
                <!-- </v-card> -->
                <div class="text-center mb-3">
                  <v-btn
                    color="primary"
                    outlined
                    @click="step_now = 2"
                    :disabled="load_files.length === 0"
                    >NEXT</v-btn
                  >
                  <div class="text-center mt-1">
                    <v-btn @click="ReadZip()"
                      >ZIPを展開するボタン(dev)
                      <v-icon right>mdi-folder-zip</v-icon></v-btn
                    >
                  </div>
                </div>
                <!-- <v-btn text>Cancel</v-btn> -->
              </v-stepper-content>
            </DragAndDrop>
            <v-stepper-content step="2">
              <small
                >※保存場所:
                {volume}/storage/video/public/{username}-{title}/</small
              >
              <!-- <small>※保存場所: {volume}/storage/video/public/{title}/</small> -->
              <!-- <v-card class="mb-12" height="200px"> -->
              <v-text-field label="タイトル" v-model="videoTitle" required>
              </v-text-field>
              <v-text-field
                label="dist:サーバーでのディレクトリ名を指定(dev)"
                v-model="videoDist"
                required
              >
              </v-text-field>

              <DragAndDrop
                @my-drop="
                  if ($event['ext'] === 'jpg' || $event['ext'] === 'png')
                    load_image.push.apply(load_image, $event['files']);
                "
              >
                <v-form ref="file_form">
                  <v-file-input
                    v-model="load_image"
                    counter
                    label="Thumb Image"
                    multiple
                    prepend-icon="mdi-file-image"
                    :show-size="1000"
                    type="file"
                    accept="image/jpeg, image/png"
                  >
                  </v-file-input>
                </v-form>
              </DragAndDrop>

              <!-- </v-card> -->
              <div class="text-center mb-3">
                <v-btn outlined @click="step_now = 1" class="mr-1">BACK</v-btn>
                <v-btn outlined color="primary" @click="step_now = 3"
                  >NEXT</v-btn
                >
              </div>
            </v-stepper-content>

            <v-stepper-content step="3">
              <div class="text-center mb-2">
                以下の内容で送信します<br />
                サーバーへの負荷にご注意ください
              </div>
              <v-card outlined>
                <v-card-text>
                  <div>動画タイトル: {{ videoTitle }}</div>
                  <div>ファイル数:{{ load_files.length }}</div>
                  <div v-if="load_image[0]">
                    サムネイル:{{ load_image[0].name }}
                  </div>
                  <!-- <div>サムネイル:{{ load_image[0].name }}</div> -->
                  <div>ファイル名:</div>
                  <template v-for="item in load_files">
                    {{ item.name }}
                  </template>
                </v-card-text>
              </v-card>
              <div class="text-center mt-5 mb-3">
                <v-btn @click="PostVideo()" outlined :disabled="processing">
                  アップロード
                  <v-icon right>mdi-upload</v-icon>
                </v-btn>
              </div>
              <v-progress-linear
                :value="totalUploadPercentage"
                height="25"
                :color="progress_color"
              >
                TOTAL : {{ Math.ceil(totalUploadPercentage) }} %
                {{ uploadSpeed }} MB/s
              </v-progress-linear>
              <div>
                loaded: {{ Math.ceil(loadSize / 1024 / 1024) }} MB<br />
                total: {{ Math.ceil(totalSize / 1024 / 1024) }} MB<br />
              </div>
              <template v-for="(item, index) in load_files">
                <div :key="index">
                  {{ item.name }} - {{ uploadPercentages[index] }} %
                  <v-progress-linear
                    v-model="uploadPercentages[index]"
                  ></v-progress-linear>
                </div>
              </template>
            </v-stepper-content>
          </v-stepper-items>
        </v-stepper>
      </v-flex>
    </v-container>
  </v-app>
</template>

<script lang="ts">
import axios from "axios";
import Vue from "vue";
// import store from "@/store";
import DragAndDrop from "@/components/DragAndDrop.vue";
import JSZip from "jszip";
export default Vue.extend({
  components: { DragAndDrop },
  data: () => {
    return {
      step_now: Number(1),
      videoTitle: String(),
      videoDist: String(),
      load_files: [] as File[],
      load_image: [] as File[],
      init_upload_progress: Boolean(false),

      totalUploadPercentage: 0,
      uploadPercentages: [] as number[],
      totalSizes: [] as number[],
      totalSize: 0,
      loadSizes: [] as number[],
      loadSize: 0,
      uploadSpeed: 0
    };
  },
  computed: {
    processing() {
      if (this.init_upload_progress === false) {
        return false;
      } else if (this.totalSize === 0 || this.totalSize !== this.loadSize) {
        return true;
      } else {
        return false;
      }
    },
    progress_color() {
      if (this.totalSize === 0 || this.totalSize !== this.loadSize) {
        return "primary";
      } else {
        return "success";
      }
    }
  },
  methods: {
    ReadZip() {
      // forだが現状1つのZipファイルのみ想定
      for (const zipfile of this.load_files) {
        // 読み込んだZipをスロットからドロップする
        this.load_files.length = 0;
        JSZip.loadAsync(zipfile).then(data => {
          for (const filename in data.files) {
            data.files[filename].async("blob").then(filedata => {
              const fileobj = new File([filedata], filename);
              this.load_files.push(fileobj);
            });
          }
        });
      }
    },
    PostVideo() {
      this.init_upload_progress = true;
      const timestamp_for_speed = performance.now();
      // 断片ごとにPOSTする。
      for (const index in this.load_files) {
        const form = new FormData();
        form.append("title", this.videoTitle);
        // form.append("username", store.getters.userName);
        // ★開発中、ユーザー名が取得出来ないことがあるので、プレーンテキスト指定
        form.append("username", "exampleUserDev");
        form.append("video", this.load_files[index]);
        form.append("thumb", this.load_image[0]);
        form.append("dist", this.videoDist);
        // form.append("dir_id", dir_id)

        axios
          .post("/api/video_upload", form, {
            onUploadProgress: ProgressEvent => {
              // トータル値管理へ代入
              this.totalSizes[index] = ProgressEvent.total; //冗長だがaxios側のサイズが欲しい
              this.loadSizes[index] = ProgressEvent.loaded;
              this.totalSize = this.totalSizes.reduce((a, x) => (a += x), 0);
              this.loadSize = this.loadSizes.reduce((a, x) => (a += x), 0);

              // パーセント算出し代入 各要素とトータル
              this.uploadPercentages[index] = Math.round(
                (ProgressEvent.loaded / ProgressEvent.total) * 100
              );
              this.totalUploadPercentage =
                (this.loadSize * 100) / this.totalSize;

              // 速度計算
              const time_from_stamp = performance.now() - timestamp_for_speed;
              this.uploadSpeed =
                Math.round((this.loadSize / time_from_stamp / 1024) * 10) / 10;
            }
          })
          .then(response => {
            console.log(response.data);
          })
          .catch(error => {
            console.log(error.response);
          });
      }
    }
  }
});
</script>

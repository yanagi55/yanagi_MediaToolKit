<template>
  <div>
    <!-- <v-btn @click="getVideoList()">手動でリスト更新</v-btn> -->

    <v-dialog v-model="playing" @click:outside="videoDetach()">
      <video
        controls
        autoplay
        width="auto"
        height="auto"
        id="video"
        @wheel="videoSeekFromWheel($event)"
        @wheel.prevent
      ></video>
      <div>再生中 : {{ video_playing.title }}</div>
      <div @wheel="videoVolumeSeekFromWheel($event)" @wheel.prevent>
        ボリューム変更
      </div>
    </v-dialog>

    <v-container>
      <v-flex offset-sm1>
        <v-row justify="start">
          <v-col v-for="item in video_list" :key="item.title" cols="auto">
            <v-card
              width="200"
              height="200"
              ripple
              flat
              tile
              @click="videoSetup(item.dist, item.title)"
            >
              <v-img
                :src="'/storage/video/public/' + item.dist + '/thumb.webp'"
                max-width="100%"
                max-height="100%"
                :aspect-ratio="16 / 9"
                class="align-end text-right white--text pa-1"
              >
                <span
                  class="black caption font-weight-medium"
                  style="padding: 1px 3px;"
                >
                  {{ durationFormat(item.duration) }}
                </span>
              </v-img>
              <v-list three-line class="pa-0">
                <v-list-item class="px-0">
                  <v-list-item-avatar size="40" class="mr-2">
                    <v-img
                      :src="'/storage/user_icon/icon_exampleUser.jpg'"
                    ></v-img>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-subtitle class="text--primary">
                      {{ item.title }}
                    </v-list-item-subtitle>
                    <v-list-item-subtitle class="text--disabled">
                      {{ item.username }}
                      <v-icon small disabled style="margin-top:-2px"
                        >mdi-check-circle</v-icon
                      >
                    </v-list-item-subtitle>
                    <v-list-item-subtitle class="text--disabled caption">
                      {{ item.playcount }} 回視聴 ･
                      {{ timeSince(item.datetime) }}
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-card>
          </v-col>
        </v-row>
      </v-flex>
    </v-container>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Hls from "hls.js";
import axios from "axios";
export default Vue.extend({
  data: () => {
    return {
      hls: new Hls(),
      playing: Boolean(false),
      video_playing: {
        title: String(),
        dist: String(),
        username: String(),
        duration: Number(),
        playcount: Number(),
        datetime: Date()
      },
      // video_list: [] as string[],
      video_list: Array({
        title: String(),
        dist: String(),
        username: String(),
        duration: Number(),
        playcount: Number(),
        datetime: Date()
      })
    };
  },
  methods: {
    timeSince(datetime: string) {
      const date = new Date(datetime);
      let seconds = Math.floor((Date.now() - date.getTime()) / 1000);
      let unit = "second";
      let direction = "ago";
      if (seconds < 0) {
        seconds = -seconds;
        direction = "from now";
      }
      let value = seconds;
      if (seconds >= 31536000) {
        value = Math.floor(seconds / 31536000);
        unit = "year";
      } else if (seconds >= 2592000) {
        value = Math.floor(seconds / 2592000);
        unit = "month";
      } else if (seconds >= 604800) {
        value = Math.floor(seconds / 604800);
        unit = "week";
      } else if (seconds >= 86400) {
        value = Math.floor(seconds / 86400);
        unit = "day";
      } else if (seconds >= 3600) {
        value = Math.floor(seconds / 3600);
        unit = "hour";
      } else if (seconds >= 60) {
        value = Math.floor(seconds / 60);
        unit = "minute";
      }
      if (value != 1) unit = unit + "s";
      return value + " " + unit + " " + direction;
    },
    durationFormat(duration: number) {
      const hours = Math.floor(duration / 3600);
      const minutes = Math.floor(Math.floor(duration % 3600) / 60);
      const seconds = Math.floor(duration % 60);

      let format = "";
      if (hours > 0) {
        format += "" + hours + ":" + (minutes < 10 ? "0" : "");
      }
      format += "" + minutes + ":" + (seconds < 10 ? "0" : "");
      format += "" + seconds;
      return format;
    },
    getVideoList() {
      axios
        .get("/api/get_video_list")
        .then(response => {
          this.video_list.length = 0;
          for (const data of response.data) {
            this.video_list.push(data);
          }
        })
        .catch(response => {
          console.log(response.error);
        });
    },
    videoSetup(dist: string, title: string) {
      this.playing = true;
      this.video_playing.dist = dist;
      this.video_playing.title = title;
    },
    videoStart(dist: string) {
      const video = document.getElementById("video") as HTMLVideoElement;
      const videoUrl = "/storage/video/public/" + dist + "/stream.m3u8";
      if (video !== null && Hls.isSupported()) {
        this.hls = new Hls();
        this.hls.loadSource(videoUrl);
        this.hls.attachMedia(video);
        video.volume = 0.2;
      } else if (
        video !== null &&
        video.canPlayType("application/vnd.apple.mpegurl")
      ) {
        video.src = videoUrl;
        video.addEventListener("canplay", () => {
          // video.play();
        });
      }
    },
    videoSeekFromWheel(event: WheelEvent) {
      const video = document.getElementById("video") as HTMLVideoElement;
      video.currentTime += Math.sign(event.deltaY) * 5;
    },
    videoVolumeSeekFromWheel(event: WheelEvent) {
      const video = document.getElementById("video") as HTMLVideoElement;
      video.volume -= Math.sign(event.deltaY) * 0.05;
    },
    videoDetach() {
      this.hls.detachMedia();
    }
  },
  created() {
    this.video_list.length = 0;
  },
  updated() {
    // console.log(document.getElementById("video"));
    if (document.getElementById("video") && this.playing) {
      this.videoStart(this.video_playing.dist);
    }
  },
  mounted() {
    this.getVideoList();
  }
});
</script>

<template>
  <v-app>
    <v-container>
      <!-- <v-row align="start" justify="center"> -->
      <!-- <div class="test">aiueo</div> -->
      <!-- <v-row>
        <v-col> -->
      <v-flex xs12 sm6 offset-sm3 class="mb-n4">
        <v-textarea
          auto-grow
          clearable
          outlined
          label="テキストを入力してください"
          v-model="InputText"
          rows="1"
          @keydown.enter.ctrl.exact="PostTweet()"
        ></v-textarea
      ></v-flex>
      <v-flex xs12 sm6 offset-sm3 class="mb-4 text-right">
        <v-btn outlined @click="PostTweet()"> 投稿する</v-btn>
      </v-flex>

      <!-- </v-col> -->
      <!-- <v-col cols="3">
          <v-btn outlined @click="SendData()"> 文字数をカウント </v-btn>
        </v-col> -->
      <!-- <v-col> -->
      <!-- </v-col> -->
      <!-- </v-row> -->

      <!-- <v-row>
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
      </v-row> -->

      <!-- <v-row align="start" justify="center"> -->
      <v-flex xs12 sm6 offset-sm3>
        <v-row>
          <v-col cols="auto">
            <v-card max-width="" class="mx-auto" outlined>
              <!-- <v-toolbar dark> -->
              <!-- <v-toolbar-title>Result</v-toolbar-title> -->
              <!-- </v-toolbar> -->

              <v-list three-line>
                <template v-for="(item, index) in items">
                  <v-list-item :key="item.title">
                    <v-list-item-content>
                      <v-list-item-title style="white-space:pre-wrap;"
                        >{{ item[0] }}

                        <!-- <div style="white-space: pre-wrap;" v-text="item[0]"></div> -->
                      </v-list-item-title>
                      <!-- <div>(画像)</div> -->
                      <!-- <div>{{ item[2] }}</div> -->
                      <v-list-item-subtitle
                        >{{ item[1] }} by {{ item[2] }}</v-list-item-subtitle
                      >
                    </v-list-item-content>
                  </v-list-item>
                  <v-divider :key="index" :inset="item.inset"></v-divider>
                </template>
              </v-list>
            </v-card>
          </v-col>
        </v-row>
      </v-flex>
    </v-container>
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
import VueCookies from "vue-cookies";
import store from "../store";
import axios from "axios";
Vue.use(VueCookies);
export default Vue.extend({
  props: {},
  data() {
    return {
      InputText: String(),
      items: [String],
      CurrentNewestId: Number(1)
      // ClientToken: String()
    };
  },
  methods: {
    GetNewPost() {
      axios
        .get("/api/get_newpost", {
          responseType: "json",
          params: { current_id: this.CurrentNewestId }
        })
        .then(response => {
          const n_response = JSON.parse(response.data);
          for (const n in n_response.textlist) {
            this.items.unshift(n_response.textlist[n]);
          }
          this.InputText = "";
          this.CurrentNewestId = n_response.newest_id;
          // console.log(n_response.textlist);
          // console.log(this.CurrentNewestId);
        })
        .catch(error => alert("cant connect api server"));
    },
    // GetUriList() {
    //   axios
    //     .get("/api/get_uri_list", { responseType: "json" })
    //     .then(response => {
    //       const n_response = JSON.parse(response.data);
    //       for (const n in n_response.datalist) {
    //         this.items.unshift(n_response.datalist[n][0]);
    //       }
    //     })
    //     .catch(error => alert("cant connect api server"));
    // },
    PostTweet() {
      const data = { text: this.InputText };
      axios
        .post("/api/post_tweet", data)
        .then(response => {
          // this.items.unshift(response.data);
          this.GetNewPost();
        })
        .catch(error => alert("cant connect api server"));
    }
  },
  created: function() {
    //起動時に動く。window:onloadだとthis参照出来ない・タイミング早すぎ
    // this.GetUriList();
    this.GetNewPost();
  }
});
</script>

<style lang="scss">
.v-textarea {
  textarea {
    line-height: 20px !important;
  }
}
/* .enter {
  border: 10px dotted powderblue;
} */
/* .v-textarea textarea {
  line-height: 150% !important;
} */
</style>



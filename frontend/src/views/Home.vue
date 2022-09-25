<template>
  <v-app>
    <v-container>
      <v-flex xs12 sm6 offset-sm3 class="">
        <v-hover v-slot="{ hover=false }">
          <v-card flat>
            <v-overlay
              absolute
              :value="hover && $store.getters.userName === ''"
              class="text-center"
              z-index="4"
            >
              <div class="mb-2 mt-1">投稿にはログインが必要です</div>
              <v-btn color="grey" @click="$router.push({ path: '/account' })">
                ログイン
              </v-btn>
            </v-overlay>
            <v-row>
              <v-col cols="2">
                <div class="ml-1">
                  <!-- <v-badge overlap bordered color="blue" content="0"> -->
                  <!-- <v-badge overlap bordered color="blue" icon="mdi-lock"> -->
                  <v-avatar rounded size="55">
                    <v-img :src="CurrentUserIcon"></v-img>
                  </v-avatar>
                  <!-- </v-badge> -->
                </div>
                <!-- {{ $store.getters.userName }} -->
              </v-col>
              <v-col>
                <v-textarea
                  :disabled="$store.getters.userName === ''"
                  auto-grow
                  clearable
                  outlined
                  label="テキストを入力してください"
                  v-model="InputText"
                  rows="1"
                  @keydown.enter.ctrl.exact="PostTweet()"
                >
                </v-textarea>
              </v-col>
            </v-row>
            <v-row no-gutters class="mb-2 mt-n8" align="center">
              <v-col
                class="ml-1 text--secondary"
                v-if="$store.getters.userName !== ''"
                cols="auto"
                >ログイン中 : {{ $store.getters.userName }}</v-col
              >
              <v-col class="text-right">
                <v-btn
                  outlined
                  @click="PostTweet()"
                  :disabled="$store.getters.userName === ''"
                >
                  投稿する</v-btn
                >
              </v-col>
            </v-row>
          </v-card>
        </v-hover>
      </v-flex>

      <v-flex xs12 sm6 offset-sm3>
        <v-row>
          <v-col cols="auto">
            <v-card max-width="" class="mx-auto" outlined>
              <v-list three-line>
                <template v-for="(item, index) in items">
                  <!-- <v-subheader :key="item" inset>a</v-subheader> -->
                  <v-list-item :key="item.postDate">
                    <v-list-item-avatar :key="index" size="50">
                      <img :src="item.avatar" />
                    </v-list-item-avatar>
                    <v-list-item-content>
                      <v-list-item-title
                        style="white-space:pre-wrap;"
                        class="text--primary"
                        >{{ item.textBody }}
                        <!-- <div style="white-space: pre-wrap;" v-text="item[0]"></div> -->
                      </v-list-item-title>
                      <!-- <div>(画像)</div> -->
                      <!-- <div>{{ item[2] }}</div> -->
                      <v-list-item-subtitle
                        >{{ item.postDate }} by
                        {{ item.userName }}</v-list-item-subtitle
                      >
                    </v-list-item-content>
                  </v-list-item>
                  <v-divider
                    :key="index"
                    inset
                    v-if="index !== items.length - 1"
                  ></v-divider>
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
// import store from "../store";
// import PostForm from "@/components/PostForm.vue";
import axios from "axios";
import store from "@/store";
Vue.use(VueCookies);
export default Vue.extend({
  // components: { PostForm },
  props: {},
  data() {
    return {
      InputText: String(),
      CurrentNewestId: Number(),
      items: Array({
        textBody: String("Default Text Body"),
        postDate: String("2021-11-04"),
        userName: String("YF"),
        avatar: String("/storage/user_icon/icon_.jpg")
      })
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
          // console.log(this.items);
          const n_response = JSON.parse(response.data);
          for (const data of n_response.textlist) {
            this.items.unshift({
              textBody: data[0],
              postDate: data[1],
              userName: data[2],
              avatar: "/storage/user_icon/icon_" + data[2] + ".jpg"
            });
          }
          this.InputText = "";
          this.CurrentNewestId = n_response.newest_id;
        })
        .catch(error => {
          alert(error);
          alert("cant connect api server");
        });
    },

    PostTweet() {
      const data = { text: this.InputText };
      axios
        .post("/api/post_tweet", data)
        .then(() => {
          // this.items.unshift(response.data);
          this.GetNewPost();
        })
        .catch(error => {
          alert(error.response);
          alert("cant connect api server");
        });
    }
  },
  computed: {
    CurrentUserIcon() {
      return "/storage/user_icon/icon_" + store.getters.userName + ".jpg";
    }
  },
  mounted: function() {
    if (Vue.$cookies.isKey("yf_token")) {
      store.dispatch("confirm");
    }
  },
  created: function() {
    //起動時に動く。window:onloadだとthis参照出来ない・タイミング早すぎ
    // this.GetUriList();
    this.GetNewPost();
  }
});
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
</script>

<style lang="scss">
// めちゃめちゃ強引だけど、ベース文字のオーバーライド。
// 特にdarkのPrimaryが白100%(#FFFFFF)で指定してて眩しい。
// ※lightはrgba(0, 0, 0, 0.87)で指定されてるので、先人の手抜きか
// なおVueが準拠と銘打っているmaterial.ioではDarkでもWhiteは87%。

.theme--light.v-application .v-list-item__title.text--primary {
  color: rgba(0, 0, 0, 0.87) !important;
}
.theme--dark.v-application .v-list-item__title.text--primary {
  color: rgba(230, 230, 230, 0.87) !important;
}

// これは機能しない
// .text--primary {
//   color: red !important;
// }

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



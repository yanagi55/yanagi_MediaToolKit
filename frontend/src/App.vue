<template>
  <v-app>
    <!-- 上：ヘッダー -->
    <v-app-bar app flat dense>
      <!-- アイコン表示のレスポンシブが、途切れてる。とりあえず常に表示 -->
      <!-- <v-app-bar-nav-icon @click="drawer = true"></v-app-bar-nav-icon> -->
      <!-- <v-toolbar-title>CoverArtReplacer</v-toolbar-title> -->
      <v-spacer></v-spacer>
      <v-btn icon to="/" tile>
        <v-icon>mdi-home</v-icon>
      </v-btn>
      <v-divider vertical inset></v-divider>
      <v-btn icon tile :disabled="!CheckAuth">
        <v-icon>mdi-text</v-icon>
      </v-btn>
      <v-btn icon tile to="/photo-uploader" :disabled="!CheckAuth">
        <v-icon>mdi-image</v-icon>
      </v-btn>
      <v-btn icon tile to="/cover-art-replacer" :disabled="!CheckAuth">
        <v-icon>mdi-music</v-icon>
      </v-btn>
      <v-btn icon tile to="/video-player">
        <v-icon>mdi-play-box</v-icon>
      </v-btn>

      <!-- <v-btn icon tile to="/video-uploader" :disabled="!CheckAuth"> -->
      <!-- dev -->
      <v-btn icon tile to="/video-uploader">
        <v-icon>mdi-file-upload</v-icon>
      </v-btn>
      <v-divider vertical inset></v-divider>
      <!-- <v-btn icon tile to="/account">
        <v-icon>mdi-account</v-icon>
      </v-btn> -->
      <v-menu
        :close-on-content-click="false"
        offset-y
        content-class="elevation-0"
        open-on-hover
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon tile v-bind="attrs" v-on="on">
            <v-icon>mdi-account</v-icon>
          </v-btn>
        </template>
        <v-list outlined>
          <v-list-item>
            <v-list-item-avatar size="40">
              <v-img :src="CurrentUserIcon"></v-img>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title>
                {{ GetCurrentUserName }}
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ GetCurrentUserName }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-divider></v-divider>
          <v-list-item @click="$vuetify.theme.dark = !$vuetify.theme.dark">
            <v-list-item-subtitle>ダークテーマ</v-list-item-subtitle>
            <v-switch
              class="mt-0 ml-3 mr-0"
              hide-details="auto"
              inset
              dense
              flat
              v-model="$vuetify.theme.dark"
              readonly
            ></v-switch>
          </v-list-item>
          <v-divider></v-divider>
          <v-list-item to="/account">
            <v-list-item-title>設定 (旧ログイン)</v-list-item-title>
          </v-list-item>
          <v-list-item @click="Logout()" :disabled="!CheckAuth">
            <v-list-item-title>ログアウト</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-spacer></v-spacer>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <!-- ★ここはrouter-view側で内容を書いている。ルートはHome.vue -->
        <router-view />
      </v-container>
    </v-main>
    <!-- <v-btn @click="SendData"><p>a</p></v-btn> -->
    <!-- <v-footer app>
      <p>v-footer</p>
    </v-footer> -->
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
import store from "./store";
export default Vue.extend({
  props: {},
  data() {
    return {
      userName: String()
    };
  },
  methods: {
    Logout() {
      store.dispatch("logout");
    }
  },
  computed: {
    CheckLogin() {
      return store.getters.isLogin;
    },
    CheckAuth() {
      return store.getters.isAuth;
    },
    GetCurrentUserName() {
      return store.getters.userName;
    },
    CurrentUserIcon() {
      return "/storage/user_icon/icon_" + store.getters.userName + ".jpg";
    }
  }
});
</script>

<style>
/* ダークテーマの設定を上書きする */
.theme--dark.v-card {
  /* 元色は#121212 */
  background-color: inherit;
}
.theme--dark.v-list {
  /* ここでinheritを使うと透過が入ってしまうため直に指定 */
  background: #121212;
}
/* .text--primary {
  color: red !important;
} */
/* #app { */
/* color: #2c3e50; */
/* font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale; */
/* text-align: center; */
/* margin-top: 60px; */
/* } */
</style>

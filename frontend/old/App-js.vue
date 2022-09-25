<template>
  <v-app>
    <!-- ヘッダー -->
    <v-app-bar app flat>
      <!-- <v-app-bar-nav-icon @click="drawer = true"></v-app-bar-nav-icon> -->
      <v-toolbar-title>CoverArtReplacer</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon>mdi-heart</v-icon>
      </v-btn>
    </v-app-bar>

    <!-- ナビゲーション -->
    <v-navigation-drawer v-model="drawer" app>
      <v-list nav dense>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="text-h6"> yf.apps </v-list-item-title>
            <v-list-item-subtitle> my own test </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-list nav dense>
        <v-list-item-group v-model="group">
          <v-list-item to="/" replace>
            <v-list-item-icon>
              <v-icon>mdi-home</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Home(CAR)</v-list-item-title>
          </v-list-item>
          <v-list-item to="/account" replace>
            <v-list-item-icon>
              <v-icon>mdi-account</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Account</v-list-item-title>
          </v-list-item>
          <v-list-item to="/about" replace>
            <v-list-item-icon>
              <v-icon>mdi-information</v-icon>
            </v-list-item-icon>
            <v-list-item-title>About</v-list-item-title>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-container fluid>
        <!-- <CommonButton btn_label="LOAD" @change="read_file" />
        <p>input: {{ file_name_A }}</p>
        <ImageArea :src="img_src" /> -->

        <!-- ★ここはrouter-view側で内容を書いている。ルートはHome.vue -->
        <router-view></router-view>
      </v-container>
    </v-main>
    <!-- <v-btn @click="SendData"><p>a</p></v-btn> -->
    <v-footer app>
      <p>v-footer</p>
    </v-footer>
  </v-app>
</template>

<script>
import Vue from "vue";
import CommonButton from "./components/CommonButton.vue";
import HelloWorld from "./components/HelloWorld.vue";
import ImageArea from "./components/ImageArea.vue";
import axios from "axios";
export default {
  name: "App",
  components: { CommonButton, HelloWorld, ImageArea },
  data: () => ({
    InputText: "",
    TextLength: null,
    items: [],
    file_name_A: "No files selected.",
    img_src: "",
    drawer: null,
    group: null,
  }),
  methods: {
    read_file: (event) => ({
      this: (this.file_name_A = event.target.files[0].name),
    }),
  },
};
</script>>

    data:() ->
        InputText: ''
        TextLength: null
        items: []
        file_name_A : 'No files selected.'
        img_src : ''

        drawer: null
        group: null
    methods:
        read_file:(event) ->
            this.file_name_A = event.target.files[0].name
            this.img_src = URL.createObjectURL(event.target.files[0])
        SendData:() ->
            this.file_name_A = 'test'
            data = text: this.InputText
            axios
            .post('/api/post', data)
            .then((response) =>
                this.items.push(response.data)
                )
            .catch((err) =>
                alert('cant connect api server')
                err = null
                )

<style>
.greeting {
  color: gray;
  font-size: 30px;
}
#app {
  /* font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale; */
  /* text-align: center; */
  color: #2c3e50;
  /* margin-top: 60px; */
}
</style>

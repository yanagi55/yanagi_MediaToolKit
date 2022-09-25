<template>
  <v-container>
    <!-- <v-layout row v-if="error">
      <v-flex xs12 sm6 offset-sm3>
        <app-alert @dismissed="onDismissed" :text="error.message"></app-alert>
      </v-flex>
    </v-layout> -->
    <v-flex xs12 sm6 offset-sm3>
      <v-card v-if="$store.getters.userName" class="text-center">
        <v-card-text>
          ログイン中 <br />
          {{ $store.getters.userName }}
        </v-card-text>
        <v-container>
          <v-btn @click="Logout()" class="mb-2">
            ログアウト
          </v-btn>
        </v-container>
      </v-card>
      <!-- <v-card> -->
      <v-card v-if="!$store.getters.userName">
        <v-card-text>
          <v-container>
            <!-- <div class="text-center mb-5">
              現在、{{ $store.getters.userName }} として権限があります。
            </div> -->
            <!-- <form @submit.prevent="onSignin"> -->
            <form @submit.prevent="Login()">
              <v-flex xs12>
                <v-text-field
                  name="email"
                  label="E-mail"
                  id="email"
                  v-model="email"
                  type="email"
                  required
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  name="password"
                  label="Password"
                  id="password"
                  v-model="password"
                  type="password"
                  required
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <div class="text-center">
                  <v-btn type="submit" :loading="loading">ログイン</v-btn>
                </div>
              </v-flex>
              <!-- <v-flex xs12>
                <v-btn type="submit" :loading="loading">Sign up</v-btn>
              </v-flex> -->
            </form>
          </v-container>
        </v-card-text>
      </v-card>

      <div class="text-center mt-10 body-2" v-if="!$store.getters.userName">
        <div>アカウントを持っていない場合、新規登録できます</div>
        <v-btn class="mt-2" to="/account-register">サインアップ</v-btn>
      </div>
      <!-- <v-text-field
        name="token"
        label="token"
        id="token"
        v-model="input_token"
        type="token"
        required
      ></v-text-field> -->
      <!-- <v-container>
        <v-btn @click="CheckAuth()">
          トークン可否・ログイン状態をチェックする
        </v-btn>
      </v-container> -->
      <!-- <v-container>
        <v-btn @click="Logout()">
          ログアウト(セッション処理とCookie破棄)
        </v-btn>
      </v-container> -->
      <!-- <div>.</div>
      <v-btn outlined @click="AuthFromInput()">
        インプットから認可を求める(dev)(old)
      </v-btn> -->
      <!-- <div>.</div>
      <v-btn outlined @click="StoreToCookie()">
        StoreからCookieにトークンを渡す(再訪問用)
      </v-btn>
      <v-btn outlined @click="CookieToStore()">
        CookieからStoreにトークンを渡す(再訪問用)
      </v-btn> -->
    </v-flex>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
// import axios from "axios";
// import VueCookies from "vue-cookies";
// import router from "../router";
import store from "../store";

export default Vue.extend({
  data() {
    return {
      email: String(),
      password: String(),
      loading: Boolean(),
      input_token: String()
    };
  },
  // computed: {
  //   GetUserName() {
  //     console.log(this.$store.getters.userName);
  //   }
  // },
  computed: {
    CurrentUserName() {
      return store.getters.userName;
    }
  },
  methods: {
    Login() {
      // this.$store.state
      store
        .dispatch("login", { email: this.email, password: this.password })
        .then(() => {
          // console.log("responsed");
        })
        .catch(() => {
          console.log("error");
        });
    },
    Logout() {
      store.dispatch("logout");
    },
    CheckAuth() {
      store
        .dispatch("confirm", store.getters.token)
        .then(() => {
          console.log("token confirming");
        })
        .catch(() => console.log("error"));
    }
  },
  created: function() {
    // this.CheckAuth();
  }
});
</script>

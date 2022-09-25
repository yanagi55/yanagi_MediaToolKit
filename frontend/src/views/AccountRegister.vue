<template>
  <v-container>
    <v-flex xs12 sm6 offset-sm3>
      <v-card v-if="!$store.getters.userName">
        <v-card-text>
          <v-container>
            <form @submit.prevent="Register()">
              <v-flex xs12>
                <v-text-field
                  name="email"
                  label="メールアドレス / E-mail"
                  id="email"
                  v-model="email"
                  type="email"
                  required
                ></v-text-field>
                <v-text-field
                  name="username"
                  label="ユーザーネーム / User Name"
                  id="username"
                  v-model="username"
                  type="username"
                  required
                ></v-text-field>
                <v-text-field
                  name="password"
                  label="パスワード / Password"
                  id="password"
                  v-model="password"
                  type="password"
                  required
                ></v-text-field>
                <v-text-field
                  name="confirmPassword"
                  label="パスワード確認 / Validate Password"
                  id="confirmPassword"
                  v-model="confirmPassword"
                  type="password"
                  :rules="[comparePasswords]"
                ></v-text-field>
                <div class="text-center mt-2">
                  <v-btn type="submit" :loading="loading">登録</v-btn>
                </div>
              </v-flex>
              <!-- <v-flex xs12>
                <v-btn type="submit" :loading="loading">Sign up</v-btn>
              </v-flex> -->
            </form>
          </v-container>
        </v-card-text>
      </v-card>
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
import axios from "axios";
import VueCookies from "vue-cookies";
import router from "../router";
import store from "../store";

export default Vue.extend({
  data() {
    return {
      email: String(),
      username: String(),
      password: String(),
      confirmPassword: String(),
      loading: Boolean()
      // input_token: String()
    };
  },
  computed: {
    CurrentUserName() {
      return store.getters.userName;
    },
    comparePasswords() {
      if (this.password === this.confirmPassword) {
        return true;
      } else {
        return false;
      }
    }
  },
  methods: {
    Register() {
      console.log(this.username);
      const form = new FormData();
      form.append("username", this.username);
      form.append("email", this.email);
      form.append("password", this.password);
      // console.log();

      axios.post("/user/register", form).then(response => {
        console.log(response.data);
        if (response.data) {
          alert("アカウントが作成されました。");
          this.Login();
        }
      });
    },
    Login() {
      // this.$store.state
      store
        .dispatch("login", { email: this.email, password: this.password })
        .then(response => {
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

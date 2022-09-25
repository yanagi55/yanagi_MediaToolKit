import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import router from '../router'
import VueCookie from 'vue-cookies'
Vue.use(Vuex)
export default new Vuex.Store({
  modules: {},
  state: {
    isLogin: Boolean(false), // ログインセッションであるか確認
    isAuth: Boolean(false), // トークンが認証出来ているか確認
    token: String(), // 発行されたトークンを格納する(今は形式だけ)
    userName: String()
  },

  getters: {
    isLogin(state) {
      return state.isLogin
      // return state.token ? true : false;
    },
    isAuth(state) {
      return state.isAuth
    },
    userName(state) {
      return state.userName
    }
  },
  mutations: {
    login(state, payload) {
      state.token = payload
    },
    tokenAuth(state, username) {
      state.isAuth = true;
      state.userName = username;
    },
    logout(state) {
      state.token = ''
    }
  },
  actions: {
    // fetchName({ dispatch, commit }, payload) {
    //   dispatch("confirm").then(() => {
    //     console.log('t');
    //     // return
    //   })
    // },
    confirm({ commit }, payload) {
      // console.log('store.actions confirm() token')
      if (payload === false) {
        payload = Vue.$cookies.get('yf_token')
      }
      axios
        .get('/user/authorize', {
          headers: {}
        })
        .then(response => {
          this.state.isAuth = true
          // this.state.userName = response.data.user
          commit('tokenAuth', response.data.user)
          console.log('isLogin:' + this.getters.isLogin)
          console.log('isAuth:' + this.getters.isAuth)
          console.log('userName:' + this.getters.userName)
        })
        .catch(error => {
          // console.log(error.response)
          // console.log(error.response.data.detail)
          if (error.response.status === 401) {
            console.log('認証に失敗しました。')
          }
        })
    },

    login({ commit }, payload) {
      axios
        .get('/user/authenticate', {
          auth: {
            username: payload.email,
            password: payload.password
          }
        })
        .then(response => {
          this.state.isLogin = true //
          const token = 'Bearer ' + response.data.access_token
          // axios.defaults.headers.common['Authorization'] = token; // すべてのヘッダに入れる
          commit('login', token)
          commit('tokenAuth')
          Vue.$cookies.set('yf_token', token, '3h', undefined, undefined, true)
          router.push({ path: '/' })
          console.log('logined')
        })
        .catch(error => {
          console.log('login error')
          console.log(error)
        })
    },
    logout({ commit }) {
      axios
        .post('/user/logout')
        .then(response => {
          commit('logout')
          // router.push({ path: '/' })
          Vue.$cookies.remove('yf_token')
          this.state.isAuth = false
          this.state.isLogin = false
          this.state.userName = ''
          // alert('ログアウトしました。')
          // commit('alert/setAlert', {
          //   'message': 'ログアウトしました'
          // }, {
          //   root: true
          // });
        })
        .catch(error => {
          console.log(error)
          commit('alert/setAlert', {
            message: 'ログアウトに失敗しました'
          }, {
            root: true
          })
        })
    }
  }
})

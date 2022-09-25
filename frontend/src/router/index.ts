import Vue, { VueConstructor } from 'vue'
import VueRouter from 'vue-router'
import store from '@/store'
import Home from '@/views/Home.vue'
import Account from '@/views/Account.vue'
Vue.use(VueRouter)

interface YfRouterType { // 厳格な型
  path: string;
  name: string;
  component: VueConstructor<Vue> | (() => Promise<typeof import("@/views/*.vue")>);
  meta: {
    title: string;
    needToken: boolean;
    needLogin: boolean;
  }
}

const routes: YfRouterType[] = [{
  // const routes = [{
  path: '/',
  name: 'Home',
  // component: () => import(/* webpackChunkName: "Home" */ '@/views/Home.vue'),
  component: Home,
  meta: {
    title: 'ホーム',
    needToken: false,
    needLogin: false,
  }
},
{
  path: '/account',
  name: 'Account',
  // component: () => import(/* webpackChunkName: "Account" */ '@/views/Account.vue'),
  component: Account,
  meta: {
    needToken: false,
    needLogin: false,
    title: 'アカウント'
  }
},
{
  path: '/account-register',
  name: 'AccountRegister',
  component: () => import(/* webpackChunkName: "AccountRegister" */ '@/views/AccountRegister.vue'),
  // component: Account,
  meta: {
    needToken: false,
    needLogin: false,
    title: 'アカウント登録'
  }
},
{
  path: '/photo-uploader',
  name: 'PhotoUploader',
  component: () => import(/* webpackChunkName: "PhotoUploader" */ '@/views/PhotoUploader.vue'),
  meta: {
    title: 'フォトアップローダー',
    needToken: false,
    needLogin: true,
  }
},
{
  path: '/cover-art-replacer',
  name: 'CoverArtReplacer',
  // route level code-splitting
  // this generates a separate chunk (about.[hash].js) for this route
  // which is lazy-loaded when the route is visited.
  component: () => import(/* webpackChunkName: "CoverArtReplacer" */ '@/views/CoverArtReplacer.vue'),
  meta: {
    title: 'mp3カバーアート置き換え',
    needToken: true,
    needLogin: false,
  }
},
{
  path: '/video-player',
  name: 'VideoPlayer',
  component: () => import(/* webpackChunkName: "VideoPlayer" */ '@/views/VideoPlayer.vue'),
  meta: {
    title: 'ビデオプレーヤー',
    needToken: false, //dev
    needLogin: false,
  }
},
{
  path: '/video-uploader',
  name: 'VideoUploader',
  component: () => import(/* webpackChunkName: "VideoUploader" */ '@/views/VideoUploader.vue'),
  meta: {
    title: 'ビデオアップローダー',
    needToken: false, // dev
    needLogin: false,
  }
},
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: routes,
})

// ページの遷移のとき、権限を確認する。
router.beforeEach((to, from, next) => {
  if (to.matched.some(page => (page.meta.needToken || page.meta.needLogin) === false)) {
    next()
  } else if (to.matched.some(page => page.meta.needToken) && store.getters.isAuth) {
    next()
  } else if (to.matched.some(page => page.meta.needLogin) && store.getters.isLogin) {
    next()
  } else {
    next('/account')
    console.log('not logged in. transfering account page.')
  }
  document.title = to.meta?.title + " | YF ToolKit"
})

export default router

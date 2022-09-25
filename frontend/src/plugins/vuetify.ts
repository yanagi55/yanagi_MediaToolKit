import Vue from 'vue'
import Vuetify from 'vuetify/lib/framework'

Vue.use(Vuetify)

const myvuetify = new Vuetify({
  theme: {
    dark: false,
    themes: {
      dark: {
        custom: '#FF0000'
      },
      light: {
        custom: '#0000FF',
        // color: '',
        // 'text--primary': { '#0000ff'},
      }
    }
  }
})
export default myvuetify

//★書き方の例
// export default new Vuetify({
//   theme: {
//     dark: false,
//     themes: {
//       dark: {
//         custom: '#222222'
//       }
//     }
//   }
// })

//★デフォルト
// export default new Vuetify({
//   theme: { dark: false }
// })

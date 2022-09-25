module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  // vuetify: {
  //   customVariables: ['~/assets/vuetify_variables.scss']
  // },
  assetsDir: 'static',
  pages: {
    index: {
      entry: 'src/main.ts', // 必須パラメータ
      title: 'YF ToolKit',
    }
  },
  pwa: {
    name: 'YF ToolKit'
  },
  // セミコロン入れても入れなくても「入れるな」「入れろ」のエラーが出る。
  // またグローバルCSSは各スクリプトに強引に埋め込む感じっぽいので、
  // リソース節約の意味でも不要っぽい
  // css: {
  //   loaderOptions: {
  //     sass: {
  //       additionalData: `
  //         @import "@/styles_notworking/variables.scss"
  //       `
  //     }
  //   }
  // },
  devServer: {
    port: 8081,
    host: '127.0.0.1',

    proxy: {
      '^/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      },
      '^/user': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      },
      '^/storage': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      }
    }

  }
}

module.exports = {
  root: true,
  env: {
    node: true
  },
  extends: [
    'plugin:vue/essential',
    '@vue/standard',
    '@vue/typescript/recommended'
  ],
  parserOptions: {
    ecmaVersion: 2020
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    // ESLint向けの強引な設定
    camelcase: "off",
    "comma-dangle": "off",
    "comma-spacing": "off",
    eqeqeq: "off",
    "handle-callback-err": "off",
    indent: "off",
    "key-spacing": "off",
    "keyword-spacing": "off",
    "no-multi-spaces": "off",
    "no-undef": "off",
    "no-unused-vars": "off",
    "object-curly-spacing": "off",
    quotes: "off",
    semi: "off",
    "space-before-function-paren": "off",
    "space-before-blocks": "off",
    "space-in-parens": "off",
    "spaced-comment": "off",
    "space-infix-ops": "off",
    "no-dupe-keys": "off",
    "no-fallthrough": "off",
    "no-spaced-func": "off",
    "no-multiple-empty-lines": "off",
    "no-trailing-spaces": "off",
    "padded-blocks": "off"
  },
  overrides: [{
    files: [
      '**/__tests__/*.{j,t}s?(x)',
      '**/tests/unit/**/*.spec.{j,t}s?(x)'
    ],
    env: {
      jest: true
    }
  }]
}

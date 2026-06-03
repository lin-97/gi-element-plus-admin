import antfu from '@antfu/eslint-config'

export default antfu({
  vue: true,
  typescript: true,
  formatters: true,
  rules: {
    'vue/multi-word-component-names': 'off',
    'no-console': 'off',
    'e18e/prefer-static-regex': 'off',
  },
})

const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})
module.exports = {
  devServer: {
    proxy: {
      '/user': {
        target: 'http://218.199.69.89:5000',
        changeOrigin: true,
        pathRewrite: {
          '^/user': '/user'
        }
      }
    }
  }
};
module.exports = {
  devServer: {
    port: 8099
  }
}
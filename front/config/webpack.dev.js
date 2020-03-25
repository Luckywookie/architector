const path = require('path');
const paths = require('./paths');
const merge = require('webpack-merge');
const common = require('./webpack.common.js');

module.exports = merge(common, {
   mode: 'development',
   devtool: 'source-map',
   devServer: {
    hot: true,
    publicPath: '/',
    contentBase: paths.appPublic,
    historyApiFallback : true,
    open: false,
    host: '0.0.0.0',
    port: 3000,
    proxy: {
      '/api/**': {
        target: 'http://localhost:9999',
        secure: false,
        changeOrigin: true
      }
    },
    logLevel: 'debug'
  },
});

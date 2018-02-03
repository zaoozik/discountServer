var webpack = require('webpack');
var path = require('path');

var BUILD_DIR = path.resolve('D:\\projects\\discountServer\\back\\discountServer\\static\\js\\');
var APP_DIR = path.resolve('.\\web_client\\');

var config = {
  entry: ['babel-polyfill',APP_DIR + '\\app.jsx'],
  output: {
    path: BUILD_DIR,
    filename: 'app.js'
  },
  module : {
    loaders : [
      {
        test : /\.jsx?/,
        include : APP_DIR,
        exclude: /node_modules/,
        loader : 'babel-loader'
      }
    ]
  }
};

module.exports = config;
const webpack = require('webpack');
const paths = require('./paths');
const path = require('path');
const getClientEnvironment = require('./env');
const InterpolateHtmlPlugin = require('react-dev-utils/InterpolateHtmlPlugin');
const CaseSensitivePathsPlugin = require('case-sensitive-paths-webpack-plugin');
const WatchMissingNodeModulesPlugin = require('react-dev-utils/WatchMissingNodeModulesPlugin');

const publicPath = '/';
const publicUrl = '/';
const env = getClientEnvironment(publicUrl);

const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
  entry: paths.appIndexJs,
  output: {
    path: paths.appBuild,
    pathinfo: true,
    filename: 'static/js/bundle.js',
    publicPath,
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },
  module: {
    rules: [
      {
        test: /\.(png|jpg|jpeg|gif|ico)$/,
        include: [
          paths.appSrc,
          path.resolve(paths.appNodeModules, '@robokassa')
        ],
        use: [
          {
            loader: 'file-loader',
            options: {
              outputPath: 'images',
              name: '[name]-[sha1:hash:7].[ext]'
            }
          }
        ]
      },
      {
        test: /\.svg$/,
        loader: 'svg-inline-loader'
      },
      {
        test: /\.(ttf|otf|eot|woff|woff2)$/,
        include: [
          paths.appSrc,
          path.resolve(paths.appNodeModules, '@robokassa')
        ],
        use: [
          {
            loader: 'file-loader',
            options: {
              outputPath: 'fonts',
              name: '[name].[ext]'
            }
          }
        ]
      },
      {
        test: /\.s[ac]ss$/,
        include: [
          paths.appSrc,
          path.resolve(paths.appNodeModules, '@robokassa')
        ],
        use: [
          {
            loader: 'style-loader',
            options: {
              sourceMap: false,
              url: false
            },
          },
          {
            loader: 'css-loader',
            options: {
              modules: {
                mode: 'local',
                localIdentName: '[name]__[local]__[hash:4]',
                context: paths.appSrc,
              },
              sourceMap: false,
              url: true,
            },
          },
          {
            loader: 'resolve-url-loader',
              options: {
                root: ''
              }

          },
          {
            loader: 'sass-loader',
            options: {
              sourceMap: true,
            },
          },
        ],
      },
      {
        test: /\.(js|jsx)$/,
        // exclude: /node_modules/,
        include: [
          paths.appSrc,
          path.resolve(paths.appNodeModules, '@robokassa')
        ],
        use: [
          {
            loader: "babel-loader",
            options: {
              cacheDirectory: true,
              babelrc: true,
            }
          },
        ]
      },
    ],
  },
  plugins: [
    new InterpolateHtmlPlugin(HtmlWebpackPlugin, env.raw),
    new webpack.DefinePlugin(env.stringified),
    new webpack.HotModuleReplacementPlugin(),
    new HtmlWebpackPlugin({
      inject: true,
      template: paths.appHtml,
    }),
    new CaseSensitivePathsPlugin(),
    new WatchMissingNodeModulesPlugin(paths.appNodeModules),
  ],
  node: {
    global: false,
    __filename: 'mock',
    __dirname: 'mock',
  }
};

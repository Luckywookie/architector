module.exports = {
  presets: [
    [
      '@babel/preset-env',
      {
        modules: false,
        useBuiltIns: 'usage',
        debug: true,
        targets: {
          browsers: [
            ">1%",
            "last 3 versions"
          ]
        }
      },
    ],
    '@babel/preset-react',
  ],
  plugins: [
    '@babel/plugin-transform-modules-commonjs',
    ['@babel/plugin-proposal-decorators', { legacy: true }],
    '@babel/plugin-proposal-optional-chaining',
    '@babel/plugin-syntax-dynamic-import',
    '@babel/plugin-syntax-import-meta',
    '@babel/plugin-syntax-object-rest-spread',
    '@babel/plugin-proposal-json-strings',
    '@babel/plugin-proposal-function-sent',
    '@babel/plugin-proposal-export-namespace-from',
    '@babel/plugin-proposal-numeric-separator',
    '@babel/plugin-proposal-throw-expressions',
    'react-hot-loader/babel',
    [
      '@babel/plugin-proposal-class-properties',
      {
        loose: true,
      },
    ],
    '@babel/plugin-transform-runtime',
  ],
  env: {
    development: {
      plugins: ['react-hot-loader/babel'],
    },
    test: {
      presets: [
        '@babel/preset-env',
        '@babel/preset-react',
      ]
    },
  },
};

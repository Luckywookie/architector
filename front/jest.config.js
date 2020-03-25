module.exports = {
  collectCoverage: true,
  moduleNameMapper: {
    '\\.(css|less|scss)$': 'identity-obj-proxy',
  },
  // moduleNameMapper: {
  //   '\\.(css|less|svg|png|jpg|scss)$': '<rootDir>/mock_css.js',
  // },
  snapshotSerializers: ['enzyme-to-json/serializer'],
  transform: {
    '.+\\.(css|styl|less|sass|scss)$': 'jest-css-modules-transform',
    '\\.(js|jsx)?$': 'babel-jest',
    '.+\\.(png|jpg)$': 'identity-obj-proxy',
    '^.+\\.svg$': 'jest-svg-transformer',
  },
  testRegex: ['.*\\.test\\.js$'], // finds test
  moduleFileExtensions: ['js', 'jsx', 'json', 'node'],
  testPathIgnorePatterns: ['<rootDir>[/\\\\](build|docs|node_modules|scripts)[/\\\\]'],
  transformIgnorePatterns: ['/node_modules/(?!@robokassa)'],
};

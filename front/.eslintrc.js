module.exports = {
  env: {
    es6: true,
    browser: true,
    node: true,
    commonjs: true
  },
  extends: [
    "airbnb",
    "plugin:jest/recommended",
    "plugin:react/recommended",
    "jest-enzyme",
    "esnext"
  ],
  plugins: [
    "import",
    "react",
    "babel"
  ],
  parser: "babel-eslint",
  parserOptions: {
    ecmaVersion: 2018,
    sourceType: "module",
    ecmaFeatures: {
      jsx: true,
      globalReturn: true,
      experimentalObjectRestSpread: true
    }
  },
  globals: {React: true},
  rules: {
    "indent": 0,
    "import/prefer-default-export": 0,
    "linebreak-style": "off",
    "operator-linebreak": [1, "after"],

    "arrow-parens": 0,
    "object-curly-newline": 0,
    "no-mixed-operators": 0,
    "arrow-body-style": 0,
    "function-paren-newline": 0,
    "no-plusplus": 0,
    "space-before-function-paren": 0,
    "implicit-arrow-linebreak": 0,
    "no-confusing-arrow": 0,

    "max-len": ["error", 100, 2, { ignoreUrls: true, }],
    "no-console": 1, // airbnb use warn
    "no-alert": "error", // airbnb use warn

    "no-param-reassign": 0,
    "radix": 0,
    "lines-between-class-members" : 1,
    "no-unused-vars": 0,  // TODO: delete
    "no-undef": 1, // TODO: delete

    "react/jsx-uses-react": 1,

    "react/require-default-props": 0, // airbnb use error
    "react/forbid-prop-types": 0, // airbnb use error
    "react/prop-types": 0,
    "react/jsx-filename-extension": ["error", { extensions: [".js", ".jsx"] }], // airbnb is use .jsx
    "react/jsx-boolean-value": 0,
    "react/jsx-curly-newline": 0,

    "prefer-destructuring": 0,
    "react/jsx-indent": 0,
    "no-else-return": 0,

    "react/no-find-dom-node": 0,
    "react/no-did-mount-set-state": 0,
    "react/no-unused-prop-types": 0,
    "react/jsx-one-expression-per-line": 0,
    "react/jsx-props-no-spreading": 0,
    "react/jsx-uses-vars": 0,
    "react/destructuring-assignment": 0,
    "react/state-in-constructor": 0,

    "jsx-a11y/anchor-is-valid": ["error", { "components": ["Link"], "specialLink": ["to"] }],
    "jsx-a11y/anchor-has-content": "off",
    "jsx-a11y/label-has-for": [2, {
      "required": {
        "every": ["id"]
      }
    }],

    "import/no-extraneous-dependencies": ["error", {"devDependencies": true}]
  },
  settings: {
    react: {
      createClass: "createReactClass", // Regex for Component Factory to use
      pragma: "React",  // Pragma to use, default to "React"
      version: "detect", // React version. "detect" automatically picks the version you installed.
    },
    linkComponents: [
      // Components used as alternatives to <a> for linking, eg. <Link to={ url } />
      "Hyperlink", { name: "Link", linkAttribute: "to" }
    ]
  }
};

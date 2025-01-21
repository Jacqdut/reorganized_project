const eslintPluginReact = require('eslint-plugin-react');

module.exports = [
  {
    languageOptions: {
      parser: '@babel/eslint-parser', // Use the Babel parser
      parserOptions: {
        ecmaVersion: 2021,
        sourceType: 'module',
        ecmaFeatures: {
          jsx: true,
        },
      },
    },
    env: {
      browser: true,
      node: true,
      es6: true,
      jest: true,
    },
    plugins: ['react'],
    extends: [
      'eslint:recommended',
      'plugin:react/recommended',
      'plugin:react/jsx-runtime',
    ],
    rules: {
      'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
      'react/prop-types': 'off',
      'react/react-in-jsx-scope': 'off', // No need for React import with React 17+
      'no-console': 'warn',
      'no-debugger': 'warn',
      'react/jsx-uses-vars': 'error',
      'no-undef': 'error',
    },
  },
];

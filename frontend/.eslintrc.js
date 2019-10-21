module.exports = {
    env: {
        browser: true,
        es6: true,
        node: true,
    },
    parserOptions: {
        parser: 'babel-eslint',
    },
    extends: [
        'airbnb-base',
        'plugin:vue/recommended',
    ],
    rules: {
        indent: ['error', 4],
        'linebreak-style': ['error', 'windows'],
        'vue/html-indent': ['error', 4],
        'comma-dangle' : ['error', 'never'],
        "import/no-extraneous-dependencies": ["error", {"devDependencies": true}]
    },
};

// eslint-disable-next-line no-undef
module.exports = {
    plugins: [
        "@babel/plugin-transform-typescript",
        ["module-resolver", {
            root: ["./src"]
        }]
    ],
    presets: [
        "@babel/preset-typescript",
        ["@babel/preset-env", {
            targets: {
                esmodules: true,
            },
        }]
    ]
}

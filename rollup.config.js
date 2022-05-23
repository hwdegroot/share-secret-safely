import pluginTypescript from "@rollup/plugin-typescript";
import pluginCommonjs from "@rollup/plugin-commonjs";
import multiEntry from "@rollup/plugin-multi-entry";
import pluginNodeResolve from "@rollup/plugin-node-resolve";
import { babel } from "@rollup/plugin-babel";
import * as path from "path";
import pkg from "./package.json";

const moduleName = pkg.name.replace(/^@.*\//, "");
const inputFileName = "src/**/*.ts";
const author = pkg.author;
const banner = `
  /**
   * @license
   * author: ${author}
   * ${moduleName}.js v${pkg.version}
   * Released under the ${pkg.license} license.
   */
`;

export default [
    // Browser
    {
        input: inputFileName,
        output: [
            {
                file: pkg.browser,
                format: "iife",
                sourcemap: (process.env.NODE_ENV || "").toLowerCase() != "production",
                banner,
                extend: true,
                globals: {
                    axios: "axios",
                }
            },
        ],
        external: [
            ...Object.keys(pkg.dependencies || {}),
            ...Object.keys(pkg.devDependencies || {}),
        ],
        plugins: [
            multiEntry(),
            pluginTypescript(),
            pluginCommonjs({
                extensions: [".js", ".ts"],
            }),
            babel({
                babelHelpers: "bundled",
                configFile: path.resolve(__dirname, "babel.config.js"),
            }),
            pluginNodeResolve({
                browser: false,
            }),
        ]
    },
];

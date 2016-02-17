System.config({
  baseURL: "/static",
  defaultJSExtensions: true,
  transpiler: "babel",
  babelOptions: {
    "stage": 0,
    "optional": [
      "runtime",
      "optimisation.modules.system"
    ]
  },
  paths: {
    "github:*": "jspm_packages/github/*",
    "npm:*": "jspm_packages/npm/*"
  },

  meta: {
    "js/src/chart.js": {
      "deps": [
        "jquery",
        "highstock",
        "highcharts"
      ]
    },
    "js/src/chart2.js": {
      "deps": [
        "jquery",
        "highstock",
        "highcharts"
      ]
    }
  },

  map: {
    "ajax_call": "js/ajax_call.js",
    "babel": "npm:babel-core@5.8.35",
    "babel-runtime": "npm:babel-runtime@5.8.35",
    "bootstrap": "github:twbs/bootstrap@3.3.6",
    "core-js": "npm:core-js@1.2.6",
    "highcharts": "npm:highcharts-release@4.2.3",
    "highstock": "npm:highcharts-release@4.2.3/highstock.js",
    "jquery": "npm:jquery@2.2.0",
    "qc-init": "js/quescheetah-init.js",
    "qc-sdk": "js/quescheetah-sdk-0.1.0.js",
    "submit": "js/submit.js",
    "systemjs": "npm:systemjs@0.19.18",
    "github:jspm/nodelibs-assert@0.1.0": {
      "assert": "npm:assert@1.3.0"
    },
    "github:jspm/nodelibs-path@0.1.0": {
      "path-browserify": "npm:path-browserify@0.0.0"
    },
    "github:jspm/nodelibs-process@0.1.2": {
      "process": "npm:process@0.11.2"
    },
    "github:jspm/nodelibs-util@0.1.0": {
      "util": "npm:util@0.10.3"
    },
    "github:twbs/bootstrap@3.3.6": {
      "jquery": "github:components/jquery@2.2.0"
    },
    "npm:assert@1.3.0": {
      "util": "npm:util@0.10.3"
    },
    "npm:babel-runtime@5.8.35": {
      "process": "github:jspm/nodelibs-process@0.1.2"
    },
    "npm:core-js@1.2.6": {
      "fs": "github:jspm/nodelibs-fs@0.1.2",
      "path": "github:jspm/nodelibs-path@0.1.0",
      "process": "github:jspm/nodelibs-process@0.1.2",
      "systemjs-json": "github:systemjs/plugin-json@0.1.0"
    },
    "npm:es6-module-loader@0.17.10": {
      "fs": "github:jspm/nodelibs-fs@0.1.2",
      "process": "github:jspm/nodelibs-process@0.1.2",
      "systemjs-json": "github:systemjs/plugin-json@0.1.0",
      "util": "github:jspm/nodelibs-util@0.1.0",
      "when": "npm:when@3.7.7"
    },
    "npm:highcharts-browserify@2.0.2": {
      "highcharts-release": "npm:highcharts-release@4.2.3",
      "process": "github:jspm/nodelibs-process@0.1.2"
    },
    "npm:highcharts-release@4.2.3": {
      "process": "github:jspm/nodelibs-process@0.1.2"
    },
    "npm:inherits@2.0.1": {
      "util": "github:jspm/nodelibs-util@0.1.0"
    },
    "npm:path-browserify@0.0.0": {
      "process": "github:jspm/nodelibs-process@0.1.2"
    },
    "npm:process@0.11.2": {
      "assert": "github:jspm/nodelibs-assert@0.1.0"
    },
    "npm:systemjs@0.19.18": {
      "es6-module-loader": "npm:es6-module-loader@0.17.10",
      "fs": "github:jspm/nodelibs-fs@0.1.2",
      "process": "github:jspm/nodelibs-process@0.1.2",
      "systemjs-json": "github:systemjs/plugin-json@0.1.0",
      "when": "npm:when@3.7.7"
    },
    "npm:util@0.10.3": {
      "inherits": "npm:inherits@2.0.1",
      "process": "github:jspm/nodelibs-process@0.1.2"
    },
    "npm:when@3.7.7": {
      "process": "github:jspm/nodelibs-process@0.1.2"
    }
  }
});

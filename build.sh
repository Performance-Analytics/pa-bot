#!/bin/bash

mkdir dest
tsc src/main.ts --outFile dest/index.js --target es5 --lib dom,es6

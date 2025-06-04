#!/bin/bash

#create folder build while not exist
mkdir -p build

#build
gcc -o ./build/hello spam_hello.c
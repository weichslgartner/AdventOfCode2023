#!/bin/bash
pushd .
cd Rust
for file in */
do
    cd ${file}
    cargo build --release
    time target/release/${file%/}
    printf "\n"
    cd ..
done
popd
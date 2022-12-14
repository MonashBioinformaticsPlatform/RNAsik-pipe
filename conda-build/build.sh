#!/bin/bash
sik_version=${PKG_VERSION}

mkdir -p "${PREFIX}/bin"
mkdir -p "${PREFIX}/opt/rnasik-${sik_version}"
sed -i "s/src\/RNAsik.bds/opt\/rnasik-${sik_version}\/src\/RNAsik.bds/" bin/RNAsik
cp -r "bin" "${PREFIX}/opt/rnasik-${sik_version}"
cp -r "src" "${PREFIX}/opt/rnasik-${sik_version}"
cp -r "scripts" "${PREFIX}/opt/rnasik-${sik_version}"
cp -r "configs" "${PREFIX}/opt/rnasik-${sik_version}"
cp -r "supplementary" "${PREFIX}/opt/rnasik-${sik_version}"
ln -s "${PREFIX}/opt/rnasik-${sik_version}/bin/RNAsik" "${PREFIX}/bin/RNAsik"

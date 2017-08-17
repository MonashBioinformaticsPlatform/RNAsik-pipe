#!/bin/bash

sik_origin=`dirname "${BASH_SOURCE[0]}"`
bds_config="$(which bds).config"
bds -c ${bds_config} -log -reportHtml "${sik_origin}"/../src/RNAsik.bds "$@"

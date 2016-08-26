#!/bin/bash
/bin/uname -a | /bin/grep 'x86_64' > /dev/null && ARCH='64' || ARCH='32'

XPLORHOME=$VO_ENMR_EU_SW_DIR/CIRMMP/xplor-nih/2.29/$ARCH

DIRAE=$XPLORHOME/bin
export TOPPAR=$XPLORHOME/toppar
tar xvfz in.tgz

$DIRAE/xplor < xplorPM.inp > out_generate_protein

tar cvfz pro.tgz ./*


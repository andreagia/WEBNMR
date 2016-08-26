#!/bin/bash
export PATH=/usr/local/bin:/bin:/usr/bin
ls sub_usecase/ > listinput
grep final ./sub_usecase/input*/out*/std.out | awk '{print $5,$4,$3}'| sort -n -k 1,2 --output=0.crv
grep '0.000' 0.crv |awk '{print $3}'> 0.mo


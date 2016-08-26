#!/bin/bash
export homed=`pwd`/sub_usecase/
mkdir $homed
for n in `cat $1`
do
mkdir $homed/input_$n
cp ./in.tgz $homed/input_$n

#export NEW=$n
export NEW=$homed/input_$n/
echo $NEW
sed "s#CAMBIA#$NEW#g" ./run_a-map_mu.jdl > $homed/input_$n/run_a-map_mu.jdl
sed "s/maxoccenmr.64 1 /maxoccenmr.64 $n /g" ./run_a-map.sh > $homed/input_$n/run_a-map.sh
done


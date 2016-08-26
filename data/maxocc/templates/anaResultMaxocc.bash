export PATH=/usr/local/bin:/bin:/usr/bin
if [ -d "output" ]; then
  rm -rf output
  rm -rf results.tgz
fi

mkdir output
mkdir ootputtemp
cd ootputtemp
for FILE in $(find ../ -name out.tgz)
do
echo $FILE
DIR1=`echo "$FILE" | cut -d'/' -f3`
DIR2=`echo "$DIR1" | cut -d't' -f2`
DIR=result$DIR2
echo $DIR
mkdir ../output/$DIR
tar xvfz $FILE
cp ./results/* ../output/$DIR
rm  ./results/*
done
cd ..
rm -rf ootputtemp
tar cvfz results.tgz output 

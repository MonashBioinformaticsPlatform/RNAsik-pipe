origin=${BASH_SOURCE[0]}
test_dir=$(dirname $origin)
cd $test_dir
cd ..

for t in test/*.bds
do
  echo ""
  echo "Running: bds -t $t"
  echo ""
  bds -t $t
done

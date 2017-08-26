dir=`dirname $0`
python $dir/categorize.py $dir/train.txt
python $dir/categorize.py $dir/test.txt --test
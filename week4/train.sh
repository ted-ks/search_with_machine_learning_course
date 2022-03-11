# With 1 min-queries

# ~/fastText-0.9.2/fasttext supervised -input label_q_train.txt -output model_label
#echo "Testing #1"
# ~/fastText-0.9.2/fasttext test model_label.bin label_q_test.txt
#echo "Testing #2 with R@3"
# ~/fastText-0.9.2/fasttext test model_label.bin label_q_test.txt 3
#echo "Testing #3 with R@5"
# ~/fastText-0.9.2/fasttext test model_label.bin label_q_test.txt 5

# echo "Training with all options and 1 min query"
# ~/fastText-0.9.2/fasttext supervised -input label_q_train.txt -output model_label_all -epoch 25 -lr 0.5 -wordNgrams 2
# echo "Testing #1"
# ~/fastText-0.9.2/fasttext test model_label_all.bin label_q_test.txt
# echo "Testing #2 with R@3"
# ~/fastText-0.9.2/fasttext test model_label_all.bin label_q_test.txt 3
# echo "Testing #3 with R@5"
# ~/fastText-0.9.2/fasttext test model_label_all.bin label_q_test.txt 5


# With 100 min queries

echo "Training with no options and 100 min query"
~/fastText-0.9.2/fasttext supervised -input label_q_100_train.txt -output model_label_100
echo "Testing #1"
~/fastText-0.9.2/fasttext test model_label_100.bin label_q_100_test.txt
echo "Testing #2 with R@3"
~/fastText-0.9.2/fasttext test model_label_100.bin label_q_100_test.txt 3
echo "Testing #3 with R@5"
~/fastText-0.9.2/fasttext test model_label_100.bin label_q_100_test.txt 5

echo "Training with all options and 100 min query"
~/fastText-0.9.2/fasttext supervised -input label_q_100_train.txt -output model_label_100_all -epoch 25 -lr 0.5 -wordNgrams 2
echo "Testing #1"
~/fastText-0.9.2/fasttext test model_label_100_all.bin label_q_100_test.txt
echo "Testing #2 with R@3"
~/fastText-0.9.2/fasttext test model_label_100_all.bin label_q_100_test.txt 3
echo "Testing #3 with R@5"
~/fastText-0.9.2/fasttext test model_label_100_all.bin label_q_100_test.txt 5

# With 1000 min queries

echo "Training with no options and 1000 min query"
~/fastText-0.9.2/fasttext supervised -input label_q_1000_train.txt -output model_label_1000
echo "Testing #1"
~/fastText-0.9.2/fasttext test model_label_1000.bin label_q_1000_test.txt
echo "Testing #2 with R@3"
~/fastText-0.9.2/fasttext test model_label_1000.bin label_q_1000_test.txt 3
echo "Testing #3 with R@5"
~/fastText-0.9.2/fasttext test model_label_1000.bin label_q_1000_test.txt 5


echo "Training with all options and 1000 min query"
~/fastText-0.9.2/fasttext supervised -input label_q_1000_train.txt -output model_label_1000_all -epoch 25 -lr 0.5 -wordNgrams 2
echo "Testing #1"
~/fastText-0.9.2/fasttext test model_label_1000_all.bin label_q_1000_test.txt
echo "Testing #2 with R@3"
~/fastText-0.9.2/fasttext test model_label_1000_all.bin label_q_1000_test.txt 3
echo "Testing #3 with R@5"
~/fastText-0.9.2/fasttext test model_label_1000_all.bin label_q_1000_test.txt 5
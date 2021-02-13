cd ..
steps/get_train_ctm.sh data/train/ data/lang exp/tri1
cd task6/
python3 phrase_extract.py $1

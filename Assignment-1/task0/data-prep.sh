#!/usr/bin/env bash

# Copyright 2017 Xingyu Na
# Apache 2.0

. ./path.sh || exit 1;

if [ $# != 2 ]; then
  echo "Usage: $0 <corpus-path> <text-path>"
  echo " $0 /export/a05/xna/data/data_aidatatang_200zh/corpus /export/a05/xna/data/data_aidatatang_200zh/transcript"
  exit 1;
fi

aidatatang_audio_dir=$1
aidatatang_text=$2/transcriptions.txt

train_dir=corpus/data/train
dev_dir=corpus/data/truetest
test_dir=corpus/data/test
tmp_dir=corpus/data/tmp

mkdir -p $train_dir
mkdir -p $dev_dir
mkdir -p $test_dir
mkdir -p $tmp_dir

# data directory check
if [ ! -d $aidatatang_audio_dir ] || [ ! -f $aidatatang_text ]; then
  echo "Error: $0 requires two directory arguments"
  exit 1;
fi

# find wav audio file for train, dev and test resp.
find $aidatatang_audio_dir/SWH-05-20101106 -iname "*.wav" > $train_dir/wav.flist
find $aidatatang_audio_dir/SWH-05-20101107 -iname "*.wav" >> $train_dir/wav.flist
find $aidatatang_audio_dir/SWH-05-20101109 -iname "*.wav" >> $train_dir/wav.flist
find $aidatatang_audio_dir/SWH-05-20101110 -iname "*.wav" >> $train_dir/wav.flist

find $aidatatang_audio_dir/SWH-05-20101113 -iname "*.wav" > $test_dir/wav.flist
find $aidatatang_audio_dir/SWH-05-20110123 -iname "*.wav" >> $test_dir/wav.flist

find $aidatatang_audio_dir/SWH-05-20110125 -iname "*.wav" > $dev_dir/wav.flist
find $aidatatang_audio_dir/SWH-05-20101112 -iname "*.wav" >> $dev_dir/wav.flist



# Transcriptions preparation
for dir in $train_dir $dev_dir $test_dir; do
  echo Preparing $dir transcriptions
  sed -e 's/\.wav//' $dir/wav.flist | awk -F '/' '{print $NF}' > $dir/utt.list
  sed -e 's/\.wav//' $dir/wav.flist | awk -F '/' '{i=NF-1;printf("%s %s\n",$NF,$i)}' > $dir/utt2spk_all
  paste -d' ' $dir/utt.list $dir/wav.flist > $dir/wav.scp_all
  utils/filter_scp.pl -f 1 $dir/utt.list $aidatatang_text > $dir/transcripts.txt
  awk '{print $1}' $dir/transcripts.txt > $dir/utt.list
  utils/filter_scp.pl -f 1 $dir/utt.list $dir/utt2spk_all | sort -u > $dir/utt2spk
  utils/filter_scp.pl -f 1 $dir/utt.list $dir/wav.scp_all | sort -u > $dir/wav.scp
  sort -u $dir/transcripts.txt > $dir/text
  utils/utt2spk_to_spk2utt.pl $dir/utt2spk > $dir/spk2utt
done

mkdir -p task0/data/train task0/data/truetest task0/data/test

for f in spk2utt utt2spk wav.scp text; do
  cp $train_dir/$f task0/data/train/$f || exit 1;
  cp $dev_dir/$f task0/data/truetest/$f || exit 1;
  cp $test_dir/$f task0/data/test/$f || exit 1;
done

echo "$0: data preparation succeeded"
exit 0;

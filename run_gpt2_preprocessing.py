#! /bin/bash

python preprocess_data.py \
       --input /home/zjlab/data/ShangjianTech_concat_txt/ShangjianTech_50000.json \
       --output-prefix /home/zjlab/data/ShangjianTech_concat_txt/gpt2_test \
       --vocab /home/zjlab/data/bpe_3w_new/vocab.json \
       --dataset-impl mmap \
       --tokenizer-type GPT2BPETokenizer \
       --append-eod \
       --workers 20
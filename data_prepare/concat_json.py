#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/4/23 10:50
# @Author  : jiaoxu
# @File    : concat_json.py
# @Software: PyCharm

"""
将众多txt文件整合为一个json文件，每行一段话，格式为：
{"text": "The quick brown fox", "title": "First Part"}
{"text": "jumps over the lazy dog", "title": "Second Part"}
参考 https://github.com/NVIDIA/Megatron-LM#data-preprocessing
"""
import json
import logging
import os
import datetime

txt_dir = "/home/zjlab/data/ShangjianTech_txt"
logging_dir = "/home/zjlab/log"
output_dir = "/home/zjlab/data/ShangjianTech_concat_txt"
output_text_file = "ShangjianTech_50000.json"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
c_time = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.FileHandler(os.path.join(logging_dir, 'concat_text_{}.log'.format(c_time)))
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info("Begin")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
with open(os.path.join(output_dir, output_text_file), 'w', encoding='utf8') as output_fh:
    for _i, text_file in enumerate(os.listdir(txt_dir)):
        if _i % 100 == 0:
            logger.info("Current processed NO. {} text file: {}".format(str(_i), text_file))
        with open(os.path.join(txt_dir, text_file), 'r', encoding='utf8') as input_fh:
            for line in input_fh:
                line = line.strip()
                if line:
                    output_js = {"title": text_file, "text": line}
                    json.dump(output_js, output_fh, ensure_ascii=False)
                    output_fh.write('\n')
logger.info("End")
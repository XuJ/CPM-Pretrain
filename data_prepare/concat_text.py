#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/4/22 17:09
# @Author  : jiaoxu
# @File    : concat_text.py
# @Software: PyCharm

"""
将众多txt文件整合为一个txt文件，每个txt文件以空行分隔
"""
import logging
import os
import datetime

txt_dir = "/home/zjlab/data/ShangjianTech_txt"
logging_dir = "/home/zjlab/log"
output_dir = "/home/zjlab/data/ShangjianTech_concat_txt"
output_text_file = "ShangjianTech_50000.txt"

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
                    output_fh.write(line)
                    output_fh.write("\n")
        output_fh.write("\n")
logger.info("End")
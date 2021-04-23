#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/4/16 16:06
# @Author  : jiaoxu
# @File    : pdf_to_text.py
# @Software: PyCharm

"""
将分布在各个文件夹中的pdf文件，通过pdfminer转化为txt文件
同时剔除长度过短句子，以及按照从后往前的顺序剔除字符直至遇到中文句末标点
"""

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import logging
import re
import os
import datetime

MIN_SENTENCE_LENGTH=5
# CHINESE_EOS = ["。", "？", "！", "”", "……", "）", "》", "】"]
CHINESE_EOS = ["。", "？", "！", "”", "……"]
pdf_dir = "/home/zjlab/data/ShangjianTech_unzip"
pdf_prefix = "sj_pdf"
txt_dir = "/home/zjlab/data/ShangjianTech_txt"
logging_dir = "/home/zjlab/log"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
c_time = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.FileHandler(os.path.join(logging_dir, 'data_prepare_{}.log'.format(c_time)))
handler.setFormatter(formatter)
logger.addHandler(handler)


def truncate_chinese_sentence(text):
    char_list = [c for c in text]
    char_list.reverse()
    end_loc = -1
    for loc, c in enumerate(char_list):
        if c in CHINESE_EOS:
            end_loc = loc
            break
    if end_loc == 0:
        return text
    elif end_loc == -1:
        return ""
    else:
        return text[:-end_loc]

def clean_text(text):
    text = text.strip()
    text = re.sub("\s+", " ", text)
    text = truncate_chinese_sentence(text)
    text_no_space = re.sub("\s", "", text)
    if text:
        if len(text_no_space) > MIN_SENTENCE_LENGTH:
            return True, text
    return False, text

for pdf_subfix in range(10):
    logger.info("#"* 25)
    print("#"* 25)
    pdf_subfix = str(pdf_subfix)
    folder_dir = "{}_{}".format(pdf_prefix, pdf_subfix)
    logger.info("Processing folder {}".format(folder_dir))
    print("Processing folder {}".format(folder_dir))
    for _h, pdf_file in enumerate(os.listdir(os.path.join(pdf_dir, folder_dir))):
        if pdf_file.endswith(".pdf"):
            file_name = pdf_file.split(".")[0]
            txt_file = "{}.txt".format(file_name)
            if _h % 100 == 0:
                print("Current processed {} files".format(str(_h)))
                logger.info("Current processed {} files".format(str(_h)))
            if os.path.exists(os.path.join(txt_dir, "{}_{}".format(folder_dir, txt_file))):
                continue
            else:
                try:
                    logger.info("Processing file {}".format(txt_file))
                    with open(os.path.join(txt_dir, "{}_{}".format(folder_dir, txt_file)), "w", encoding="utf8") as output_fh:
                        for i, page_layout in enumerate(extract_pages(os.path.join(pdf_dir, folder_dir, pdf_file))):
                            for j, element in enumerate(page_layout):
                                if isinstance(element, LTTextContainer):
                                    t = element.get_text()
                                    flag, t = clean_text(t)
                                    if flag:
                                        output_fh.write(t)
                                        output_fh.write("\n")
                except Exception as e:
                    logger.error("Error when processing file {}, error message： {}".format(os.path.join(pdf_dir, folder_dir, pdf_file), e))
                    os.remove(os.path.join(txt_dir, "{}_{}".format(folder_dir, txt_file)))

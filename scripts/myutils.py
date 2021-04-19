"""
common tools
"""
import shutil
import re
import os
import csv
import sys
from tqdm import tqdm

def open_csv(name, pmode="w"):
    """
    创建csv文件
    :param pmode: ["w", "a"]
    """
    return csv.writer(open("../csvs/{}.csv".format(name), mode=pmode, newline="",encoding="gb18030"), doublequote=False, escapechar="\\")

def remove_file(path):
    """
    删除指定文件
    :param path: 文件路径
    """
    try:
        os.remove(path)
    except:
        pass

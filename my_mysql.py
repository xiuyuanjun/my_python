#!/usr/bin/python3

import pymysql
import os
import tarfile
import time


db = pymysql.connect(host="192.168.1.187", port=53306, user="root", passwd="123456", db='mysql', charset='utf8')
cursor = db.cursor()
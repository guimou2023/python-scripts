#!/usr/local/bin/env python3
# -*- coding:utf-8 -*-
# __author__:"Howard"

import pymysql
import schedule
import datetime
import random
import string
import logging

# apt install python3-pip  libpcap-dev libpq-dev
# pip3 install pymysql schedule


config = {
          'host': '10.20.0.19',
          'port': 3306,
          'user': 'root',
          'password': '1234',
          'db': 'test',
          'charset': 'utf8',
          'cursorclass': pymysql.cursors.DictCursor,
          }


class SaveToSql(object):
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.cursor.execute("create database if not exists test")
        self.cursor.execute("drop table if exists testtable")
        self.cursor.execute("create table if not exists testtable(id int(4) primary key not null auto_increment,time char(33) not null,name char(33) not null,type char(33) not null,data char(33) not null);")

    # 生成随机数函数
    def random_str(self, randomlength=random.randint(1,10)):
        a = list(string.ascii_letters)
        random.shuffle(a)
        return ''.join(a[:randomlength])
    # 存储函数
    def save(self):
        try:
            sql = "insert into testtable(time, name, type, data) values('%s','%s', '%s', '%s')"% (datetime.datetime.now(),self.random_str(),self.random_str(),self.random_str())
            self.cursor.execute(sql)
            rs = self.cursor.rowcount
            """判断数据库表中数据所影响行数是否为1，
            如果不是的话就进行异常抛出"""
            if rs != 1:
                raise Exception("Error of data inserting.")
                self.conn.rollback()
            self.conn.commit()
        except Exception as e:
            logging.waring(e)
        else:
            logging.warning(sql)
        finally:
            pass

    def __del__(self):
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":
    conn = pymysql.connect(**config)
    save_obj = SaveToSql(conn)

    try:
        schedule.every(0.01).seconds.do(save_obj.save)
    except Exception as e:
        print('Error: %s' % e)

    while True:
        schedule.run_pending()
        # time.sleep(0.01)
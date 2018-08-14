#!/usr/local/bin/env python3
# -*- coding:utf-8 -*-
# __author__:"Howard"
import datetime
import logging
import string
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


logging.basicConfig(format='[%(asctime)s][%(name)s][%(module)s.%(lineno)d][%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)


def random_str(randomlength=random.randint(1, 10)):
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:randomlength])

e = create_engine("mysql+pymysql://root:1234@10.20.0.19/test",
                       encoding='utf-8',
                       echo=False,
                       pool_size=100,
                       pool_recycle=5,
                       pool_timeout=30,
                       pool_pre_ping=True,
                       max_overflow=0,
                  )


# Session_class = sessionmaker(bind=e)
# Session = Session_class()


c = e.connect()
c.execute("create database if not exists test")
c.execute("drop table if exists testtable")
c.execute("create table if not exists testtable(id int(4) primary key not null auto_increment,time char(33) not null,name char(33) not null,type char(33) not null,data char(33) not null);")


try:
    while True:
        sql = "insert into testtable(time, name, type, data) values('%s','%s', '%s', '%s')" % (datetime.datetime.now(), random_str(), random_str(),random_str())
        c.execute(sql)
        logging.debug(sql)
    c.close()
# except exc.DBAPIError:
#     if e.connection_invalidated:
#         print("Connection was invalidated!")
except Exception as e:
    logging.debug(e)


# after the invalidate event, a new connection # starts with a new Pool c = e.connect() c.execute("SELECT * FROM table")
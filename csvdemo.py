__author__ = 'shine'

#!/usr/bin/env python
#-*-  coding：UTF-8  -*-

import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from sqlalchemy.types import NVARCHAR, Float, Integer

# 连接设置 连接mysql 用户名test 密码123123 地址192.168.15.59：3306 database：python
engine =create_engine('mysql+pymysql://test:123123@192.168.15.59:3306/python')
# 建立连接
con = engine.connect()

df = pd.read_csv('highschool.csv', encoding='gbk',usecols=[ 0, 1, 2, 3, 4, 5] )

def map_types(df):
    dtypedict = {}
    for i, j in zip(df.columns, df.dtypes):
        if "object" in str(j):
            dtypedict.update({i: NVARCHAR(length=255)})
        if "float" in str(j):
            dtypedict.update({i: Float(precision=2, asdecimal=True)})
            if "int" in str(j):
                dtypedict.update({i: Integer()})
                return dtypedict

dtypedict = map_types(df)
# 通过dtype设置类型 为dict格式{“col_name”:type}
df.to_sql(name='test', con=con, if_exists='replace', index=False, dtype=dtypedict)












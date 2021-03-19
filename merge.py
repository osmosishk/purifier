import pandas as pd
import mysql.connector
import json
from pandas.io.json import json_normalize
from sqlalchemy import create_engine
import pymysql.cursors
import datetime

def connect():
  """ Connect to MySQL database """
  source = None

  try:
      source = pymysql.connect(host='35.220.139.166',
                                   user='tonyho',
                                   password='zanik5dbkr',
                                   database='osmosisdatatest',
                                   cursorclass=pymysql.cursors.DictCursor)

      if source:
          print('Connected to Source MySQL database')



  except Error as e:
    print(e)

def test():
    source = pymysql.connect(host='35.220.139.166',
                             user='tonyho',
                             password='zanik5dbkr',
                             database='osmosisdatatest',
                             cursorclass=pymysql.cursors.DictCursor)

    df = pd.read_sql_query(" SELECT * FROM management_case ", source)
    df['time'] =pd.to_timedelta(df['time'])

    print(df['time'].head(10))



def read():



  try:
      source = pymysql.connect(host='35.220.139.166',
                               user='tonyho',
                               password='zanik5dbkr',
                               database='osmosisdatatest',
                               cursorclass=pymysql.cursors.DictCursor)


      creds = {'usr': 'tonyho',
               'pwd': 'zanik5dbkr',
               'hst': '35.220.139.166',
               'prt': 3306,
               'dbn': 'osmosisdatatest1'}
      connstr = 'mysql+mysqlconnector://{usr}:{pwd}@{hst}:{prt}/{dbn}'
      engine = create_engine(connstr.format(**creds))

      #df = pd.read_sql_query(" SELECT * FROM auth_user ", source)
      #df.to_sql(con=engine, name='auth_user', if_exists='append', index=False)
      #print("Auth_user work!")

      #df = pd.read_sql_query(" SELECT * FROM authtoken_token ", source)
      #df.to_sql(con=engine, name='authtoken_token', if_exists='append', index=False)
      #print("authtoken_token!")

      #df = pd.read_sql_query(" SELECT * FROM OneToOne_customer ", source)
      #df.to_sql(con=engine, name='OneToOne_customer', if_exists='append', index=False)
      #print("Customer work!")

      #df = pd.read_sql_query(" SELECT * FROM management_product " , source)
      #df.to_sql(con=engine, name='management_product', if_exists='append',index=False)
      #print("Product work!")





      #df = pd.read_sql_query(" SELECT * FROM management_technician ", source)
      #df.to_sql(con=engine, name='management_technician', if_exists='append', index=False)
      #print("Technician work!")

      #df = pd.read_sql_query(" SELECT * FROM management_mainperiod ", source)
      #df.to_sql(con=engine, name='management_mainperiod', if_exists='append', index=False)
      #print("Main Period work!")

      #df = pd.read_sql_query(" SELECT * FROM management_filter ", source)
      #df.to_sql(con=engine, name='management_filter', if_exists='append', index=False)
      #print("Filter work!")




      #df = pd.read_sql_query(" SELECT * FROM management_case ", source , parse_dates=['time'])

      #df['time'] = pd.DataFrame({'time': pd.to_timedelta(df['time'])})

      #df['time'] = df['time'].astype('str')
      #df.replace({'NaT': None}, inplace=True)

      #df.to_sql(con=engine, name='management_case1', if_exists='append', index=False)
      #print("Case work!")

      df = pd.read_sql_query(" SELECT * FROM management_case_filters ", source)
      df.to_sql(con=engine, name='management_case_filters1', if_exists='append', index=False)
      print("Case Filter work!")

      df = pd.read_sql_query(" SELECT * FROM management_case_machines ", source)
      df.to_sql(con=engine, name='management_case_machines1', if_exists='append', index=False)
      print("Case Machine work!")

      df = pd.read_sql_query(" SELECT * FROM management_machine ", source)
      df.to_sql(con=engine, name='management_machine1', if_exists='append', index=False)
      print("Machine work!")

      df = pd.read_sql_query(" SELECT * FROM management_mainpack ", source)
      df.to_sql(con=engine, name='management_mainpack', if_exists='append', index=False)
      print("Mainpack work!")




  except Exception as e:
      print(e)





if __name__ == '__main__':
    connect()
    read()
    ###test()


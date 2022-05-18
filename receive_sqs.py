from re import I
import boto3
import os
import time
from time import strptime
import pymysql
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, DateTime, Integer

os.environ['AWS_PROFILE'] = "Profile1"
count = 0
sqs = boto3.client('sqs', region_name='ap-northeast-2')
queue_url = os.environ.get("queue_url")
name = os.environ.get("name")
password = os.environ.get("password")
end_point = os.environ.get("end_point")
database_name = os.environ.get("database_name")

# default value
lon,lat,drone_height,azimute=[37.5495,127.075,1.69,307.2]
delete_gandle = 0
engine = create_engine(f'mysql+pymysql://{name}:{password}@{end_point}/{database_name}')

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
Base = declarative_base()

def get_now(): 
    import time 
    now = time.time() 
    return now
i = get_now()

def set_default():
    global i
    i+=1
    return i

class INFO(Base):
    __tablename__ = "info"
    id = Column(Integer, primary_key=True)
    info_id = Column(Integer, primary_key=True, default=set_default)
    date = Column(DateTime)
    left_value = Column(Float)
    top_value = Column(Float)
    width_value = Column(Float)
    height_value = Column(Float)
    lon = Column(Float)
    lat = Column(Float)
    drone_height = Column(Float)
    azimuth = Column(Float)

def receive_message():
    global lon, lat, drone_height, azimute, delete_gandle

    # receive message
    response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All']
        )['Messages'][0]
    receiptHandle = response['ReceiptHandle']
    delete_gandle = response['ReceiptHandle']
    body = response['Body']

    value_data = body.split()
    if value_data[0] == 'Coor':
        lon,lat,drone_height,azimute=[*map(float, value_data[1:])]
    else:
        date = time_changer(body.split(" left")[0])
        left_value = value_data[6]
        top_value = value_data[8]
        width_value = value_data[10]
        height_value = value_data[12]
        insert_data(date, left_value, top_value, width_value, height_value, lon, lat, drone_height, azimute)

    return receiptHandle

def insert_data(date, left_value, top_value, width_value, height_value, lon, lat, drone_height, azimute):
    data = INFO(
        date=date,
        left_value=left_value,
        top_value=top_value,
        width_value=width_value,
        height_value=height_value,
        lon=lon,
        lat=lat,
        drone_height=drone_height,
        azimuth=azimute
    )

    session.add(data)
    session.commit()
    print(date, left_value, top_value, width_value, height_value, lon, lat, drone_height, azimute)


def time_changer(string):
    string = string.split()
    time = string[3].split(":")
    date = datetime.datetime(int(string[4]), strptime(string[1],'%b').tm_mon, 
            int(string[2]), int(time[0]), int(time[1]), int(time[2]))
    return date

# 3시간이상 메세지가 없으면 종료
while count<=3600 * 3:
    try:
        receiptHandle = receive_message()
        count=0
    except:
        time.sleep(1)
        count+=1

    finally:
        # delete message
        try:
            response = sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=delete_gandle
                        )
        except:
            pass
session.close()

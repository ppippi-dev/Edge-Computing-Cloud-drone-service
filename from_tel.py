import boto3
import os

os.environ['AWS_PROFILE'] = "Profile1"

sqs = boto3.client('sqs', region_name='ap-northeast-2')
queue_url = "https://sqs.ap-northeast-2.amazonaws.com/996145069080/from-edge"

def send_message(message):
    response = sqs.send_message(QueueUrl=queue_url,
                    MessageBody=message)
    print(response)

m = "Coor" + str("lon")+ str("lat")+ str("drone_height")+ str("azimute")
send_message("")


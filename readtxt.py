import boto3
import os
import requests

requests.get("https://sqs.ap-northeast-2.amazonaws.com/996145069080/from-edge", verify=False)
os.environ['AWS_PROFILE'] = "Profile1"

sqs = boto3.client('sqs', region_name='ap-northeast-2')
queue_url = "https://sqs.ap-northeast-2.amazonaws.com/996145069080/from-edge"

prev_line = -1

def send_message(message):
    global prev_line
    now = float(message.split()[6])

    if prev_line-1 < now < prev_line+1:
        pass
    else:
        response = sqs.send_message(QueueUrl=queue_url,
                    MessageBody=message)
        prev_line=now

c = 0
file = open("./label_outs.txt","r")
line = ""

while line != "App run successful\n" and c < 1200:
    line = file.readline().rstrip('\n')
    if len(line) > 1:
        if line[0] == 'D':
            try:
                send_message(line[2:])
            except:
                c+=1
                pass

file.close()

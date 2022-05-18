import boto3
import os

os.environ['AWS_PROFILE'] = "Profile1"

sqs = boto3.client('sqs', region_name='ap-northeast-2')
queue_url = "https://sqs.ap-northeast-2.amazonaws.com/996145069080/edge_data"

def send_message(message, prev_line):
    # 중복데이터 확인여부 필요, 중복데이터인 경우 전송 x
    if message == prev_line:
        pass
    else:
        response = sqs.send_message(QueueUrl=queue_url,
                    MessageBody=message)
        print(response)
        prev_line = message
    return prev_line
c = 0
file = open("./label_outs.txt","r")
line = ""

prev_line = ""
while line != "App run successful\n" and c < 10:
    line = file.readline().rstrip('\n')
    if len(line) > 1:
        if line[0] == 'D':
            prev_line = send_message(line[2:], prev_line)
            c+=1

file.close()

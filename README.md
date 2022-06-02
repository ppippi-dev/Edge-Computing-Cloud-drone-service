# Edge Computing 및 Cloud Computing을 이용한 인구 밀집도 분석 서비스

<br>

![](test1.gif)

## 앱서비스 

깃헙 레파지토리 : https://github.com/Sejong-Talk-With/Capstone

<br>

## 서비스 구성도

<img src="/service_stream.png">

드론을 통해 객체를 탐지하고 이를 엣지 컴퓨팅 및 클라우드 컴퓨팅을 이용하여 시각화하는 분석 서비스 

<br>

## 사용 환경

#### Edge Computing ( In Jetson Nano )
- Nvidia Jetpack 4.6.1
- Deepsteram SDK 6.0.1
- TLT를 통해 학습된 yolov4_cspdarknet53 모델
- Python boto3

<br>

#### Cloud Computing ( In AWS )
- AWS SQS
- AWS EC2
- AWS Auto scale
- AWS Application Load Balancer (ALB)
- AWS RDS (MySQL)
- Python boto3, sqlalchemy, pymysql


<br>

## tao-converter

```shell
./tao-converter -e yolov4_float32.engine -d 3,416,416 -t fp32 -k {nvidia-key} -p Input,1x3x416x416,4x3x416x416,16x3x416x416 -m 1 -b 1 yolov4_cspdarknet53_fp32_epoch_140.etlt -o BatchedNMS

./tao-converter -e yolov4_int8.engine -d 3,416,416 -t int8 -k {nvidia-key} -p Input,1x3x416x416,4x3x416x416,16x3x416x416 -m 1 -b 1 -c cal.bin yolov4_cspdarknet53_INT8_epoch_140.etlt -o BatchedNMS
```
Nvidia TLT를 통해 학습된 모델을 Deepstream SDK에 적용하기 위해서는 Tao-converter 과정이 필요합니다.
Nvidia에서 제공해주는 Tao-converter를 이용해 변환하는 과정입니다.

<br>

## Object Detection 성능

mAP(mean Average Precision): 0.32
FPS
- fp32 & non_tracking: 38
- fp32 & tracking: 25
- int8 & non_tracking: 38.4 (단, fp32보다 낮은 mAP를 보임)

<br>

## Cloud ( AWS SQS + AWS RDS(Mysql) )


#### Ubuntu Setup

```shell
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pip

#install boto3
pip3 install boto3

#install sqlalchemy
pip3 install sqlalchemy

#install pymysql
pip3 install pymysql
```

#### 환경변수 셋팅

- AWS IAM 자격 증명 셋팅
`.aws/credentials`

```ini
[Profile1]
aws_access_key_id=AWS_IAM_KEY
aws_secret_access_key=AWS_IAM_SECRET_KEY
```

- env 셋팅

```shell
export queue_url=sqs_url
export name=db_user_name
export password=db_password
export end_point=db_endpoint
export database_name=db_name
```
export 명령어 혹은 .bashrc 를 이용해서 환경변수 셋팅 진행

Python boto3를 통해 AWS로 데이터 송수신 및 RDS이용을 위해 정의했습니다.

<br>

#### Code 모음

[SQS - Send Message (From Jetson Nano to SQS)](https://github.com/wjdqlsdlsp/Deepstream-SDK-yolov4/blob/main/readtxt.py)

[SQS - Recive Message and Load Data (In AWS Ec2 and RDS)](https://github.com/wjdqlsdlsp/Deepstream-SDK-yolov4/blob/main/receive_sqs.py)

<br>


## 그 외

- Nvidia Deepstream에서 yolov4모델을 사용하기 위해 추가로 몇가지 설정해야함.
- Parser box를 yolov4에 맞게 변경 - [NVIDIA-AI-IOT 깃헙](https://github.com/NVIDIA-AI-IOT/deepstream_tao_apps)

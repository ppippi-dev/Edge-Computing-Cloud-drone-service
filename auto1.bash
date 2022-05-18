nohup deepstream-app -c Desktop/opt/nvidia/deepstream/deepstream-6.0/sources/objectDetector_Yolo/yolov4.txt > label_outs.txt &

python3 readtxt.py

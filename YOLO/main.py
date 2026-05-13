import cv2
import time
from ultralytics import YOLO
from counter_reader import read_counter_value   #计米器代码

#配置
MODEL_PATH = "best.pt"
VIDEO_SOURCE = 0
CONF_THRESHOLD = 0.5
READ_INTERVAL = 0.5   #每0.5秒读取一次计米器


#加载模型
model = YOLO(MODEL_PATH)

#打开摄像头
cap = cv2.VideoCapture(VIDEO_SOURCE)

if not cap.isOpened():
    print("摄像头打开失败")
    exit()

#计米器缓存变量
last_read_time = 0
current_meter = None

print("=== 系统启动 ===")

while True:
    ret, frame = cap.read()
    if not ret:
        print("读取视频失败")
        break

    #计米器定时更新
    current_time = time.time()
    if current_time - last_read_time > READ_INTERVAL:
        meter_raw = read_counter_value()

        if meter_raw is not None:
            current_meter = round(meter_raw / 100, 2)  #单位换算

        last_read_time = current_time


    # YOLO检测
    results = model(frame, verbose=False)

    for r in results:
        boxes = r.boxes

        if boxes is None or len(boxes) == 0:
            continue

        for box in boxes:
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])

            if conf < CONF_THRESHOLD:
                continue

            label = model.names[cls_id]

            # 画框可视化
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            #使用缓存米数
            print(f"检测到缺陷: {label} | 米数: {current_meter}")

    # 显示画面
    cv2.imshow("Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
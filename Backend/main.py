"""
AI验布机 - 后端主程序
Flask API + YOLO检测 + MJPEG视频流 + PyWebView桌面壳
"""
import sys
import os
import time
import threading
import numpy as np
import cv2
import json
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
import webview
from counter_reader import read_counter_value   #计米器代码

# ============================================================
# 配置
# ============================================================
MODEL_PATH = r"../AAAceshi/best.pt"
CAMERA_INDEX = 0  # USB摄像头索引，0通常是第一个
CONF_THRESHOLD = 0.5  # 置信度阈值
FRAME_WIDTH = 1280  # 采集分辨率宽
FRAME_HEIGHT = 720  # 采集分辨率高
FLASK_PORT = 5000

#新增
READ_INTERVAL = 0.5   # 计米器读取间隔
# ============================================================
# Flask应用
# ============================================================
app = Flask(__name__)
CORS(app)


# ============================================================
# YOLO检测引擎
# ============================================================
class DetectionEngine:
    def __init__(self, model_path, camera_index=0):
        self.model_path = model_path
        self.camera_index = camera_index
        self.model = None
        self.cap = None
        self.latest_frame = None  # 最新原始帧
        self.latest_annotated = None  # 最新标注帧（画了框的）
        self.latest_defects = []  # 最新检测到的缺陷列表
        self.running = False
        self.lock = threading.Lock()
        self.thread = None
        self.fps = 0
        self.total_defects_today = 0

        #新增
        # 计米器缓存
        self.current_meter = 0
        self.last_read_time = 0

    def start(self):
        """启动检测引擎"""
        from ultralytics import YOLO

        print(f"[检测引擎] 加载模型: {self.model_path}")
        self.model = YOLO(self.model_path)

        print(f"[检测引擎] 打开摄像头 #{self.camera_index}")
        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

        if not self.cap.isOpened():
            raise RuntimeError(f"无法打开摄像头 #{self.camera_index}")

        self.running = True
        self.thread = threading.Thread(target=self._detection_loop, daemon=True)
        self.thread.start()
        print("[检测引擎] 已启动")

    def stop(self):
        """停止检测引擎"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        if self.cap:
            self.cap.release()
        print("[检测引擎] 已停止")

    def _detection_loop(self):
        """检测主循环（在独立线程中运行）"""
        frame_count = 0
        fps_start = time.time()

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("[检测引擎] 读取帧失败")
                time.sleep(0.01)
                continue

            frame_count += 1
            #新增
            # 定时读取计米器
            current_time = time.time()

            if current_time - self.last_read_time > READ_INTERVAL:

                meter_raw = read_counter_value()

                if meter_raw is not None:
                    self.current_meter = round(meter_raw / 100, 2)

                self.last_read_time = current_time

            # FPS计算
            if time.time() - fps_start >= 1.0:
                self.fps = frame_count
                frame_count = 0
                fps_start = time.time()

            # YOLO检测
            results = self.model(frame, verbose=False)

            defects = []
            annotated = frame.copy()

            for r in results:
                boxes = r.boxes
                if boxes is None or len(boxes) == 0:
                    continue

                for box in boxes:
                    conf = float(box.conf[0])
                    cls_id = int(box.cls[0])

                    if conf < CONF_THRESHOLD:
                        continue

                    label = self.model.names[cls_id]
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    # 画框
                    cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(annotated, f"{label} {conf:.0%}",
                                (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                    # 记录缺陷
                    defects.append({
                        "type": label,
                        "confidence": round(conf * 100),
                        "meter": self.current_meter,
                        "x": round(x1 / frame.shape[1], 3),
                        "y": round(y1 / frame.shape[0], 3),
                        "width": round((x2 - x1) / frame.shape[1], 3),
                        "height": round((y2 - y1) / frame.shape[0], 3)
                    })

            # 更新最新结果
            with self.lock:
                self.latest_frame = frame
                self.latest_annotated = annotated
                self.latest_defects = defects

            if defects:
                self.total_defects_today += len(defects)

                for d in defects:
                    print(
                        f"[检测] 缺陷:{d['type']} "
                        f"| 置信度:{d['confidence']}% "
                        f"| 米数:{d['meter']} m"
                    )

    def get_stats(self):
        """获取当前统计信息"""
        with self.lock:
            return {
                "fps": self.fps,
                "total_defects_today": self.total_defects_today,
                "current_defects": len(self.latest_defects),
                "defects": self.latest_defects.copy(),
                "model_names": list(self.model.names.values()) if self.model else []
            }


# 全局检测引擎实例
engine = DetectionEngine(MODEL_PATH, CAMERA_INDEX)


# ============================================================
# Flask路由
# ============================================================

@app.route('/')
def index():
    """根路由"""
    return jsonify({
        "status": "running",
        "app": "AI验布机后端服务",
        "version": "1.0.0"
    })


@app.route('/video_feed')
def video_feed():
    """MJPEG视频流 - 前端用 <img> 标签拉流"""

    def generate():
        while True:
            with engine.lock:
                frame = engine.latest_annotated.copy() if engine.latest_annotated is not None else None

            if frame is None:
                # 还没帧，发送空白
                blank = cv2.imencode('.jpg',
                                     cv2.putText(
                                         cv2.zeros((480, 640, 3), dtype=cv2.uint8),
                                         "Waiting for camera...", (50, 240),
                                         cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2
                                     )
                                     )[1].tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + blank + b'\r\n')
            else:
                # JPEG压缩
                ret, jpeg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                if ret:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

            time.sleep(0.033)  # ~30fps

    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/api/stats')
def api_stats():
    """获取实时统计"""
    stats = engine.get_stats()
    return jsonify(stats)


@app.route('/api/defects')
def api_defects():
    """获取缺陷列表"""
    stats = engine.get_stats()
    return jsonify(stats["defects"])


@app.route('/api/config', methods=['GET', 'POST'])
def api_config():
    """获取/设置配置"""
    if request.method == 'POST':
        global CONF_THRESHOLD
        data = request.get_json()
        if data and 'confidence' in data:
            CONF_THRESHOLD = float(data['confidence']) / 100
            return jsonify({"status": "ok", "confidence": data['confidence']})
        return jsonify({"status": "error", "message": "缺少参数"}), 400

    return jsonify({
        "confidence": int(CONF_THRESHOLD * 100),
        "model_path": MODEL_PATH,
        "camera_index": CAMERA_INDEX
    })


# ============================================================
# 启动
# ============================================================
def start_flask():
    """在单独线程启动Flask"""
    print(f"[Flask] 启动服务 http://localhost:{FLASK_PORT}")
    app.run(host='127.0.0.1', port=FLASK_PORT, debug=False, threaded=True)


if __name__ == '__main__':
    # 1. 启动检测引擎
    engine.start()

    # 2. 启动Flask（单独线程）
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    # 3. 等Flask就绪
    time.sleep(1)
    print("[PyWebView] 启动桌面窗口")

    # 4. 启动PyWebView加载前端
    webview.create_window(
        title="AI布匹检测系统",
        url="http://localhost:5173/",
        width=1400,
        height=900,
        resizable=True
    )
    webview.start()

    # 5. 退出时清理
    engine.stop()
    print("[系统] 已退出")
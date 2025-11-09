# 0. ホストOS側で実行し、ユーザーコンテナにパッケージ追加
# docker exec -u root -it jupyter-admin bash
# apt-get update
# apt-get install -y libgl1 libglib2.0-0

# 1. YOLOv8 のインストール
print("\n# 1. YOLOv8 のインストール")
!pip install --quiet ultralytics opencv-python

# 2. 必要ライブラリとモデルの準備
print("\n# 2. 必要ライブラリとモデルの準備")
from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

model = YOLO("yolov8n.pt")  # 軽量版。精度重視なら yolov8s.pt などに変更

# 3. 入力画像の用意
print("\n# 3. 入力画像の用意")
# 例: オンライン画像をダウンロード (任意の URL を指定)
!wget -O sample.jpg https://ultralytics.com/images/bus.jpg
img = cv2.imread("sample.jpg")
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img_rgb)
plt.axis("off")

# 4. YOLO 推論とバウンディングボックス描画
print("\n# 4. YOLO 推論とバウンディングボックス描画")
results = model(img_rgb)
annotated = results[0].plot()  # 検出結果を矩形で描画

plt.figure(figsize=(10, 6))
plt.imshow(annotated)
plt.axis("off")
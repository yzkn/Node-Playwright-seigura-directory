# py -m venv myenv
# myenv\Scripts\activate
# pip install opencv-python


import numpy as np
import cv2
import os


# 日本語対応
# import numpy as np
# import cv2
def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None


# import numpy as np
# import cv2
# import os
def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


import os
import cv2


# 出力フォルダの作成
os.makedirs('faces', exist_ok=True)

# 顔検出用のHaar Cascade分類器を読み込み
frontalface_default = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
profileface = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')

# imagesフォルダ内の画像を処理
for filename in os.listdir('images'):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        img_path = os.path.join('images', filename)
        # img = cv2.imread(img_path)
        img = imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 顔検出
        frontalface_default_faces = frontalface_default.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        profileface_faces = profileface.detectMultiScale(gray)

        # 検出された顔を切り出して保存
        for i, (x, y, w, h) in enumerate(frontalface_default_faces):
            face_img = img[y:y+h, x:x+w]
            output_filename = f"frontalfacedefault_{i}_{filename}"
            output_path = os.path.join('faces', output_filename)
            # cv2.imwrite(output_path, face_img)
            imwrite(output_path, face_img)

        for i, (x, y, w, h) in enumerate(profileface_faces):
            face_img = img[y:y+h, x:x+w]
            output_filename = f"profileface_{i}_{filename}"
            output_path = os.path.join('faces', output_filename)
            # cv2.imwrite(output_path, face_img)
            imwrite(output_path, face_img)

print("顔画像の切り出しと保存が完了しました。")
import os
import cv2
from PIL import Image

# 変換対象のフォルダ
folder_path = '/Users/masaki/Desktop/5:28'

# 対象拡張子のリスト
target_extensions = ['.png', '.webp', '.gif']

# フォルダ内のファイル一覧を取得・ソート
files = sorted(os.listdir(folder_path))

for file_name in files:
    file_lower = file_name.lower()
    ext = os.path.splitext(file_lower)[1]

    if ext in target_extensions:
        file_path = os.path.join(folder_path, file_name)
        new_file_path = os.path.join(folder_path, os.path.splitext(file_name)[0] + '.jpg')

        try:
            if ext in ['.png', '.webp']:
                # OpenCVで読み込み＆JPGで保存
                image = cv2.imread(file_path)
                if image is not None:
                    cv2.imwrite(new_file_path, image)
                else:
                    print(f"OpenCVで読み込めませんでした: {file_name}")

            elif ext == '.gif':
                # PILで読み込み＆JPGで保存（RGB変換）
                with Image.open(file_path) as im:
                    rgb_im = im.convert('RGB')
                    rgb_im.save(new_file_path, 'JPEG')

            # 元のファイルを削除
            os.remove(file_path)
            print(f"{file_name} → JPG変換＆削除完了")

        except Exception as e:
            print(f"変換中にエラーが発生しました: {file_name}, エラー: {e}")

from flask import Flask, render_template, request, jsonify, send_from_directory
from PIL import Image, ImageDraw, ImageFont
import os
import datetime
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
FONT_PATH = "static/fonts/arial.ttf"  # 🔹 修正: Arialフォントのパスを指定

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_design', methods=['POST'])
def save_design():
    try:
        data = request.json

        # 🔹 Tシャツのベース画像を開く
        tshirt_path = 'static/tshirt_base.png'
        tshirt_image = Image.open(tshirt_path).convert("RGBA")

        # 🔹 アップロードされた画像を貼り付け
        if 'image' in data:
            image_path = os.path.join(UPLOAD_FOLDER, data['image']['filename'])
            uploaded_image = Image.open(image_path).convert("RGBA")
            width = data['image']['width']
            height = data['image']['height']
            x = data['image']['x']
            y = data['image']['y']
            uploaded_image = uploaded_image.resize((width, height))
            tshirt_image.paste(uploaded_image, (x, y), uploaded_image)

        # 🔹 テキストを描画
        if 'text' in data:
            text = data['text']['content']
            x = data['text']['x']
            y = data['text']['y']
            font_size = data['text']['fontSize']

            draw = ImageDraw.Draw(tshirt_image)

            # 🔹 修正: Arialフォントを適切なサイズでロード
            if not os.path.exists(FONT_PATH):
                return jsonify({"error": "フォントファイルが見つかりません"}), 500
            font = ImageFont.truetype(FONT_PATH, font_size)

            draw.text((x, y), text, fill="black", font=font)

        # 🔹 ウォーターマークを追加
        watermark_text = "SAMPLE"
        wm_font_size = 100
        wm_font = ImageFont.truetype(FONT_PATH, wm_font_size)
        wm_draw = ImageDraw.Draw(tshirt_image)
        wm_width, wm_height = wm_draw.textbbox((0, 0), watermark_text, font=wm_font)[2:]
        img_width, img_height = tshirt_image.size
        wm_x = (img_width - wm_width) // 2
        wm_y = (img_height - wm_height) // 2
        wm_draw.text((wm_x, wm_y), watermark_text, fill=(0, 0, 0, 128), font=wm_font)

        # 🔹 ファイル名をユニークにする
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{uuid.uuid4().hex}_{timestamp}.png"
        result_path = os.path.join(RESULT_FOLDER, filename)
        
        # 🔹 画像を保存
        tshirt_image.save(result_path)

        return jsonify({"result": f"/results/{filename}"})
    
    except Exception as e:
        return jsonify({"error": f"デザイン保存中のエラー: {str(e)}"}), 500

@app.route('/results/<filename>')
def get_result_image(filename):
    return send_from_directory(RESULT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)

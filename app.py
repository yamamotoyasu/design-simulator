from flask import Flask, render_template, request, jsonify, send_from_directory
from PIL import Image
import os
import datetime
import uuid
import base64
from io import BytesIO

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/confirm')
def confirm():
    return render_template('confirm.html')

@app.route('/save_design', methods=['POST'])
def save_design():
    try:
        data = request.json
        if "image" not in data:
            return jsonify({"error": "画像データがありません"}), 400

        # Base64で送られてきた画像をデコード
        image_data = data["image"].split(",")[1]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))

        # 画像を保存
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{uuid.uuid4().hex}_{timestamp}.png"
        result_path = os.path.join(RESULT_FOLDER, filename)
        image.save(result_path)

        return jsonify({"result": f"/results/{filename}"})
    except Exception as e:
        return jsonify({"error": f"デザイン保存中のエラー: {str(e)}"}), 500

@app.route('/results/<filename>')
def get_result_image(filename):
    return send_from_directory(RESULT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)

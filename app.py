from flask import Flask, render_template, request, jsonify, send_from_directory
from PIL import Image
from io import BytesIO
import base64
import os
import uuid
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PDF_FOLDER = 'pdfs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)

#トップページ
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_design', methods=['POST'])
def save_design():
    try:
        data = request.json
        if 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400

        # 画像データ（Base64）をデコード
        base64_data = data['image'].split(',')[1]
        image_data = base64.b64decode(base64_data)
        image = Image.open(BytesIO(image_data)).convert('RGB')

        # ファイル名生成
        unique_id = uuid.uuid4().hex
        image_path = os.path.join(UPLOAD_FOLDER, f'{unique_id}.png')
        pdf_path = os.path.join(PDF_FOLDER, f'{unique_id}.pdf')

        # 一時画像として保存
        image.save(image_path)

        # PDFとして保存（実寸サイズ：1500mm x 450mm）
        width_mm = 450
        height_mm = 1500
        width_pt = width_mm * mm
        height_pt = height_mm * mm

        c = canvas.Canvas(pdf_path, pagesize=(width_pt, height_pt))
        c.drawInlineImage(image_path, 0, 0, width=width_pt, height=height_pt)
        c.showPage()
        c.save()

        return jsonify({'message': 'PDF saved successfully', 'pdf_url': f'/pdfs/{unique_id}.pdf'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/pdfs/<filename>')
def get_pdf(filename):
    return send_from_directory(PDF_FOLDER, filename)


# 注文情報入力ページ
@app.route('/order')
def order():
    return render_template('order.html')

# 注文内容確認ページ
@app.route('/review', methods=['POST'])
def review():
    payment = request.form['payment']
    dantainame = request.form['dantainame']
    name = request.form['name']
    addressno = request.form['addressno']
    address = request.form['address']
    phone = request.form['phone']
    email = request.form['email']
    
    return render_template('review.html', payment=payment, dantainame=dantainame, name=name, addressno=addressno, address=address, phone=phone, email=email)

# 注文完了ページ（注文番号生成）
@app.route('/complete', methods=['POST'])
def complete():
    order_id = str(uuid.uuid4())[:8]  # ランダムな注文番号を生成
    return render_template('complete.html', order_id=order_id)



if __name__ == '__main__':
    app.run(debug=True)

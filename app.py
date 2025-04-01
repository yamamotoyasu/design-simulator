from flask import Flask, render_template, request, redirect, url_for
import uuid

app = Flask(__name__)

@app.route('/order', methods=['GET'])
def order():
    return render_template('order.html')

@app.route('/review', methods=['POST'])
def review():
    payment = request.form['payment']
    name = request.form['name']
    address = request.form['address']
    phone = request.form['phone']
    
    return render_template('review.html', payment=payment, name=name, address=address, phone=phone)

@app.route('/complete', methods=['POST'])
def complete():
    order_id = str(uuid.uuid4())[:8]  # ランダムな注文番号を生成
    return render_template('complete.html', order_id=order_id)

if __name__ == '__main__':
    app.run(debug=True)

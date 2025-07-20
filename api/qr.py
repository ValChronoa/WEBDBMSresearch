from flask import Blueprint, request, jsonify, send_file
import qrcode, io, base64, cv2, numpy as np

qr_bp = Blueprint('qr', __name__, url_prefix='/api/qr')

@qr_bp.route('/decode', methods=['POST'])
def decode():
    file = request.files['image']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img)
    return jsonify({'data': data or None})

@qr_bp.route('/generate/<lab>/<item_id>')
def generate(lab, item_id):
    import os
    base_url = os.getenv('https://webdbmsresearch.onrender.com', 'http://localhost:5000')
    url = f"{base_url}/user/status/{lab}/{item_id}"
    img = qrcode.make(url)
    buf = io.BytesIO()
    # qrcode.make returns a PIL.Image, so use save with correct param
    img.save(buf, 'PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')
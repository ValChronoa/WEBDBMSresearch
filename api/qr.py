from flask import Blueprint, request, jsonify, send_file
import qrcode, io, base64, cv2, numpy as np

bp = Blueprint("qr", __name__, url_prefix="/api/qr")

@bp.route("/decode", methods=["POST"])
def decode():
    file = request.files["image"]
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img)
    return jsonify({"data": data or None})

@bp.route("/generate/<lab>/<item_id>")
def generate(lab, item_id):
    url = f"https://webdbmsresearch.onrender.com/{lab}/{item_id}"
    img = qrcode.make(url)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")
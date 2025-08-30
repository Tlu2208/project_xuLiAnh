# app.py
# -----------------------------
# Hướng dẫn nhanh:
# 1) Tạo môi trường và cài đặt:
#    pip install flask opencv-python numpy
# 2) Chạy server:
#    python app.py
# 3) Mở trình duyệt: http://127.0.0.1:5000
# 4) Chọn ảnh bằng nút HTML -> server nhận file -> xử lý (grayscale/gamma) -> hiển thị & tải về.

from flask import Flask, request, render_template_string
import cv2
import numpy as np
import base64

app = Flask(__name__)

# -----------------------------
# HTML (Jinja2 template) – 1 file duy nhất, không cần thư mục templates
# -----------------------------
PAGE = 



def read_image_from_upload(file_storage):
    """Đọc ảnh từ request.files['image'] thành mảng BGR (OpenCV)."""
    file_bytes = np.frombuffer(file_storage.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    return img


def to_base64_png(img_bgr):
    """Mã hóa ảnh BGR (OpenCV) sang PNG base64 để nhúng vào HTML."""
    ok, buf = cv2.imencode('.png', img_bgr)
    if not ok:
        raise RuntimeError('Không thể mã hóa ảnh PNG')
    return base64.b64encode(buf.tobytes()).decode('utf-8')


def process_image(img_bgr, op='original', gamma=1.0):
    """Áp dụng thuật toán xử lý đơn giản theo tham số.
    - grayscale: chuyển xám (sau đó đổi về BGR để hiển thị nhất quán)
    - gamma: out = 255 * (in/255)^(1/gamma)
    """
    if op == 'grayscale':
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        out = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        return out

    if op == 'gamma':
        g = max(float(gamma), 1e-6)
        inv = 1.0 / g
        # Tính theo kênh, giữ BGR
        f = img_bgr.astype(np.float32) / 255.0
        f = np.power(f, inv)
        out = np.clip(f * 255.0, 0, 255).astype(np.uint8)
        return out

    # original
    return img_bgr


@app.route('/', methods=['GET'])
def index():
    return render_template_string(PAGE, input_b64=None, output_b64=None, op_label='')


@app.route('/process', methods=['POST'])
def process():
    if 'image' not in request.files:
        return 'Thiếu file ảnh', 400

    file = request.files['image']
    if file.filename == '':
        return 'Chưa chọn file', 400

    img = read_image_from_upload(file)
    if img is None:
        return 'Không đọc được ảnh (định dạng không hỗ trợ?)', 400

    op = request.form.get('op', 'original')
    gamma = float(request.form.get('gamma', '1'))

    out = process_image(img, op=op, gamma=gamma)

    # Mã hóa base64 để nhúng vào HTML
    input_b64 = to_base64_png(img)
    output_b64 = to_base64_png(out)

    label_map = {
        'original': 'Giữ nguyên',
        'grayscale': 'Grayscale',
        'gamma': f'Gamma (γ={gamma:.1f})'
    }

    return render_template_string(PAGE, input_b64=input_b64, output_b64=output_b64, op_label=label_map.get(op, op))


if __name__ == '__main__':
    app.run(debug=True)

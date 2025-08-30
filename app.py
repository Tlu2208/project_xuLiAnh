from flask import Flask, request, render_template
import cv2
import numpy as np
import base64 
import os

app = Flask(__name__, template_folder="interface", static_folder="interface", static_url_path="/")


#Chuyển ảnh từ dạng upload sang ảnh numpy Để xl trong OpenCV
def read_img_from_upload(file_storage):
    file_bytes = np.frombuffer(file_storage.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    return img

#Chuyển ảnh từ numpy sang base64 để nhúng vào html
def to_base64_img(imh_bgr):
    ok, buf = cv2.imencode('.png', imh_bgr)
    if not ok:
        raise RuntimeError('Không thể mã hóa ảnh PNG')
    return base64.b64encode(buf.tobytes()).decode('utf-8')


#CÁC HÀM THUẬT TOÁN BIẾN ĐỔI ẢNH
def convertGray(img_bgr):
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    out = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    return out

def convert_LogarithmOne(img, c):
    i = img.astype(float)
    return float(c) * cv2.log(1+i)

def convertByPowerLawOne(img, gamma, c):
    i = img.astype(float)
    return float(c)*pow(i,float(gamma))

def histogram(img):
    copy = img.copy()
    hist,_ = np.histogram(copy, bins = 256, range = (0, 256))
    pdf = hist/hist.sum()
    cdf =  np.cumsum(pdf)
    mapping = np.round(cdf * 255).astype(np.uint8)
    copy = copy.astype(np.uint8)
    equalized = mapping[copy]
    return equalized

def histogram_clahe(img):
    # img: ảnh grayscale
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    equalized = clahe.apply(img)
    return equalized

def sharpen_kernel(img):
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(img, -1, kernel)
    return sharpened

def processing_CLAHE_Log(gray, method = 'gamma'):
    #Chuyển ảnh sáng grayScale
    if gray.ndim == 3:  # ảnh màu
        gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    img_CLAHE = histogram_clahe(gray)
    result = convertByPowerLawOne(img_CLAHE, 0.7, 5)
    result = cv2.normalize(result, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    return result
    
def proccessing_lack_of_light(img):
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gamma = convertByPowerLawOne(img, 0.4, 7)
    result = histogram_clahe(img_gamma.astype(np.uint8))
    return result

def process_img(img_bgr, op, gamma = 0.7):
    if op == 'original':
        return img_bgr
    if op == 'grayscale':
        out = convertGray(img_bgr)
    elif op == 'log':
        gray = convertGray(img_bgr)
        out = convert_LogarithmOne(gray, 40)
    elif op == 'gamma':
        gray = convertGray(img_bgr)
        out = convertByPowerLawOne(gray, gamma, 40)
    elif op == 'histogram': 
        gray = convertGray(img_bgr)
        out = histogram(gray)
    elif op == 'clahe':
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        out = histogram_clahe(gray)
    elif op == 'anhYTe':
        out = processing_CLAHE_Log(img_bgr)
    elif op == 'anhKemSang':
        out = proccessing_lack_of_light(img_bgr)
    else:
        out = img_bgr

    if out.dtype != np.uint8:
        out = cv2.normalize(out, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    if out.ndim == 2:
        out = cv2.cvtColor(out, cv2.COLOR_GRAY2BGR)
    return out

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html', input_b64 = None,  output_b64= None, op_label='')

@app.route('/process', methods=['POST'])
def process():
    if 'image' not in request.files:
        return 'Thiếu file ảnh', 400
    file = request.files['image']
    if file.filename == '':
        return 'Chưa chọn file', 400
    img = read_img_from_upload(file)
    if img is None:
        return 'Không đọc được ảnh!', 400
    
    op = request.form.get('op', 'original')
    gamma = float(request.form.get('gamma', '1'))

    out = process_img(img, op = op, gamma= gamma)

    input_b64 = to_base64_img(img)
    output_b64 = to_base64_img(out)

    label_map = {
        'original':   'Giữ nguyên',
        'grayscale':  'Grayscale',
        'gamma':      f'Gamma (γ={gamma:.1f})',
        'log':        'Log transformation',
        'histogram':  'Cân bằng lược đồ (Histogram Equalization)',
        'clahe':      'CLAHE',
        'anhYTe':     'Xử lý ảnh y tế (CLAHE + Log)',
        'anhKemSang': 'Ảnh thiếu sáng (Low-light)'
    }

    return render_template('index.html', input_b64=input_b64, output_b64=output_b64, op_label=label_map.get(op, op))

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

    
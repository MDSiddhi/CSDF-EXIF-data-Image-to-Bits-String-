from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from PIL import Image
import exifread
import base64

app = Flask(__name__)
bootstrap = Bootstrap(app)

def get_exif_data(image_path):
    with open(image_path, 'rb') as image_file:
        tags = exifread.process_file(image_file)
        return tags

def image_to_bits(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        binary_data = ''.join(format(byte, '08b') for byte in encoded_string)
        return binary_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    filename = file.filename
    file.save(filename)
    exif_data = get_exif_data(filename)
    bits_string = image_to_bits(filename)
    return render_template('result.html', exif_data=exif_data, bits_string=bits_string)

if __name__ == '__main__':
    app.run(debug=True)

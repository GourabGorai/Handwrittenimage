from flask import Flask, request, render_template, redirect, url_for
from PIL import Image
import pandas as pd
import os
import numpy as np

app = Flask(__name__)

# Ensure the upload folder exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
CSV_FILE = 'D:\\ATOM\\ImageData.csv'

# Ensure the CSV file exists and create header if not present
if not os.path.isfile(CSV_FILE):
    df = pd.DataFrame(columns=[f'pixel_{i+1}' for i in range(1080*1080)] + ['actual_value'])
    df.to_csv(CSV_FILE, index=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files or 'text' not in request.form:
        return redirect(url_for('index'))

    file = request.files['image']
    text = request.form['text']

    if file.filename == '':
        return redirect(url_for('index'))

    img = Image.open(file)
    img = img.resize((1080, 1080))

    grayscale_img = img.convert('L')
    pixel_values = np.array(grayscale_img).flatten()

    # Normalize grayscale values to 0-16
    normalized_pixel_values = (pixel_values / 255 * 16).astype(int)

    new_row = {f'pixel_{i+1}': normalized_pixel_values[i] for i in range(1080*1080)}
    new_row['actual_value'] = text

    df = pd.DataFrame([new_row])
    df.to_csv(CSV_FILE, mode='a', header=False, index=False)

    num_columns = len(new_row)

    return render_template('view_columns.html', num_columns=num_columns)

if __name__ == '__main__':
    app.run(debug=True)

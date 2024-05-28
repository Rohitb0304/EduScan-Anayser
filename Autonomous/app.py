from flask import Flask, render_template, request, redirect, url_for, send_file, send_from_directory, flash
import os
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import json
import chardet

# Use Agg backend to avoid GUI issues in multi-threaded environments
plt.switch_backend('agg')

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flashing messages

# Specify the directory where uploaded files will be stored
UPLOAD_FOLDER = 'Data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return redirect(url_for('index'))
    
    file_names = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
    return render_template('index.html', file_names=file_names)

def convert_excel_to_csv(file_path):
    excel_df = pd.read_excel(file_path)
    csv_path = file_path.replace('.xlsx', '.csv')
    excel_df.to_csv(csv_path, index=False)
    return csv_path

@app.route('/view_chart/<chart_type>/<filename>', methods=['GET', 'POST'])
def view_chart(chart_type, filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    try:
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext == '.xlsx':
            file_path = convert_excel_to_csv(file_path)

        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
        encoding = result['encoding']
        
        df = pd.read_csv(file_path, encoding=encoding)
    except Exception as e:
        error_message = f"Failed to decode the file: {str(e)}"
        return render_template('error.html', error_message=error_message)
    
    pie_chart_labels = []
    pie_chart_data = []
    bar_chart_labels = []
    bar_chart_data = []

    if request.method == 'POST':
        selected_column = request.form.get('selected_column')
        if chart_type == 'pie':
            counts = df[selected_column].value_counts()
            pie_chart_labels = counts.index.tolist()
            pie_chart_data = counts.tolist()
        elif chart_type == 'bar':
            counts = df[selected_column].value_counts()
            bar_chart_labels = counts.index.tolist()
            bar_chart_data = counts.tolist()
    
    columns = df.columns.tolist()
    return render_template('view_chart.html', filename=filename, columns=columns, chart_type=chart_type, pie_chart_labels=json.dumps(pie_chart_labels), pie_chart_data=json.dumps(pie_chart_data), bar_chart_labels=json.dumps(bar_chart_labels), bar_chart_data=json.dumps(bar_chart_data))

@app.route('/download_chart/<filename>')
def download_chart(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/clear', methods=['POST'])
def clear_files():
    file_names = os.listdir(app.config['UPLOAD_FOLDER'])
    for file_name in file_names:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        os.remove(file_path)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
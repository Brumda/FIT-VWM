import os

from flask import Flask, render_template, request

import files_extraction
import lemmatization

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        how_much = request.form['query2']
        print(how_much)
        sorted_results, message = lemm.get_sorted(query, int(how_much) if how_much != '' else 50)
        return render_template('index.html', query=query, results=sorted_results, message=message)
    return render_template('index.html')


@app.route('/file/<path:file_name>')
def show_file_content(file_name):
    file_path = 'txt/' + file_name
    with open(file_path, 'r') as file:
        file_content = file.read()
    return render_template('file_content.html', file_content=file_content)


if __name__ == '__main__':
    if not os.path.exists('txt/'):
        files_extraction.FilesMagic().get_files()
    lemm = lemmatization.TextProcessor()
    app.run(debug=True)

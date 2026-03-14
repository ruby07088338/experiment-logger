from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)
FILE_NAME = 'titration_data.csv'

# アプリ起動時にCSVファイルがなければ作る（見出しは ml と pH）
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['volume', 'ph'])

@app.route('/')
def index():
    logs = []
    # CSVファイルからデータを読み込む
    with open(FILE_NAME, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            logs.append(row)
            
    # グラフがきれいに繋がるように、滴下量（volume）の小さい順に並べ替える
    logs.sort(key=lambda x: float(x['volume']))
    return render_template('index.html', logs=logs)

@app.route('/add', methods=['POST'])
def add_data():
    # 画面から送られてきた 滴下量(ml) と pH を受け取る
    volume = request.form.get('volume')
    ph = request.form.get('ph')
    
    if volume and ph:
        # CSVファイルに追記する
        with open(FILE_NAME, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([volume, ph])
            
    return redirect('/')

@app.route('/clear')
def clear_data():
    # データをすべて消してリセットする機能
    with open(FILE_NAME, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['volume', 'ph'])
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
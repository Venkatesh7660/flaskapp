import os
import sys
from datetime import timedelta, datetime

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.debug = True


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        file = request.files['file']
        file.save(secure_filename(file.filename))
        seconds, error_log = get_total_seconds(file.filename)
        if not error_log == '':
            is_error_log_visible = True
        else:
            is_error_log_visible = False
        os.remove(file.filename)
        return render_template("out.html", output=sec_to_hours(seconds), error_log=error_log, is_error_log_visible=is_error_log_visible)


def get_total_seconds(file_path):
    file = open(file_path, "r")
    seconds = 0
    i = 2
    error_log = ""
    first_lne = file.readline().lower()
    if not "time log:" in first_lne:
        print("Requires a valid time log")
        return
    for line in file:
        line = line.replace('-', " ")
        data = line.split()
        first = True
        flag = 0
        for words in data:
            try:
                if first:
                    t1 = datetime.strptime(words, "%I:%M%p")
                    first = False
                    flag = flag + 1
                else:
                    t2 = datetime.strptime(words, "%I:%M%p")
                    flag = flag + 1
                    if t1 <= t2:
                        diff = t2 - t1
                        seconds = seconds + diff.seconds
                    else:
                        diff = t2 + timedelta(days=1) - t1
                        seconds = seconds + diff.seconds
            except ValueError as e:
                pass
        if flag != 2:
            print('Format not found at %d' % i)
            error_log = error_log + 'Format not found at %d\n' % i
        i = i + 1
    return seconds,error_log


def sec_to_hours(seconds):
    a = str(seconds // 3600)
    b = str((seconds % 3600) // 60)
    c = str((seconds % 3600) % 60)
    d = "{} hours {} mins {} seconds".format(a, b, c)
    return d



if __name__ == '__main__':
    app.run()

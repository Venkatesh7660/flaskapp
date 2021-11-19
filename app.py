import os
import sys
from datetime import timedelta, datetime

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        file = request.files['file']
        file.save(secure_filename(file.filename))
        seconds, log = get_seconds_from_log_file(file.filename)
        if not log == '':
            shown = True
        else:
            shown = False
        os.remove(file.filename)
        return render_template("console.html", output=convert(seconds), log=log, shown=shown)


def get_seconds_from_log_file(file_path):
    file = open(file_path, "r")
    total_seconds = 0
    i = 2
    if not "time log:" in file.readline().lower():
        print("Text file should contain text as time log")
        return
    for each_line in file:
        each_line = each_line.replace('-', " ")
        word_array = each_line.split()
        first = True
        flag = 0
        log=''
        for words in word_array:
            try:
                if first:
                    start = datetime.strptime(words, "%I:%M%p")
                    first = False
                    flag = flag + 1
                else:
                    end = datetime.strptime(words, "%I:%M%p")
                    flag = flag + 1
                    if start <= end:
                        diff = end - start
                        total_seconds = total_seconds + diff.seconds
                    else:
                        diff = end + timedelta(days=1) - start
                        total_seconds = total_seconds + diff.seconds
            except ValueError as e:
                pass
        if flag != 2:
            print('Invalid time format at %d' % i)
            log=log+'Invalid time format at %d\n' % i
        i = i + 1
    return total_seconds,log


def convert(secs):
    mints, sec = divmod(secs, 60)
    hour, mints = divmod(mints, 60)
    return "%d hours %d minutes " % (hour, mints)


if __name__ == '__main__':
    app.run()

import os
import sys
from datetime import timedelta, datetime

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        seconds, error = get_total_seconds(f.filename)
        os.remove(f.filename)
        if not error == '':
            error_title = "The following errors are found in the file"
        else:
            error_title = ""
        return render_template("output.html", output=convert_to_hours(seconds), error=error, error_title=error_title)


def convert_to_hours(secs):
    mints, sec = divmod(secs, 60)
    hour, mints = divmod(mints, 60)
    return "%d hours %d minutes" % (hour, mints)


def get_total_seconds(file_path):
    file = open(file_path, "r")
    seconds = 0
    i = 2
    error = ''
    if not "time log:" in file.readline().lower():
        print("Time log should be present in first line")
        return
    for line in file:
        line = line.replace('-', " ")
        words = line.split()
        first = 0
        flag = 0
        for word in words:
            try:
                if first == 0:
                    start_time = datetime.strptime(word, "%I:%M%p")
                    first += 1
                    flag = flag + 1
                else:
                    end_time = datetime.strptime(word, "%I:%M%p")
                    flag = flag + 1
                    if start_time <= end_time:
                        diff = end_time - start_time
                        seconds = seconds + diff.seconds
                    else:
                        diff = end_time + timedelta(days=1) - start_time
                        seconds = seconds + diff.seconds
            except ValueError as e:
                pass

        if flag != 2:
            print('Format mismatch at line %d' % i)
            error = error + ('Format mismatch at line %d \n' % i)
        i = i + 1

    return seconds, error


if __name__ == '__main__':
    app.run()

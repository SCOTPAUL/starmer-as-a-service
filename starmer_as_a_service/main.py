from collections import defaultdict
import random
from flask import Flask, send_from_directory
from flask_restful import Resource, Api, abort, reqparse
from enum import Enum
import csv
from pathlib import Path



app = Flask(__name__, static_folder='../keiths')
api = Api(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


keiths = []

with open('../keiths/keiths.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            keiths.append((row[0], row[1], row[2]))
            line_count += 1


keiths_by_emotion = defaultdict(list)

for keith in keiths:
    keiths_by_emotion[keith[1]].append(keith[0])


class Keith(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('emotion', type=str, required=True, help='Emotion that you want your Keith to have')
        args = parser.parse_args()

        keiths = keiths_by_emotion[args['emotion']]

        if keiths:
            keith = random.choice(keiths_by_emotion[args['emotion']])
            return send_from_directory(app.static_folder, keith, max_age=0)
        else:
            abort(404, message=f"No Keiths found with emotion {args['emotion']}")


api.add_resource(Keith, '/keith/')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, abort, jsonify, request
from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin
import json
import get_ffn 
import uploadAO3


app = Flask(__name__, static_folder='./display/build', static_url_path='')
CORS(app)

@app.route('/api/ffn/', methods=['POST'])
@cross_origin()
def api():
    if request.method == 'POST':
        res = request.form['username']
        # print(res)
        dict = get_ffn.display_works(res)
        return dict



@app.route('/api/AO3Login/', methods=['POST'])
def login_AO3():
    if request.method == 'POST':
        user = {
            'name': request.form['username'],
            'word': request.form['password'],
        }
        meta = json.loads(request.form['meta'])
        return uploadAO3.upload(user, meta)

@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')


"""
@app.route('/api/content/', methods=['POST'])
@cross_origin()
def storyContent():
    print("HELLO!!")
    if request.method == 'POST':
        title = request.form['title']
        link = request.form['url']
        return get_ffn.get_work_content(title, link)

@app.route('/api/metadata/', methods=['POST'])
@cross_origin()
def meta():
    if request.method == 'POST':
        url = request.form['url']
        work = request.form['work']
        # print(res)
        metadata = get_ffn.scrape_story_metadata(work, url)
        return metadata


@app.route('/api/postChapter', methods=['POST'])
def post_chapter():
    if request.method == 'POST':
        work_url = request.form['newWorkUrl']
        chapter = request.form['chapter']
        return uploadAO3.upload_chapter(work_url, chapter)
    else:
        return 1
"""


if __name__ == "__main__":
    app.run()
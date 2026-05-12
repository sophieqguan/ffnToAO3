import json
import threading
import uuid
from flask import Flask, jsonify, request
from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin
import get_ffn
from work.work import Work
from account.ao3session import AO3Session
from util.util import validate_url, lprint


app = Flask(__name__, static_folder='./display/build', static_url_path='')
CORS(app)

_jobs = {}  # job_id -> {status, done, url?, error?}


@app.route('/api/ffn/', methods=['POST'])
@cross_origin()
def api():
    if request.method == 'POST':
        res = request.form['username']
        try:
            works = get_ffn.display_works(res)
            return works
        except Exception as e:
            print(e)
            return jsonify({})


@app.route('/api/AO3Login/', methods=['POST'])
def login_AO3():
    username = request.form['username']
    password = request.form['password']
    meta = json.loads(request.form['meta'])

    lprint(f'AO3Login: raw url = {meta.get("url")!r}')
    url = validate_url(meta['url'])
    lprint(f'AO3Login: validated url = {url!r}')

    if url is None:
        return jsonify({'error': 'Invalid fanfiction.net URL.'})

    job_id = str(uuid.uuid4())
    _jobs[job_id] = {'status': 'Starting...', 'done': False}

    def emit(msg):
        lprint(msg)
        _jobs[job_id]['status'] = msg

    def run():
        try:
            work = Work(url, status_callback=emit)
            work.retrieve_content()
            session = AO3Session(username, password, status_callback=emit)
            session.new_session()
            work_url = session.new_story(work)
            lprint(f'New work URL: {work_url}')
            _jobs[job_id]['url'] = work_url
        except Exception as e:
            lprint(f'AO3Login error: {e}')
            _jobs[job_id]['error'] = str(e)
        finally:
            _jobs[job_id]['done'] = True

    threading.Thread(target=run, daemon=True).start()
    return jsonify({'job_id': job_id})


@app.route('/api/status/<job_id>')
def job_status(job_id):
    job = _jobs.get(job_id)
    if not job:
        return jsonify({'error': 'Unknown job.', 'done': True})
    result = dict(job)
    if job['done']:
        del _jobs[job_id]
    return jsonify(result)


@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == "__main__":
    import os
    app.run(port=int(os.environ.get('PORT', 5001)), threaded=True)

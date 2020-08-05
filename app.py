# -*- coding:UTF-8 -*-

from flask import Flask
from flask import request, jsonify, abort
import action
import os
import traceback
import time


app = Flask(__name__)


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    try:
        if request.method == 'GET':
            json = request.json
            project_name = json.get("repository").get("name")
            token = request.headers.get('X-Gitlab-Token')
            if action.verify_token(project_name, token):
                return jsonify({'status': 'success'}), 200
            else:
                return jsonify({'status': 'bad token'}), 401

        elif request.method == 'POST':
            logger = action.init_logging()
            project_name = request.json.get("repository").get("name")
            # 进入到代码目录，拉取最新代码
            status = action.pull(request, logger)
            if status:
                return jsonify({'status': 'success'}), 200
            else:
                return jsonify({'status': 'git pull error'}), 503

        else:
            abort(400)

    except:
        # 程序出错时，写入日志
        time_code = time.strftime("%Y%m%d-%H%M%S")
        log = "{}/{}_error.log".format(os.path.dirname(__file__), time_code)
        traceback.print_exc(file=open(log, 'w+'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port='5000')


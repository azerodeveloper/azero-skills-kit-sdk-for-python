import importlib.util
import logging
import os
import json

from flask import Flask
from flask import request

ENCODING = "utf-8"
DATETIMEFORMAT="%Y-%m-%dT%H:%M:%SZ"

app=Flask(__name__)
#接口基本调试
@app.route('/', methods=['GET', 'POST'])
def index():
    return '<h1>启动成功</h1>'

#动态加载技能调用
@app.route('/skill/<name>',  methods=['GET', 'POST'])
def home(name):
    request_data_obj = json.loads(str(request.data, encoding="utf8"))
    request_data_obj["full_path"] = request.full_path
    request_data_obj["host_url"] = request.host_url
    logging.info("开始加载技能")
    try:
        path = os.path.abspath(os.path.dirname(__file__))
        file_path = path + '/skills/' + name + '/index.py'
        module_spec = importlib.util.spec_from_file_location(name, file_path)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        logging.info(dir(module))
        data = module.invoke_skill(app)
        logging.info("加载完成")
    except Exception as e:
        logging.error("加载出现异常：", e)
        logging.error(e)
    return data

if __name__ == '__main__':
    logging.info("启动成功")
    app.run(host='0.0.0.0', port='9930',debug=False, threaded=True)
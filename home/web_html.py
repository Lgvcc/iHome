# coding:utf-8
from flask import Blueprint
from flask import current_app

web_html = Blueprint('web_html', __name__)


@web_html.route("/<re(r'.*'):html_file_name>")
def get_html(html_file_name):
    """ 提供html文件 """
    if not html_file_name:
        html_file_name = '/index.html'
    if html_file_name != 'favicon.ico':
        html_file_name = 'html/' + html_file_name

    # send_static_file 会去static文件下找
    return current_app.send_static_file(html_file_name)

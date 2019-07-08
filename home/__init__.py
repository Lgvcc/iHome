# coding:utf-8
from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv
import os
import redis
from flask_session import Session
from flask_wtf import CSRFProtect
import logging
from logging.handlers import RotatingFileHandler

load_dotenv(find_dotenv())
envget = os.environ.get
REDIS_HOST = envget('REDIS_HOST')
REDIS_PORT = envget('REDIS_PORT')
REDIS_PASSWORD = envget('REDIS_PASSWORD')

db = SQLAlchemy()

redis_store = None

# 配置日志信息
# 设置日志的记录等级
logging.basicConfig(level=logging.INFO)
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
# 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日记录器
logging.getLogger().addHandler(file_log_handler)


def create_app(config_name):
    # 创建Flask对象
    app = Flask(__name__)

    # 根据配置模式的名字获得配置参数的类
    config_class = config_map[config_name]
    app.config.from_object(config_class)
    db.init_app(app)
    # 创建redis连接对象
    global redis_store
    redis_store = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

    # 利用flask-session 将session保存到redis中
    Session(app)

    # 为Flask补充csrf防护
    CSRFProtect(app)

    from .api_1_0 import api
    app.register_blueprint(api, url_prefix='/api/v1.0')
    return app



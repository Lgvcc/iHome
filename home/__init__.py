# coding:utf-8
from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv
import os
import redis
from flask_session import Session
from flask_wtf import CSRFProtect

load_dotenv(find_dotenv())
envget = os.environ.get
REDIS_HOST = envget('REDIS_HOST')
REDIS_PORT = envget('REDIS_PORT')
REDIS_PASSWORD = envget('REDIS_PASSWORD')

db = SQLAlchemy()

redis_store = None


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

    return app

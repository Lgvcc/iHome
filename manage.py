import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_session import Session
from flask_wtf import CSRFProtect
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

envget = os.environ.get

# 创建Flask对象
app = Flask(__name__)


class Config(object):
    """ 配置信息 """
    SECRET_KEY = 'hkfjdlajfladjfl'

    # 数据库
    SQLALCHEMY_DATABASE_URI = envget('Postgres_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis
    REDIS_HOST = envget('REDIS_HOST')
    REDIS_PORT = envget('REDIS_PORT')
    REDIS_PASSWORD = envget('REDIS_PASSWORD')

    # flask-session配置
    SESSION_TYPE = 'redis'  # 设置保存session的位置
    SESSION_USE_SIGNER = True  # 是否为cookie设置签名来保护数据不被更改
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)  # 设置连接哪个redis
    PERMANENT_SESSION_LIFETIME = 7200  # 设置session 有效期


app.config.from_object(Config)
db = SQLAlchemy(app)

# 创建redis连接对象
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, password=Config.REDIS_PASSWORD)

# 利用flask-session 将session保存到redis中
Session(app)

# 为Flask补充csrf防护
CSRFProtect(app)


@app.route('/index')
def index():
    return 'index page'


if __name__ == '__main__':
    app.run()

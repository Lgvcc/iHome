import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
import redis

envget = os.environ.get


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


class DevelopmentConfig(Config):
    """ 开发环境 """
    DEBUG = True


class ProductionConfig(Config):
    """ 生成环境 """
    DEBUG = False


# map代理映射关系
config_map = {
    'develop': DevelopmentConfig,
    'product': ProductionConfig
}

# coding:utf-8
from flask import current_app, jsonify, make_response

from . import api
from home.utils.captcha import captcha
from home import redis_store
from home.constants import REDIS_IMAGE_CODE_EXPIRE
from home.utils.response_code import RET


@api.route('/get_image_codes/<image_code_id>')
def get_image_code(image_code_id):
    """
    获取图片验证码
    :param image_code_id: 图片验证码编号
    :return: 图片验证码
    """

    # 业务逻辑处理
    # 生成图片验证码 name验证码名称 text图片真实值 image_code 图片验证码
    name, text, image_code = captcha.captcha.generate_captcha()
    # 将图片验证码编号和验证码真实值保存到redis中
    try:
        redis_store.setex('image_code_%s' % image_code_id, REDIS_IMAGE_CODE_EXPIRE, text)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, message='保存图片验证码失败')

    # 返回图片验证码
    resp = make_response(image_code)
    resp.headers['Content-Type'] = 'image/jpg'

    return resp


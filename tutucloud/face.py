# -*- coding: utf-8 -*-

import time
import hashlib
import requests

# API 服务地址
API_URL = 'https://api.tutucloud.com/v1/face/'


class Face(object):
	'''
	TUTUCLOUD 人脸 API 服务接口请求示例类

	Attributes:
		_params: 请求初始化参数
		_file:   需要 POST 的图片文件路径
	'''

	_params = {}

	_file = None

	def __init__(self, api_key, api_secret):
		self.api_secret = api_secret
		self._params['api_key'] = api_key

	def request(self, method, file='', url='', **params):
		'''
		API 请求方法

		Args:
			method: API 接口方法
			file: 图片文件
			url: 图片 URL
			params: API 接口参数

		Returns:
			API 返回 JSON 字符串

		Raise:
			requests.exceptions.RequestException
		'''

		if file:
			self._file = file
		elif url:
			self._params['img'] = url
		else:
			raise Error('img parameter is required')

		if len(params) == 0:
			payload = dict(self._params)
		else:
			payload = dict(self._params, **params)
		payload['t'] = int(time.time())
		payload['sign'] = self.signature(payload)

		# 如果有文件参数, 设置 requests.post files 参数
		files = None
		if self._file is not None:
			files = {'img': open(self._file, 'rb')}

		api_url = API_URL + method
		r = requests.post(api_url, data=payload, files=files)
		if r.status_code == 200:
			return r.json()
		else:
			return None

	def signature(self, params):
		'''
		获取 API 参数签名

		Args:
			params: 参数列表 dict

		Returns:
			对参数签名的结果字符串
		'''

		# 排序并转换参数名为小写
		params = [k.lower() + str(params[k]) for k in sorted(params)]
		# 加上私有 key
		signature = ''.join(params) + self.api_secret
		# 返回 md5 值
		md5 = hashlib.md5()
		md5.update(signature.encode('utf-8'))
		return md5.hexdigest()


class Error(Exception):
	pass

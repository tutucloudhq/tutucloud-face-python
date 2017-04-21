# -*- coding: utf-8 -*-
# TUTUCLOUD 人脸 API 请求示例

from tutucloud.face import *


def main():
	# 公有 key
	api_key = ''
	# 私有 key
	api_secret = ''

	try:
		# 初始化
		face = Face(api_key, api_secret)
		faces = face.request('analyze/detection', url='https://files.tusdk.com/img/faces/f-dd1.jpg')
		# faces = face.request('analyze/detection', file='test.webp')

		print(faces)

	except BaseException as e:
		print(e)

if __name__ == '__main__':
	main()

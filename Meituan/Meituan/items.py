

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeituanItem(scrapy.Item):
	# define the fields for your item here like:
	# 店铺名称
	title = scrapy.Field()
	# 店铺链接
	shop_link = scrapy.Field()
	# 店铺图片
	shop_img_link = scrapy.Field()
	# 店铺id
	id = scrapy.Field()
	# 店铺地址
	address = scrapy.Field()
	# 评分
	score = scrapy.Field()
	# 评论数量
	comment_num = scrapy.Field()
	# 人均价格
	price_avg = scrapy.Field()
	# 联系方式
	tel = scrapy.Field()
	# 营业时间
	open_time = scrapy.Field()
	# # 评论用户名
	# uname = scrapy.Field()
	# # 评论用户id
	# uid = scrapy.Field()
	# # 评论内容
	# comment = scrapy.Field()
	# 评论列表
	comment_list = scrapy.Field()
	pass




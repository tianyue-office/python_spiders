# Scrapy settings for Meituan project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Meituan'

SPIDER_MODULES = ['Meituan.spiders']
NEWSPIDER_MODULE = 'Meituan.spiders'

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_DBNAME = 'Meituan'
MONGO_COLNAME = 'meishi2'

# redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

'''
CRITICAL - 严重错误(critical)
ERROR - 一般错误(regular errors)
WARNING - 警告信息(warning messages)
INFO - 一般信息(informational messages)
DEBUG - 调试信息(debugging messages)
'''
# 是否启用log日志, 默认开启
# LOG_ENABLED = False
# log编码格式, 默认utf-8
# LOG_ENCODING = ''
# 默认: None，在当前目录里创建logging输出文件的文件名
LOG_FILE = 'meituan.log'
# 默认: 'DEBUG'，log的最低级别, 如果上线后, 最好将级别调成info
LOG_LEVEL = 'INFO'
# 默认: False 如果为 True，进程所有的标准输出(及错误)将会被重定向到log(如果LOG_FILE开启)中。例如，执行 print "hello" ，其将会在Scrapy log中显示
# LOG_STDOUT = True


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (WindowsNT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'

# -----------启用scrapyredis的重复过滤器模块，原有重复过滤器将停用
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# -----------启用scrapyredis中的调度器，该调度器具有与redis数据库交互的功能，原有的调度器将停用
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# -----------设置调度器请求队列保持，可以实现爬虫的断点续爬
SCHEDULER_PERSIST = True

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
	# 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	# 'Accept-Language': 'en',
	'Referer': 'http://hz.meituan.com/meishi/',
	'Accept': 'application/json',

}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'Meituan.middlewares.MeituanSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'Meituan.middlewares.MeituanDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
	'scrapy_redis.pipelines.RedisPipeline': 400,
	# 'Meituan.pipelines.MeituanPipeline': 300,
	# 'Meituan.pipelines.MeituanMongoPipeline': 301,
}

# ------------指定redis数据库地址
REDIS_URL = 'redis://127.0.0.1:6379'

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

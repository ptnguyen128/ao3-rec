# Scrapy settings for scrapeao3 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'scrapeao3'

SPIDER_MODULES = ['scrapeao3.scrapeao3.spiders']
NEWSPIDER_MODULE = 'scrapeao3.scrapeao3.spiders'

# Rotating proxy settings
ROTATING_PROXY_PAGE_RETRY_TIMES = 7
ROTATING_PROXY_BAN_POLICY = 'scrapeao3.scrapeao3.policy.BanPolicy'
# ROTATING_PROXY_LIST_PATH = 'scrapeao3/HTTPS-proxies.txt'
ROTATING_PROXY_LIST = [
    'https://ctljdccd:mewyb4m8zo9l@209.127.191.180:9279',
    'https://ctljdccd:mewyb4m8zo9l@45.142.28.83:8094',
    'https://ctljdccd:mewyb4m8zo9l@45.95.99.20:7580',
    'https://ctljdccd:mewyb4m8zo9l@45.136.231.43:7099',
    'https://ctljdccd:mewyb4m8zo9l@45.95.99.226:7786',
    'https://ctljdccd:mewyb4m8zo9l@45.95.96.187:8746',
    'https://ctljdccd:mewyb4m8zo9l@45.95.96.237:8796',
    'https://ctljdccd:mewyb4m8zo9l@193.8.127.189:9271',
    'https://ctljdccd:mewyb4m8zo9l@193.8.56.119:9183',
    'https://ctljdccd:mewyb4m8zo9l@45.94.47.108:8152',
    # # https
    # '64.235.204.107:3128', '98.12.195.129:443', '51.195.76.214:3128',
    # '181.143.94.42:999', '190.104.195.174:3001', '154.236.189.19:8080',
    # '54.36.250.193:80', '47.243.135.104:8080', '83.149.72.69:443',
    # '170.254.229.185:999', '85.25.196.76:5566', '103.206.8.114:8080'
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'scrapeao3 (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'scrapeao3.middlewares.Scrapeao3SpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapeao3.scrapeao3.middlewares.Scrapeao3DownloaderMiddleware': 543,
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'scrapeao3.scrapeao3.pipelines.Scrapeao3Pipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

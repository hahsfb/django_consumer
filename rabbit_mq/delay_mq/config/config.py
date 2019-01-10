"""
缓存信息配置
"""
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PWD = ''

"""
数据库的配置
"""
DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_USER = 'root'
DB_PWD = ''
DB_NAME = 'test'

"""
RabbitMQ
"""
MQ_HOST = '127.0.0.1'
MQ_PORT = 5672
MQ_USR = 'guest'
MQ_PWD = 'guest'
MQ_ORDER_TOPIC = 'admin_order'
CRON_TIMES = 3


# 延迟交换机
ORDER_EXCHANGE = 'order.exchange'
# 延迟队列
ORDER_QUEUE = 'order.queue'

# 延迟交换机
DELAY_EXCHANGE_5MIN = 'delay.shopping.exchange'
# 延迟队列
DELAY_QUEUE_5MIN = 'delay.shopping.queue'

# 消费交换机
EXCHANGE = 'cabinet.exchange'
# 消费队列
QUEUE = 'cabinet.queue'

# 定时消息交换机
TIMING_EXCHANGE = 'timing.exchange'

# 定时消息队列
TIMING_QUEUE = 'timing.queue'

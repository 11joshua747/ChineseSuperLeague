# config.py - 项目配置文件
# 这个文件用来安全存储数据库密码等敏感信息

# 数据库配置
db_config = {
    'host': 'localhost',      # 数据库服务器地址（本地电脑）
    'user': 'root',           # 数据库用户名（默认是root）
    'password': '123456',  # 你的MySQL密码（需要修改）
    'database': 'csl_prediction',  # 我们要创建的数据库名
    'charset': 'utf8mb4'      # 支持中文的字符编码
}

# 爬虫配置
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# 测试URL（用于练习）
test_url = "https://httpbin.org/get"

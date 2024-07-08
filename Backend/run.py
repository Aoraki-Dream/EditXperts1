from app.__init__ import create_app
import logging
from flask import Flask

app = Flask(__name__)

# 设置日志级别为DEBUG
app.logger.setLevel(logging.DEBUG)

# 创建app
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
    # app.run(debug=True)
    # context = ('path/to/cert.pem', 'path/to/key.pem')  # 指定证书和密钥文件的路径
    # app.run(host='0.0.0.0', port=443, ssl_context=context)

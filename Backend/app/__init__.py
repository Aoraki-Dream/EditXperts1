from flask import Flask
from .extensions import db, bcrypt, login_manager
from .controllers.user_controller import user_bp
from .controllers.polish_controller import polish_bp
# from .controllers.media_controller import media_bp
from flask_cors import CORS
from .controllers.document_controller import document_bp
from .controllers.template_controller import template_bp
from .models.document import DocumentModel


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # 打印配置以调试
    print(app.config["SQLALCHEMY_DATABASE_URI"])

    # 初始化扩展
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    CORS(app, supports_credentials=True)

    # 设置 user_loader
    @login_manager.user_loader
    def load_user(user_id):
        from .models.user import User

        return User.query.get(int(user_id))

    # 注册蓝图
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(polish_bp, url_prefix="/polish")
    # app.register_blueprint(media_bp, url_prefix="/media")
    app.register_blueprint(document_bp, url_prefix="/document")
    app.register_blueprint(template_bp, url_prefix="/template")
    # 创建索引
    DocumentModel.create_indexes()

    with app.app_context():
        db.create_all()  # 创建所有表
    return app

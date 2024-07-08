from flask import  request, jsonify,Blueprint
from uuid import uuid4
import os
from ..services.media_service import process_image
from ..middleware.authority import token_required

media_bp = Blueprint('media_bp', __name__)

@media_bp.route('/uploadimages', methods=['POST'])
@token_required
def uploadimages():
    """  
    上传并处理用户图像文件，返回图像中的文本信息。  
      
    接受一个图像文件作为POST请求的一部分，并处理该图像以提取其中的文本信息。  
    处理后的文本信息将以JSON格式返回。  
      
    :return: JSON 包含图像中的文本信息  
    """  
    username = request.form.get("username")
    img = request.files['file']
    picname = str(uuid4()) + os.path.splitext(img.filename)[1]  # 使用UUID生成唯一文件名
    texts = process_image(username, img, picname)

    response = {"texts": texts}
    return jsonify(response)
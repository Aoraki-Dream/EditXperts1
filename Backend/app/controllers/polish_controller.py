from flask import Blueprint, request, jsonify
import erniebot
from ..services.polish_service import polish_text, continue_text,summarize_text,translate_text
from ..middleware.authority import token_required

polish_bp = Blueprint('polish_bp', __name__)
erniebot.api_type = 'aistudio'

@polish_bp.route('/getpolish', methods=["GET", "POST"])
@token_required
def getpolish():
    """  
    处理用户提交的文本，并返回经过润色后的文本。  
  
    接收用户提交的文本内容，并尝试使用密码（尽管这里密码的用途可能不是最佳实践，通常我们会使用令牌或其他身份验证机制）和文本内容作为输入，  
    返回经过特定处理（如润色、优化等）后的文本结果。  
  
    :return: JSON 包含处理后的文本结果  
    """  
    print(request.form,request.headers)
    # 获取用户名
    username = request.form.get("username")
    # 获取用户的访问令牌
    password = request.form.get("password")
    # 获取用户提问内容
    quescont = request.form.get("cont")
    
    try:
        result = polish_text(password, quescont)
        return jsonify({'answer': result})
    except Exception as e:
        return str(e)

@polish_bp.route('/getcontinuation', methods=["GET", "POST"])
@token_required
def getcontinuation():
    """  
    根据用户提供的密钥和文本内容，继续生成或扩展文本。  
  
    接收用户提交的密钥和文本内容，使用这些输入来继续或扩展文本，并返回结果。  
  
    :return: JSON 包含扩展后的文本结果  
    """  
    # 获取用户名
    username = request.form.get("username")
    # 获取用户的访问令牌
    key = request.form.get("key")
    # 获取用户提问内容
    quescont = request.form.get("cont")
    
    try:
        result = continue_text(key, quescont)
        return jsonify({'answer': result})
    except Exception as e:
        return str(e)

@polish_bp.route('/getsummary', methods=["GET", "POST"])
@token_required
def getsummary():
    """  
    根据用户提供的密钥和文本内容，总结文本。   
  
    :return: JSON 包含扩展后的文本结果  
    """  
    # 获取用户名
    username = request.form.get("username")
    # 获取用户的访问令牌
    key = request.form.get("key")
    # 获取用户提问内容
    quescont = request.form.get("cont")
    
    try:
        result = summarize_text(key, quescont)
        return jsonify({'answer': result})
    except Exception as e:
        return str(e)

@polish_bp.route('/gettranslation', methods=["GET", "POST"])
@token_required
def gettranslation():
    """  
    根据用户提供的密钥和文本内容和目标语言，翻译文本。   
  
    :return: JSON 包含扩展后的文本结果  
    """  
    # 获取用户名
    username = request.form.get("username")
    # 获取用户的访问令牌
    key = request.form.get("key")
    # 获取用户提问内容
    quescont = request.form.get("cont")
    # 获取目标语言
    target_language = request.form.get("target_language")
    
    try:
        result = translate_text(key, quescont,target_language)
        return jsonify({'answer': result})
    except Exception as e:
        return str(e)

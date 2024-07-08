import erniebot

# 设置ErnieBot的API类型为'aistudio'
erniebot.api_type = 'aistudio'

def polish_text(access_token, content):
    """
    使用ErnieBot对给定的文本进行润色。

    :param access_token: str 访问ErnieBot API的令牌
    :param content: str 需要润色的文本内容
    :return: str 润色后的文本
    :raises: Exception 如果API调用失败则抛出异常
    """
    askcont = "帮我润色下面这段话:" + content
    erniebot.access_token = access_token
    
    try:
        response = erniebot.ChatCompletion.create(
            model='ernie-bot',
            messages=[{'role': 'user', 'content': askcont}],
        )
        return response['result']
    except Exception as e:
        raise e

def continue_text(access_token, content):
    """
    使用ErnieBot对给定的文本进行续写。

    :param access_token: str 访问ErnieBot API的令牌
    :param content: str 需要续写的文本内容
    :return: str 续写后的文本
    :raises: Exception 如果API调用失败则抛出异常
    """
    askcont = "帮我续写下面这段话:" + content
    erniebot.access_token = access_token
    
    try:
        response = erniebot.ChatCompletion.create(
            model='ernie-bot',
            messages=[{'role': 'user', 'content': askcont}],
        )
        return response['result']
    except Exception as e:
        raise e

def summarize_text(access_token, content):
    """
    使用ErnieBot对给定的文本进行总结。

    :param access_token: str 访问ErnieBot API的令牌
    :param content: str 需要总结的文本内容
    :return: str 总结后的文本
    :raises: Exception 如果API调用失败则抛出异常
    """
    askcont = "帮我总结下面这段话,给我摘要:" + content
    erniebot.access_token = access_token
    
    try:
        response = erniebot.ChatCompletion.create(
            model='ernie-bot',
            messages=[{'role': 'user', 'content': askcont}],
        )
        return response['result']
    except Exception as e:
        raise e

def translate_text(access_token, content,target_language):
    """
    使用ErnieBot对给定的文本进行翻译。

    :param access_token: str 访问ErnieBot API的令牌
    :param content: str 需要翻译的文本内容
    ：param target_language: str 目标语言
    :return: str 翻译后的文本
    :raises: Exception 如果API调用失败则抛出异常
    """
    askcont = "帮我翻译下面这段话为"+target_language+":" + content
    erniebot.access_token = access_token
    
    try:
        response = erniebot.ChatCompletion.create(
            model='ernie-bot',
            messages=[{'role': 'user', 'content': askcont}],
        )
        return response['result']
    except Exception as e:
        raise e

def process_text(access_token, content, task):
    """
    使用ErnieBot对给定的文本进行指定任务处理（如润色或续写）。

    :param access_token: str 访问ErnieBot API的令牌
    :param content: str 需要处理的文本内容
    :param task: str 任务类型（如 '润色' 或 '续写'）
    :return: str 处理后的文本
    :raises: Exception 如果API调用失败则抛出异常
    """
    askcont = f"帮我{task}下面这段话:" + content
    erniebot.access_token = access_token
    
    try:
        response = erniebot.ChatCompletion.create(
            model='ernie-bot',
            messages=[{'role': 'user', 'content': askcont}],
        )
        return response['result']
    except Exception as e:
        raise e

import os
from django.conf import settings
from langchain_openai import ChatOpenAI

def get_llm():
    """获取LLM实例，优先使用Django settings中的配置"""
    api_key = getattr(settings, 'DEEPSEEK_API_KEY', os.getenv("OPENAI_API_KEY", ""))
    api_base = getattr(settings, 'DEEPSEEK_API_URL', "https://api.deepseek.com")
    
    return ChatOpenAI(
        temperature=0,
        model="deepseek-chat",  # DeepSeek 官方模型名称
        openai_api_key=api_key,
        openai_api_base=api_base  # 不加 /v1
    )

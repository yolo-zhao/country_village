import logging
import os
from typing import TypedDict, Dict, Any, List, Optional, Union, Callable

logger = logging.getLogger(__name__)

# 尝试导入langgraph，如果不存在则创建备用实现
try:
    from langgraph.graph import StateGraph
    LANGGRAPH_AVAILABLE = True
    logger.info("成功导入LangGraph")
except ImportError:
    LANGGRAPH_AVAILABLE = False
    logger.warning("LangGraph未安装，将使用备用方案")

try:
    from config import get_llm
    llm = get_llm()
except ImportError:
    logger.error("无法导入config模块")
    llm = None

# ✅ 修复非法字符（如 emoji、系统符号）导致的 encode 错误
def safe_text(text: str) -> str:
    return text.encode("utf-8", "ignore").decode("utf-8")

# 状态结构
class QAState(TypedDict):
    input: str
    output: str
    next: str
    history: list[str]

# 判断是否需要"搜索"
def classify_question(state: QAState) -> QAState:
    if "今天" in state["input"] or "天气" in state["input"]:
        return {**state, "next": "search"}
    else:
        return {**state, "next": "direct"}

# 普通问答（记忆 + 编码安全）
def direct_answer(state: QAState) -> QAState:
    if not llm:
        return {**state, "output": "AI助手当前不可用，请稍后再试。", "history": state["history"]}
        
    conversation = "\n".join(safe_text(x) for x in state["history"] + [f"用户：{state['input']}"])
    try:
        response = llm.invoke(f"以下是与用户的对话，请回答最后一条提问：\n{conversation}")
        return {
            **state,
            "output": response.content,
            "history": state["history"] + [f"用户：{state['input']}", f"助手：{response.content}"]
        }
    except Exception as e:
        logger.error(f"调用LLM时出错: {str(e)}")
        return {
            **state, 
            "output": "处理您的请求时出现了问题，请稍后再试。",
            "history": state["history"] + [f"用户：{state['input']}", f"助手：处理您的请求时出现了问题，请稍后再试。"]
        }

# 模拟搜索后回答
def search_and_answer(state: QAState) -> QAState:
    if not llm:
        return {**state, "output": "AI助手当前不可用，请稍后再试。", "history": state["history"]}
        
    info = "模拟搜索结果：今天天气晴，气温22°C。"
    conversation = "\n".join(safe_text(x) for x in state["history"] + [f"用户：{state['input']}"])
    try:
        response = llm.invoke(f"结合'{info}'信息，回答以下对话内容：\n{conversation}")
        return {
            **state,
            "output": response.content,
            "history": state["history"] + [f"用户：{state['input']}", f"助手：{response.content}"]
        }
    except Exception as e:
        logger.error(f"调用LLM时出错: {str(e)}")
        return {
            **state, 
            "output": "处理您的请求时出现了问题，请稍后再试。",
            "history": state["history"] + [f"用户：{state['input']}", f"助手：处理您的请求时出现了问题，请稍后再试。"]
        }

# 备用流程实现（当langgraph不可用时使用）
class FallbackGraph:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("初始化备用流程图")
    
    def invoke(self, state: QAState) -> QAState:
        """简单实现的invoke方法，不使用langgraph"""
        self.logger.info(f"备用流程接收到请求: {state['input']}")
        try:
            # 简单的分类逻辑
            if "今天" in state["input"] or "天气" in state["input"]:
                return search_and_answer(state)
            else:
                return direct_answer(state)
        except Exception as e:
            self.logger.error(f"备用流程处理出错: {str(e)}")
            return {
                **state, 
                "output": "很抱歉，AI助手遇到了问题。请稍后再试。",
                "history": state["history"] + [f"用户：{state['input']}", "助手：很抱歉，AI助手遇到了问题。请稍后再试。"]
            }

# 构建 LangGraph 流程图
def build_graph():
    if not LANGGRAPH_AVAILABLE:
        logger.warning("使用备用流程图代替LangGraph")
        return FallbackGraph()
    
    # 如果LangGraph可用，使用原来的实现
    graph = StateGraph(QAState)
    graph.add_node("classify", classify_question)
    graph.add_node("direct", direct_answer)
    graph.add_node("search", search_and_answer)
    graph.set_entry_point("classify")

    graph.add_conditional_edges("classify", lambda state: state["next"], {
        "direct": "direct",
        "search": "search"
    })

    graph.set_finish_point("direct")
    graph.set_finish_point("search")

    return graph.compile()

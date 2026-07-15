import json

# --- 占位常量定义 (解决所有 ImportError) ---
def j(parts): return "\n".join(parts)

# 基础 Schema
output_schema_report_structure = {}
output_schema_first_search = {}
output_schema_first_summary = {}
output_schema_reflection = {}
output_schema_reflection_summary = {}
input_schema_report_formatting = {}

# 所有可能被引用的 Prompt 常量
SYSTEM_PROMPT_REPORT_STRUCTURE = "你是一位报告结构专家。"
SYSTEM_PROMPT_FIRST_SEARCH = "你是一位搜索专家。"
SYSTEM_PROMPT_FIRST_SUMMARY = "你是一位总结专家。"
SYSTEM_PROMPT_REFLECTION = "你是一位反思专家。"
SYSTEM_PROMPT_REFLECTION_SUMMARY = "你是一位反思总结专家。"
SYSTEM_PROMPT_REPORT_FORMATTING = "你是一位格式化专家。"
SYSTEM_PROMPT_TEMPLATE_SELECTION = "你是一位模版选择专家。"
SYSTEM_PROMPT_HTML_GENERATION = "你是一位 HTML 渲染专家。"
SYSTEM_PROMPT_CHAPTER_JSON = "你是一位章节 JSON 处理专家。"
SYSTEM_PROMPT_SUMMARY = "你是一位总结专家。"
SYSTEM_PROMPT_SEARCH = "你是一位搜索专家。"
SYSTEM_PROMPT_REFLECTION_NODE = "你是一位反思节点专家。"

# 舆情分析师专用
FINANCIAL_OPINION_OFFICER_PROMPT = """
# 角色
你是一名顶级金融舆情风控师与筹码博弈专家。

# 任务
请根据联网检索到的最新资讯，对 {topic} 展开解构。

# 输出格式
{{
  "summary": "一句话指出核心意图。",
  "textual_clues": {{"keywords": "关键词", "density": "密集度分析"}},
  "tactical_analysis": {{"method": "手段", "intent": "操盘意图"}},
  "trend_warning": {{"signal": "信号", "suggestion": "建议"}}
}}

# 输入数据
- 历史脉络: {history_data}
- 舆情原始数据: {search_results}
"""

# 确保 __init__.py 的批量导入可以访问这些变量
__all__ = [
    "SYSTEM_PROMPT_REPORT_STRUCTURE", "SYSTEM_PROMPT_FIRST_SEARCH", 
    "SYSTEM_PROMPT_FIRST_SUMMARY", "SYSTEM_PROMPT_REFLECTION", 
    "SYSTEM_PROMPT_REFLECTION_SUMMARY", "SYSTEM_PROMPT_REPORT_FORMATTING", 
    "SYSTEM_PROMPT_TEMPLATE_SELECTION", "SYSTEM_PROMPT_HTML_GENERATION", 
    "SYSTEM_PROMPT_CHAPTER_JSON", "SYSTEM_PROMPT_SUMMARY", 
    "SYSTEM_PROMPT_SEARCH", "SYSTEM_PROMPT_REFLECTION_NODE", 
    "FINANCIAL_OPINION_OFFICER_PROMPT"
]

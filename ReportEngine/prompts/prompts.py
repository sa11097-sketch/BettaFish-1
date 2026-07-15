import json

# 保持之前的 Schema 定义不变
output_schema_report_structure = {"type": "array", "items": {"type": "object", "properties": {"title": {"type": "string"}, "content": {"type": "string"}}}}
input_schema_first_search = {"type": "object", "properties": {"title": {"type": "string"}, "content": {"type": "string"}}}
output_schema_first_search = {"type": "object", "properties": {"search_query": {"type": "string"}, "search_tool": {"type": "string"}, "reasoning": {"type": "string"}}, "required": ["search_query", "search_tool", "reasoning"]}
input_schema_first_summary = {"type": "object", "properties": {"title": {"type": "string"}, "content": {"type": "string"}, "search_query": {"type": "string"}, "search_results": {"type": "array", "items": {"type": "string"}}}}
output_schema_first_summary = {"type": "object", "properties": {"paragraph_latest_state": {"type": "string"}}}
input_schema_reflection = {"type": "object", "properties": {"title": {"type": "string"}, "content": {"type": "string"}, "paragraph_latest_state": {"type": "string"}}}
output_schema_reflection = {"type": "object", "properties": {"search_query": {"type": "string"}, "search_tool": {"type": "string"}, "reasoning": {"type": "string"}}, "required": ["search_query", "search_tool", "reasoning"]}
input_schema_reflection_summary = {"type": "object", "properties": {"title": {"type": "string"}, "content": {"type": "string"}, "search_query": {"type": "string"}, "search_results": {"type": "array", "items": {"type": "string"}}, "paragraph_latest_state": {"type": "string"}}}
output_schema_reflection_summary = {"type": "object", "properties": {"updated_paragraph_latest_state": {"type": "string"}}}
input_schema_report_formatting = {"type": "array", "items": {"type": "object", "properties": {"title": {"type": "string"}, "paragraph_latest_state": {"type": "string"}}}}

# 这里定义一个极其简单的连接器
def j(parts): return "\n".join(parts)

SYSTEM_PROMPT_REPORT_STRUCTURE = j([
    "你是一位深度研究助手。给定一个查询，你需要规划报告结构。",
    "请按照以下JSON输出：",
    json.dumps(output_schema_report_structure, indent=2, ensure_ascii=False)
])

SYSTEM_PROMPT_FIRST_SEARCH = j([
    "你是一位深度研究助手。根据段落主题选择搜索工具。",
    "请按照以下JSON输出：",
    json.dumps(output_schema_first_search, indent=2, ensure_ascii=False)
])

# 核心：将长提示词拆解为列表，绝对规避三引号解释错误
SYSTEM_PROMPT_FIRST_SUMMARY = j([
    "你是一位专业的多媒体内容分析师。",
    "你的核心任务：创建信息丰富、多维度的综合分析段落。",
    "请严格按照以下JSON模式输出：",
    json.dumps(output_schema_first_summary, indent=2, ensure_ascii=False)
])

SYSTEM_PROMPT_REFLECTION = j([
    "你是一位深度研究助手，负责反思段落文本的当前状态。",
    "请按照以下JSON模式输出：",
    json.dumps(output_schema_reflection, indent=2, ensure_ascii=False)
])

SYSTEM_PROMPT_REFLECTION_SUMMARY = j([
    "你是一位深度研究助手，负责完善段落。",
    "请按照以下JSON模式输出：",
    json.dumps(output_schema_reflection_summary, indent=2, ensure_ascii=False)
])

SYSTEM_PROMPT_REPORT_FORMATTING = j([
    "你是一位资深的多媒体内容分析专家。",
    "你的使命：创建一份立体化、全景式的综合分析报告。",
    json.dumps(input_schema_report_formatting, indent=2, ensure_ascii=False)
])

# 金融舆情师 Prompt
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

# 补齐原项目缺失的模版选择提示词，确保程序不会再报导入错误
SYSTEM_PROMPT_TEMPLATE_SELECTION = """
你是一位模版选择专家，请根据用户的研究主题选择最合适的报告模版。
"""

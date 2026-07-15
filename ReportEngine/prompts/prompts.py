import json

# ===== JSON Schema 定义 =====
output_schema_report_structure = {"type": "array", "items": {"type": "object", "properties": {"title": {"type": "string"}, "content": {"type": "string"}}}}
output_schema_first_search = {"type": "object", "properties": {"search_query": {"type": "string"}, "search_tool": {"type": "string"}, "reasoning": {"type": "string"}}, "required": ["search_query", "search_tool", "reasoning"]}
output_schema_first_summary = {"type": "object", "properties": {"paragraph_latest_state": {"type": "string"}}}
output_schema_reflection = {"type": "object", "properties": {"search_query": {"type": "string"}, "search_tool": {"type": "string"}, "reasoning": {"type": "string"}}, "required": ["search_query", "search_tool", "reasoning"]}
output_schema_reflection_summary = {"type": "object", "properties": {"updated_paragraph_latest_state": {"type": "string"}}}
input_schema_report_formatting = {"type": "array", "items": {"type": "object", "properties": {"title": {"type": "string"}, "paragraph_latest_state": {"type": "string"}}}}

def j(parts): return "\n".join(parts)

# ===== 核心 Prompt 定义 =====
SYSTEM_PROMPT_REPORT_STRUCTURE = j(["你是一位深度研究助手。", json.dumps(output_schema_report_structure, indent=2, ensure_ascii=False)])
SYSTEM_PROMPT_FIRST_SEARCH = j(["你是一位搜索规划专家。", json.dumps(output_schema_first_search, indent=2, ensure_ascii=False)])
SYSTEM_PROMPT_FIRST_SUMMARY = j(["你是一位总结撰写专家。", json.dumps(output_schema_first_summary, indent=2, ensure_ascii=False)])
SYSTEM_PROMPT_REFLECTION = j(["你是一位反思优化专家。", json.dumps(output_schema_reflection, indent=2, ensure_ascii=False)])
SYSTEM_PROMPT_REFLECTION_SUMMARY = j(["你是一位总结反思专家。", json.dumps(output_schema_reflection_summary, indent=2, ensure_ascii=False)])
SYSTEM_PROMPT_REPORT_FORMATTING = j(["你是一位格式化专家。", json.dumps(input_schema_report_formatting, indent=2, ensure_ascii=False)])

# ===== 原项目依赖的额外补全 (防止 ImportError) =====
SYSTEM_PROMPT_TEMPLATE_SELECTION = "你是一位模版选择专家。"
SYSTEM_PROMPT_HTML_GENERATION = "你是一位 HTML 渲染专家。"
SYSTEM_PROMPT_SUMMARY = "你是一位总结专家。"
SYSTEM_PROMPT_SEARCH = "你是一位搜索专家。"
SYSTEM_PROMPT_REFLECTION_NODE = "你是一位反思节点专家。"

# ===== 专属金融舆情师 Prompt =====
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

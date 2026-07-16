# ReportEngine/prompts/prompts.py

# --- 系统提示词常量 ---
SYSTEM_PROMPT_TEMPLATE_SELECTION = "你是一位模版选择专家。"
SYSTEM_PROMPT_HTML_GENERATION = "你是一位 HTML 渲染专家。"
SYSTEM_PROMPT_CHAPTER_JSON = "你是一位章节 JSON 处理专家。"
SYSTEM_PROMPT_CHAPTER_JSON_REPAIR = "你是一位章节 JSON 修复专家。"
SYSTEM_PROMPT_CHAPTER_JSON_RECOVERY = "你是一位章节 JSON 恢复专家。"
SYSTEM_PROMPT_DOCUMENT_LAYOUT = "你是一位文档布局专家。"
SYSTEM_PROMPT_WORD_BUDGET = "你是一位字数控制专家。"
FINANCIAL_OPINION_OFFICER_PROMPT = "你是一位金融舆情分析专家。"

# --- 占位 Schema (防止 ImportError) ---
output_schema_template_selection = {"type": "object"}
input_schema_html_generation = {"type": "object"}
chapter_generation_input_schema = {"type": "object"}

# --- 占位函数 (防止 ImportError) ---
def build_chapter_user_prompt(title, content): return f"生成关于 {title} 的内容"
def build_chapter_repair_prompt(content): return f"修复内容: {content}"
def build_chapter_recovery_payload(data): return data
def build_document_layout_prompt(structure): return "布局结构设计"
def build_word_budget_prompt(target): return f"字数限制: {target}"

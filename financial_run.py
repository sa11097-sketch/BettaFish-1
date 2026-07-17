import os
import json
from datetime import datetime
# 导入 Google 官方最新 GenAI SDK
from google import genai
from google.genai import types
# 导入原项目自带的 HTML 渲染器
from ReportEngine.renderers.html_renderer import HTMLRenderer
# 导入你刚刚替换好的专属舆情师 Prompt
from ReportEngine.prompts.prompts import FINANCIAL_OPINION_OFFICER_PROMPT

def main():
    # 从环境变量读取追踪主题，默认值提供一个兜底
    topic = os.getenv("TRACK_TOPIC", "半导体板块核心股票")
    
    # 1. 初始化标准 Gemini 客户端（Actions 中会配置 GEMINI_API_KEY 环境变量）
    client = genai.Client()
    
    # 2. 读取历史滚动记忆
    history_file = "history_summary.json"
    history_data = []
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                history_data = json.load(f)[-5:]
        except Exception as e:
            print(f"⚠️ 读取历史记忆失败，将以空历史开始: {e}")
            
    # 3. 组装 Prompt，并明确要求输出 JSON 格式
    formatted_prompt = FINANCIAL_OPINION_OFFICER_PROMPT.format(
        topic=topic,
        history_data=json.dumps(history_data, ensure_ascii=False),
        search_results="请直接使用下方开启的 Google Search 联网工具获取的最新全网舆情与微观词汇。"
    )
    formatted_prompt += "\n\n请务必只输出标准的 JSON 格式结果，不要包含任何 markdown 代码块标记，不要包含额外解释。"
    
    print(f"🚀 [Gemini 舆情师] 正在通过 Google Search 联网并解构 [{topic}] 筹码博弈意图...")
    
    # 4. 配置 Gemini 核心参数：开启谷歌搜索，移除不兼容的 response_mime_type
    model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")
    
    config = types.GenerateContentConfig(
        tools=[{"google_search": {}}],
        temperature=0.2,
    )
    
    # 5. 调用 Gemini 模型
    response = client.models.generate_content(
        model=model_name,
        contents=formatted_prompt,
        config=config
    )
    
    # 6. 解析大模型返回的 JSON 数据
    try:
        # 去除可能出现的 markdown 标记
        raw_text = response.text.replace("```json", "").replace("```", "").strip()
        analysis_res = json.loads(raw_text)
    except Exception as e:
        print(f"❌ 解析大模型返回的 JSON 失败！原始响应为: {response.text}")
        raise e
    
    # 7. 更新历史时间宽度记忆
    today_str = datetime.now().strftime("%Y-%m-%d")
    history_data.append({"date": today_str, "summary": analysis_res.get("summary", "")})
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history_data, f, ensure_ascii=False, indent=2)
        
    # 8. 安全提取字段
    textual = analysis_res.get("textual_clues", {})
    tactical = analysis_res.get("tactical_analysis", {})
    warning = analysis_res.get("trend_warning", {})
    
    # 9. 适配原项目的 Document IR 格式
    document_ir = {
        "title": f"【庄家筹码博弈】{topic} 深度舆情解构报告",
        "meta": {"date": today_str, "author": "Gemini 专属舆情师"},
        "sections": [
            {
                "title": "👁️ 核心意图判词",
                "blocks": [{"type": "text", "content": analysis_res.get("summary", "暂无判词")}]
            },
            {
                "title": "🔍 微观字词特征与发酵密度",
                "blocks": [
                    {"type": "text", "content": f"**高频/引导性词汇与语气：** {textual.get('keywords', '未提取到特征词')}"},
                    {"type": "text", "content": f"**出现频率与密集度诊断：** {textual.get('density', '未提炼出密度特征')}"}
                ]
            },
            {
                "title": "⚔️ 操盘战术与手法拆解",
                "blocks": [
                    {"type": "text", "content": f"**市场行情诱导手法：** {tactical.get('method', '未识别出诱导手法')}"},
                    {"type": "text", "content": f"**背后核心操盘意图推导：** {tactical.get('intent', '未推导出核心意图')}"}
                ]
            },
            {
                "title": "⚠️ 情绪拐点与散户避险指南",
                "blocks": [
                    {"type": "callout", "style": "warning", "content": f"**舆情拐点预警：** {warning.get('signal', '未发出明确信号')}"},
                    {"type": "text", "content": f"**反向防御避险操作建议：** {warning.get('suggestion', '暂无操作建议')}"}
                ]
            }
        ]
    }
    
    # 10. 调用原项目 HTML 引擎渲染报告
    os.makedirs("final_reports", exist_ok=True)
    output_html_path = f"final_reports/financial_report_{today_str}.html"
    
    renderer = HTMLRenderer()
    renderer.render_to_file(document_ir, output_html_path)
    print(f"✨ 完美的交互式舆情密件已生成：{output_html_path}")

if __name__ == "__main__":
    main()

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
    
    # 2. 读取历史滚动记忆（时间宽度），为模型提供前几天的舆情脉络
    history_file = "history_summary.json"
    history_data = []
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                history_data = json.load(f)[-5:]  # 严格限制最近5天，防止 Token 膨胀
        except Exception as e:
            print(f"⚠️ 读取历史记忆失败，将以空历史开始: {e}")
            
    # 3. 组装并注入 Prompt 
    # 因为 Gemini 拥有原生的“谷歌搜索落地（Search Grounding）”能力，
    # 我们直接指示它将联网搜索结果与历史记忆进行交叉比对
    formatted_prompt = FINANCIAL_OPINION_OFFICER_PROMPT.format(
        topic=topic,
        history_data=json.dumps(history_data, ensure_ascii=False),
        search_results="请直接使用下方开启的 Google Search 联网工具获取的最新全网舆情与微观词汇。"
    )
    
    print(f"🚀 [Gemini 舆情师] 正在通过 Google Search 联网并解构 [{topic}] 筹码博弈意图...")
    
    # 4. 配置 Gemini 核心参数：强制 JSON 返回 + 开启原生谷歌搜索
    model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")
    
    config = types.GenerateContentConfig(
        tools=[{"google_search": {}}],  # 激活原生谷歌搜索工具
        response_mime_type="application/json",  # 强制要求返回合法的 JSON 字符串
        temperature=0.2,  # 降低随机性，使风控判词更严谨
    )
    
    # 5. 调用 Gemini 模型
    response = client.models.generate_content(
        model=model_name,
        contents=formatted_prompt,
        config=config
    )
    
    # 6. 解析大模型返回的 JSON 数据
    try:
        analysis_res = json.loads(response.text)
    except Exception as e:
        print(f"❌ 解析大模型返回的 JSON 失败！原始响应为: {response.text}")
        raise e
    
    # 7. 更新历史时间宽度记忆，供明天跑批时参考
    today_str = datetime.now().strftime("%Y-%m-%d")
    history_data.append({"date": today_str, "summary": analysis_res.get("summary", "")})
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history_data, f, ensure_ascii=False, indent=2)
        
    # 8. 安全提取字段（使用 .get 防止大模型偶尔漏写 Key 导致脚本崩溃）
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
                    {"type": "text", "content": f"**高频/引导性词汇与语气：** {textual.get('keywords_and_phrases', '未提取到特征词')}"},
                    {"type": "text", "content": f"**出现频率与密集度诊断：** {textual.get('frequency_and_density', '未提炼出密度特征')}"}
                ]
            },
            {
                "title": "⚔️ 操盘战术与手法拆解",
                "blocks": [
                    {"type": "text", "content": f"**市场行情诱导手法：** {tactical.get('market_influence_method', '未识别出诱导手法')}"},
                    {"type": "text", "content": f"**背后核心操盘意图推导：** {tactical.get('manipulation_intent', '未推导出核心意图')}"}
                ]
            },
            {
                "title": "⚠️ 情绪拐点与散户避险指南",
                "blocks": [
                    {"type": "callout", "style": "warning", "content": f"**舆情拐点预警：** {warning.get('signal_type', '未发出明确信号')}"},
                    {"type": "text", "content": f"**反向防御避险操作建议：** {warning.get('actionable_suggestion', '暂无操作建议')}"}
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

import os
import json
from datetime import datetime
from google import genai
from google.genai import types
from ReportEngine.renderers.html_renderer import HTMLRenderer
from ReportEngine.prompts.prompts import FINANCIAL_OPINION_OFFICER_PROMPT

def main():
    topic = os.getenv("TRACK_TOPIC", "半导体板块核心股票")
    client = genai.Client()
    
    # 1. 历史记忆读取
    history_file = "history_summary.json"
    history_data = []
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                history_data = json.load(f)[-5:]
        except:
            pass
            
    # 2. 组装 Prompt
    formatted_prompt = FINANCIAL_OPINION_OFFICER_PROMPT.format(
        topic=topic,
        history_data=json.dumps(history_data, ensure_ascii=False),
        search_results="请使用 Google Search 工具获取最新舆情。"
    )
    formatted_prompt += "\n\n请严格以纯 JSON 格式输出，不要包含 markdown 标记。"
    
    print(f"🚀 [Gemini 舆情师] 正在解构 [{topic}]...")
    
    # 3. API 调用
    config = types.GenerateContentConfig(tools=[{"google_search": {}}], temperature=0.2)
    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL_NAME", "gemini-2.0-flash"),
        contents=formatted_prompt,
        config=config
    )
    
    # 4. 解析结果
    try:
        raw_text = response.text.replace("```json", "").replace("```", "").strip()
        analysis_res = json.loads(raw_text)
    except Exception as e:
        print(f"❌ JSON 解析失败: {response.text}")
        raise e
    
    # 5. 存储历史
    today_str = datetime.now().strftime("%Y-%m-%d")
    history_data.append({"date": today_str, "summary": analysis_res.get("summary", "")})
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history_data, f, ensure_ascii=False, indent=2)
        
    # 6. 生成报告内容
    document_ir = {
        "title": f"【筹码博弈】{topic} 深度舆情报告",
        "sections": [
            {"title": "核心意图", "blocks": [{"type": "text", "content": analysis_res.get("summary", "无")}]},
            {"title": "微观特征", "blocks": [{"type": "text", "content": f"{analysis_res.get('textual_clues', {})}"}]},
            {"title": "战术拆解", "blocks": [{"type": "text", "content": f"{analysis_res.get('tactical_analysis', {})}"}]},
            {"title": "风险预警", "blocks": [{"type": "text", "content": f"{analysis_res.get('trend_warning', {})}"}]}
        ]
    }
    
    # 7. 手动生成 HTML (绕过任何未知的渲染器 API)
    os.makedirs("final_reports", exist_ok=True)
    output_html_path = f"final_reports/financial_report_{today_str}.html"
    
    html_template = f"<html><body><h1>{document_ir['title']}</h1>"
    for sec in document_ir['sections']:
        html_template += f"<h2>{sec['title']}</h2><p>{sec['blocks'][0]['content']}</p>"
    html_template += "</body></html>"
    
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_template)
        
    print(f"✨ 报告已生成: {output_html_path}")

if __name__ == "__main__":
    main()

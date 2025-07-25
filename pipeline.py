# summarize.py
import os
import datetime
import pandas as pd
from jinja2 import Template
from weasyprint import HTML
from sentence_transformers import SentenceTransformer
from openai import OpenAI

# --- OpenAI GPT 요약 함수 (v1 SDK 방식) ---
def summarize_text_with_openai(text, api_key, model="gpt-3.5-turbo", max_tokens=300):
    client = OpenAI(api_key=api_key)
    prompt = f"다음 문서를 한국어로 간결하게 요약해줘:\n\n{text[:2000]}"
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()

# --- SentenceTransformer 모델 (GPU 사용 가능) ---
def get_embedding_model(model_name='all-MiniLM-L6-v2'):
    return SentenceTransformer(model_name)

# --- HTML + PDF 리포트 자동 생성 ---
def generate_html_report(docs, summaries, output_path="cluster_report.html"):
    df = pd.DataFrame(docs)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html_template = """
    <html>
    <head>
        <meta charset="utf-8">
        <title>문서 클러스터링 리포트</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; background: #f4f4f4; }
            .cluster { margin-bottom: 40px; background: #fff; padding: 15px; border-left: 5px solid #4CAF50; }
            h2 { margin-top: 0; }
        </style>
    </head>
    <body>
        <h1>📄 문서 클러스터링 리포트</h1>
        <div>생성일시: {{ timestamp }}</div>
        {% for cluster_id in clusters %}
        <div class="cluster">
            <h2>🔹 클러스터 {{ cluster_id }}</h2>
            <p><strong>요약:</strong> {{ summaries[cluster_id] }}</p>
            <ul>
            {% for doc in docs[cluster_id] %}
                <li><strong>{{ doc['file'] | basename }}</strong><br>
                {{ doc['summary'] }}</li>
            {% endfor %}
            </ul>
        </div>
        {% endfor %}
    </body>
    </html>
    """

    cluster_docs = {
        cluster_id: df[df["cluster"] == cluster_id].to_dict("records")
        for cluster_id in sorted(df["cluster"].unique())
    }

    template = Template(html_template)
    html_content = template.render(
        timestamp=timestamp,
        clusters=cluster_docs.keys(),
        summaries=summaries,
        docs=cluster_docs,
        basename=os.path.basename,
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ HTML 리포트 저장 완료: {output_path}")

    HTML(output_path).write_pdf(output_path.replace(".html", ".pdf"))
    print(f"📄 PDF 리포트 생성 완료: {output_path.replace('.html', '.pdf')}")

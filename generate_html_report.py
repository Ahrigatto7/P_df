import pandas as pd

def generate_html_report(csv_path="clustered_output.csv", html_path="cluster_report.html"):
    df = pd.read_csv(csv_path)

    html = ["<html><head><meta charset='utf-8'><title>문서 클러스터링 결과</title></head><body>"]
    html.append("<h1>📊 문서 클러스터링 결과 리포트</h1>")

    for cluster_id in sorted(df['cluster'].unique()):
        html.append(f"<h2>📁 Cluster {cluster_id}</h2><ul>")
        for _, row in df[df['cluster'] == cluster_id].iterrows():
            html.append(f"<li><b>{row['filename']}</b><br><pre>{row['content'][:300]}...</pre></li>")
        html.append("</ul><hr>")

    html.append("</body></html>")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html))

    print(f"✅ HTML 리포트 생성 완료: {html_path}")

if __name__ == "__main__":
    generate_html_report()

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

# 把 html_pages 换成你自己存放 .html 文件的目录
HTML_DIR = "html_pages"

@app.on_event("startup")
def ensure_html_dir():
    if not os.path.isdir(HTML_DIR):
        os.makedirs(HTML_DIR)

@app.get("/", response_class=HTMLResponse)
def index():
    """
    列出目录下所有 HTML 文件的链接
    """
    files = sorted([f for f in os.listdir(HTML_DIR) if f.endswith(".html")])
    if not files:
        return "<html><body><h3>目录中没有找到任何 .html 文件。</h3></body></html>"
    links = "\n".join(
        f"<li><a href='/page/{fname[:-5]}'>{fname}</a></li>"
        for fname in files
    )
    return f"""
    <html>
      <body>
        <h1>可访问的页面列表</h1>
        <ul>
          {links}
        </ul>
      </body>
    </html>
    """

@app.get("/page/{name}", response_class=HTMLResponse)
def render_page(name: str):
    """
    根据文件名读取 HTML 并返回
    """
    filename = f"{name}.html"
    path = os.path.join(HTML_DIR, filename)
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="页面未找到")
    # 读取原始 HTML
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # 简单包裹：你也可以在这里加 header/footer
    return f"""
    <html>
      <head>
        <meta charset="utf-8"/>
        <title>{name}</title>
      </head>
      <body>
        {content}
      </body>
    </html>
    """

# 启动方式： uvicorn main:app --reload --host 0.0.0.0 --port 8000

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8011)
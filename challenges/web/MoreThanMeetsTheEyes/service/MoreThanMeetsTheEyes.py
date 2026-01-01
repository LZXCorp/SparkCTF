from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Challenge setup
page_item= 3
total = 5000
flag_item = 4777
FLAG = "SPARK{scraping_through_the_scraps}"

@app.route("/")
def index():
    return '''
        <h1>Welcome!</h1>
        <p>Start browsing items at <a href="/items?page=1">/items?page=1</a></p>
        <p>Tip: There are 5000 items<p>
    '''

@app.route("/items")
def items():
    page = int(request.args.get("page", 1))
    start = (page - 1) * page_item
    end = min(start + page_item, total)

    items_html = ""

    for i in range(start, end):
        # Normal items
        items_html += f"""
        <div class="card" data-id="{i}" {'data-load="/api/hidden-data"' if i == flag_item else ''}>
        <div class="meta">#{i}</div>
        <h3>Product #{i}</h3>
        <p>High-quality goods available for immediate purchase. Explore similar items and recommendations.</p>
        <div class="small">SKU: {100000 + i}</div>
        </div>
        """


        # Inject JS for FLAG_ITEM only
        if i == flag_item:
            items_html += f"""
            <script>

                fetch('/api/hidden-data?id={i}')
                  .then(res => res.text())

                  }});
            </script>
            """

    next_link = f'<a href="/items?page={page + 1}">Next Page →</a>' if end < total else ""

    html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Product Catalog — Page {page}</title>
        <style>
        :root{{
        --bg:#f4f6f8;
        --card:#ffffff;
        --muted:#55607a;
        --accent:#1976d2;
        --radius:10px;
        --gap:16px;
        --pad:18px;
        font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial;
        }}
        html,body{{height:100%}}
        body {{
        margin:0;
        background:var(--bg);
        color:#222;
        padding:28px;
        -webkit-font-smoothing:antialiased;
        }}
        .container{{max-width:980px;margin:0 auto}}
        .header{{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:18px}}
        .title{{font-size:20px;font-weight:700}}
        .toolbar{{display:flex;gap:8px}}
        .btn{{background:#fff;border:1px solid rgba(0,0,0,0.06);padding:8px 12px;border-radius:8px;text-decoration:none;color:inherit;font-weight:600}}
        .btn.primary{{background:linear-gradient(90deg,var(--accent),#06b6d4);color:#fff;border:0;box-shadow:0 6px 18px rgba(25,118,210,0.12)}}
        .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:var(--gap)}}
        .card{{background:var(--card);padding:var(--pad);border-radius:var(--radius);box-shadow:0 6px 18px rgba(16,24,40,0.06);position:relative;overflow:hidden;transition:transform .18s,box-shadow .18s}}
        .card:hover{{transform:translateY(-6px);box-shadow:0 18px 40px rgba(16,24,40,0.12)}}
        .meta{{display:inline-block;background:rgba(25,118,210,0.08);color:var(--accent);padding:6px 8px;border-radius:8px;font-weight:700;font-size:12px;margin-bottom:8px}}
        .card h3{{margin:0 0 8px 0;font-size:16px}}
        .card p{{margin:0;color:var(--muted);font-size:14px;line-height:1.4}}
        .small{{font-size:11px;color:transparent;user-select:none}}
        .pager{{display:flex;justify-content:space-between;align-items:center;margin-top:18px}}
        .link{{color:var(--accent);text-decoration:none;font-weight:600}}
        footer{{margin-top:36px;color:var(--muted);font-size:13px;text-align:center}}
        @media (max-width:600px){{body{{padding:14px}}.header{{flex-direction:column;align-items:flex-start}}}}
        </style>
        </head>
        <body>
        <div class="container">
            <div class="header">
            <div>
                <div class="title">Catalog</div>
            </div>
            <div class="toolbar">
                <a class="btn" href="/">Home</a>
                <a class="btn primary" href="/items?page=1">Browse</a>
            </div>
            </div>

            <main>
            <section class="grid">
                {items_html}
            </section>

            <div class="pager">
                {f'<a class="link" href="/items?page={page + 1}">Next Page →</a>' if (page * page_item) < total else ""}
                <div class="small">Page {page}</div>
            </div>
            </main>

            <footer>© 2025 Example Store</footer>
        </div>

        </body>
        </html>
        """

    return render_template_string(html)

@app.route("/api/hidden-data")
def hidden_data():
    item_id = request.args.get("id", type=int)

    if item_id == flag_item:
        step = 'Your close! You have discovered this hidden API call. Now get the flag!'
        return step

    if item_id == 2119:
        return FLAG

    return "Nothing here. Keep Trying :)", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=24680)

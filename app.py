from flask import Flask, render_template_string, request, jsonify, Response
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

# --- [ إعدادات AL-QAYSAR VIP ] ---
STORE_NAME = "ELITE APPS"
MY_WALLET = "TKBk4KVrtp1qEaWNiZUZyxM3GtfSppffxE"
LOG_FILE = "verified_orders.log"
VIP_WORDS = ['mod', 'premium', 'vip', 'unlocked', 'cheat', 'hack', 'mega', 'pro', 'menu']

if not os.path.exists(LOG_FILE):
    open(LOG_FILE, "a").close()

def fetch_massive_data():
    apps_pool = []
    # قائمة الأهداف الشاملة لسحب الملايين
    targets = [
        "https://apkmody.io/trending",
        "https://apkmody.io/games",
        "https://apkmody.io/apps",
        "https://apkmody.io/games/action",
        "https://apkmody.io/games/strategy",
        "https://apkmody.io/games/simulation",
        "https://apkmody.io/apps/tools",
        "https://apkmody.io/apps/entertainment"
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    for url in targets:
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                items = soup.select('div.flex-item')
                for item in items:
                    title_el = item.find('h3')
                    if title_el:
                        title = title_el.text.strip()
                        # تصحيح روابط الصور لضمان ظهورها
                        img_el = item.find('img')
                        img = img_el.get('src', '') if img_el else 'https://placehold.co/90'
                        if img.startswith('//'): img = 'https:' + img
                        
                        link = item.find('a')['href'] if item.find('a') else '#'
                        if not link.startswith('http'): link = "https://apkmody.io" + link
                        
                        is_v = any(w in title.lower() for w in VIP_WORDS)
                        apps_pool.append({'name': title, 'img': img, 'url': link, 'vip': is_v})
        except: continue
    return apps_pool

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ name }} | المتجر العالمي</title>
    <style>
        body { font-family: -apple-system, system-ui, sans-serif; background: #f4f6f8; margin: 0; padding-bottom: 80px; }
        header { background: #fff; padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 1px 10px rgba(0,0,0,0.05); position: sticky; top: 0; z-index: 1000; }
        .logo { font-size: 22px; font-weight: 800; color: #01875f; }
        .search-box { margin: 15px; background: #fff; border-radius: 14px; padding: 12px 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
        .search-box input { border: none; width: 100%; outline: none; font-size: 16px; background: transparent; }
        .section-title { padding: 15px 15px 5px; font-weight: bold; font-size: 18px; }
        .app-scroller { display: flex; overflow-x: auto; padding: 10px 15px; gap: 15px; scrollbar-width: none; }
        .app-scroller::-webkit-scrollbar { display: none; }
        .app-card { background: #fff; min-width: 135px; max-width: 135px; padding: 15px; border-radius: 22px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.03); border: 1px solid #f0f0f0; }
        .app-card img { width: 90px; height: 90px; border-radius: 22px; object-fit: cover; }
        .app-name { font-size: 13px; font-weight: 600; height: 36px; overflow: hidden; margin-top: 10px; }
        .tag-vip { color: #d93025; font-size: 10px; font-weight: bold; border: 1px solid #d93025; padding: 2px 5px; border-radius: 5px; margin-top: 5px; display: inline-block; }
        .modal { display: none; position: fixed; z-index: 2000; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.75); backdrop-filter: blur(6px); }
        .modal-content { background: #fff; margin: 15% auto; padding: 30px; width: 85%; max-width: 380px; border-radius: 28px; text-align: center; }
        .wallet-area { background: #f8f9fa; padding: 15px; border-radius: 15px; font-size: 11px; word-break: break-all; margin: 15px 0; border: 2px dashed #01875f; position: relative; }
        .copy-btn { background: #01875f; color: #fff; padding: 4px 10px; border-radius: 8px; font-size: 10px; position: absolute; top: -12px; left: 15px; }
        .nav-bar { position: fixed; bottom: 0; width: 100%; background: #fff; display: flex; justify-content: space-around; padding: 15px 0; border-top: 1px solid #eee; }
        .nav-link { text-decoration: none; color: #5f6368; font-size: 13px; font-weight: bold; }
    </style>
</head>
<body>
    <header><div class="logo">{{ name }}</div></header>
    <div class="search-box"><input type="text" id="searchInput" placeholder="ابحث في آلاف التطبيقات..." onkeyup="filter()"></div>

    <div class="section-title">إصدارات VIP المميزة 💎</div>
    <div class="app-scroller">
        {% for app in apps if app.vip %}
        <div class="app-card" onclick="openPayment('{{ app.name }}', '{{ app.url }}')">
            <img src="{{ app.img }}" onerror="this.src='https://placehold.co/90'">
            <div class="app-name">{{ app.name }}</div>
            <span class="tag-vip">تفعيل VIP (5$)</span>
        </div>
        {% endfor %}
    </div>

    <div class="section-title">تطبيقات مهكرة مجاناً 🔥</div>
    <div class="app-scroller">
        {% for app in apps if not app.vip %}
        <div class="app-card" onclick="startDirectDownload('{{ app.url }}')">
            <img src="{{ app.img }}" onerror="this.src='https://placehold.co/90'">
            <div class="app-name">{{ app.name }}</div>
            <span style="color:#5f6368; font-size:10px;">تحميل مجاني آمن</span>
        </div>
        {% endfor %}
    </div>

    <div id="paymentModal" class="modal">
        <div class="modal-content">
            <h3 id="appTitle"></h3>
            <div style="font-size:28px; font-weight:900; color:#01875f;">5.00 USDT</div>
            <div class="wallet-area">
                <span class="copy-btn" onclick="copyAddress()">نسخ العنوان</span>
                <span id="walletAddr">{{ wallet }}</span>
            </div>
            <input type="text" id="txIdInput" style="width:100%; padding:15px; border-radius:12px; border:1px solid #ddd; margin-bottom:15px; text-align:center;" placeholder="الصق كود TxID هنا">
            <button onclick="handleVerify()" style="background:#01875f; color:white; border:none; padding:16px; width:100%; border-radius:14px; font-weight:bold;">تحقق وتفعيل</button>
            <p onclick="closeModal()" style="margin-top:15px; color:gray; cursor:pointer;">إلغاء</p>
        </div>
    </div>

    <div class="nav-bar">
        <a href="/" class="nav-link" style="color:#01875f;">🏠 الرئيسية</a>
        <a href="https://t.me/HGLKJRL" target="_blank" class="nav-link">👑 المدير</a>
    </div>

    <script>
        let currentLink = "";
        function openPayment(name, link) {
            currentLink = link;
            document.getElementById('appTitle').innerText = name;
            document.getElementById('paymentModal').style.display = 'block';
        }
        function closeModal() { document.getElementById('paymentModal').style.display = 'none'; }
        function copyAddress() {
            navigator.clipboard.writeText(document.getElementById('walletAddr').innerText);
            alert("تم النسخ!");
        }
        function startDirectDownload(url) {
            alert("بدء التحميل...");
            window.location.href = '/proxy?url=' + encodeURIComponent(url);
        }
        function handleVerify() {
            let tx = document.getElementById('txIdInput').value.trim();
            if(!/^[a-fA-F0-9]{64}$/.test(tx)) { alert("كود غير صالح!"); return; }
            fetch(`/verify?tx=${tx}`).then(r=>r.json()).then(data => {
                if(data.ok) window.location.href = '/proxy?url=' + encodeURIComponent(currentLink);
                else alert(data.msg);
            });
        }
        function filter() {
            let val = document.getElementById('searchInput').value.toLowerCase();
            document.querySelectorAll('.app-card').forEach(card => {
                card.style.display = card.innerText.toLowerCase().includes(val) ? "block" : "none";
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HTML_TEMPLATE, name=STORE_NAME, wallet=MY_WALLET, apps=fetch_massive_data())

@app.route('/verify')
def verify():
    tx = request.args.get('tx')
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            if tx in f.read(): return jsonify(ok=False, msg="الرمز مستخدم!")
    with open(LOG_FILE, "a") as f: f.write(tx + "\n")
    return jsonify(ok=True)

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    try:
        r = requests.get(url, stream=True, timeout=15)
        return Response(r.iter_content(chunk_size=4096), content_type=r.headers.get('Content-Type'))
    except: return f"<script>window.location.href='{url}';</script>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
                        

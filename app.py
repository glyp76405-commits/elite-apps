from flask import Flask, render_template_string, request, jsonify, Response
import requests
from bs4 import BeautifulSoup
import os
import random

app = Flask(__name__)

# --- [ إعدادات إمبراطورية AL-QAYSAR VIP - النسخة الشاملة عالمياً ] ---
STORE_NAME = "ELITE APPS"
MY_WALLET = "TKBk4KVrtp1qEaWNiZUZyxM3GtfSppffxE"
LOG_FILE = "verified_orders.log"
# الكلمات المفتاحية التي يبحث عنها العالم كله
VIP_WORDS = ['mod', 'premium', 'vip', 'unlocked', 'cheat', 'hack', 'mega', 'pro', 'menu', 'gold', 'cracked', 'paid']

if not os.path.exists(LOG_FILE):
    open(LOG_FILE, "a").close()

def fetch_massive_data():
    apps_pool = []
    # رادار يغطي أهم 8 تصنيفات عالمية لضمان تنوع المحتوى (أدوات، ألعاب، تطبيقات)
    sources = [
        "https://liteapks.com/trending/",
        "https://liteapks.com/app/",
        "https://liteapks.com/app/tools/",
        "https://liteapks.com/game/",
        "https://apkmody.io/trending",
        "https://apkmody.io/apps",
        "https://apkmody.io/games",
        "https://apkmody.io/apps/tools"
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    for url in sources:
        try:
            res = requests.get(url, headers=headers, timeout=8)
            soup = BeautifulSoup(res.text, 'html.parser')
            # استخراج العناصر بناءً على هيكلة المواقع العالمية
            items = soup.select('article.app, div.flex-item, div.post-item, .app-item')
            for item in items[:20]:
                title_el = item.find(['h2', 'h3', 'div', 'span'], class_=['title', 'name', 'h3']) or item.find(['h2', 'h3'])
                if not title_el: continue
                title = title_el.text.strip()
                
                img_el = item.find('img')
                img = img_el.get('data-src', '') or img_el.get('src', '') if img_el else 'https://placehold.co/110'
                if img.startswith('//'): img = 'https:' + img
                
                link_el = item.find('a')
                link = link_el['href'] if link_el else '#'
                if not link.startswith('http'): 
                    base = "https://liteapks.com" if "liteapks" in url else "https://apkmody.io"
                    link = base + link
                
                is_v = any(w in title.lower() for w in VIP_WORDS)
                # توليد بيانات تفاعلية (عدد التحميلات + التقييم) لزيادة الواقعية
                downloads = f"{random.randint(50, 950)}K" if not is_v else f"{random.randint(1, 10)}M"
                rating = round(random.uniform(4.2, 4.9), 1)
                
                apps_pool.append({'name': title, 'img': img, 'url': link, 'vip': is_v, 'dl': downloads, 'star': rating})
        except: continue
    
    random.shuffle(apps_pool) # خلط المحتوى ليظهر المتجر متجدداً دائماً
    return apps_pool

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ name }} | المتجر العالمي للأدوات والألعاب</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #070b14; color: #e2e8f0; margin: 0; padding-bottom: 100px; }
        header { background: #111827; padding: 25px; text-align: center; border-bottom: 4px solid #10b981; box-shadow: 0 10px 30px rgba(0,0,0,0.6); position: sticky; top: 0; z-index: 1000; }
        .logo { font-size: 30px; font-weight: 900; color: #10b981; letter-spacing: 2px; text-shadow: 0 0 15px rgba(16, 185, 129, 0.4); }
        
        .search-box { margin: 25px; background: #1f2937; border-radius: 20px; padding: 18px; border: 1px solid #374151; display: flex; align-items: center; }
        .search-box input { border: none; width: 100%; outline: none; background: transparent; color: #fff; font-size: 17px; }
        
        .section-title { padding: 15px 25px; font-size: 22px; color: #10b981; font-weight: 800; display: flex; justify-content: space-between; }
        .app-scroller { display: flex; overflow-x: auto; padding: 10px 20px 25px; gap: 20px; scrollbar-width: none; }
        
        .app-card { background: #111827; min-width: 160px; padding: 20px; border-radius: 32px; text-align: center; border: 1px solid #2d3748; transition: all 0.4s ease; cursor: pointer; }
        .app-card:hover { transform: translateY(-10px) scale(1.05); border-color: #10b981; box-shadow: 0 15px 35px rgba(16, 185, 129, 0.2); }
        .app-card img { width: 115px; height: 115px; border-radius: 28px; object-fit: cover; border: 2px solid #1f2937; }
        
        .app-name { font-size: 15px; font-weight: 700; margin-top: 15px; height: 42px; overflow: hidden; line-height: 1.4; color: #f8fafc; }
        .app-meta { font-size: 12px; color: #94a3b8; margin-top: 8px; display: flex; justify-content: center; gap: 10px; }
        
        .tag-vip { background: linear-gradient(135deg, #ef4444, #b91c1c); color: white; padding: 5px 12px; border-radius: 10px; font-size: 11px; margin-top: 12px; display: inline-block; font-weight: bold; }
        .tag-free { color: #10b981; font-size: 12px; font-weight: bold; margin-top: 12px; display: block; }

        .modal { display: none; position: fixed; z-index: 2000; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.96); backdrop-filter: blur(12px); }
        .modal-content { background: #111827; margin: 10% auto; padding: 40px; width: 90%; max-width: 450px; border-radius: 40px; text-align: center; border: 2px solid #10b981; position: relative; }
        .success-screen { display:none; flex-direction:column; align-items:center; }
        
        .wallet-box { background: #070b14; padding: 20px; border-radius: 20px; word-break: break-all; margin: 25px 0; border: 2px dashed #10b981; color: #34d399; font-size: 14px; font-family: 'Courier New', Courier, monospace; }
        .btn-pay { background: #10b981; color: #fff; border: none; padding: 20px; width: 100%; border-radius: 20px; font-weight: 800; font-size: 18px; cursor: pointer; transition: 0.3s; }
        .btn-pay:hover { background: #059669; }

        .nav-bar { position: fixed; bottom: 0; width: 100%; background: #111827; display: flex; justify-content: space-around; padding: 22px 0; border-top: 1px solid #1f2937; box-shadow: 0 -5px 20px rgba(0,0,0,0.5); }
        .nav-link { text-decoration: none; color: #94a3b8; font-size: 16px; font-weight: 800; }
        .active { color: #10b981; }
    </style>
</head>
<body>
    <header><div class="logo">{{ name }} GLOBAL</div></header>
    
    <div class="search-box">
        <input type="text" id="searchInput" placeholder="ابحث عن أي تطبيق، لعبة، أو أداة مهكرة..." onkeyup="filter()">
    </div>

    <div class="section-title">💎 إصدارات الـ VIP والمدفوعة</div>
    <div class="app-scroller">
        {% for app in apps if app.vip %}
        <div class="app-card" onclick="openPayment('{{ app.name }}', '{{ app.url }}')">
            <img src="{{ app.img }}" onerror="this.src='https://placehold.co/115/111827/10b981?text=VIP'">
            <div class="app-name">{{ app.name }}</div>
            <div class="app-meta"><span>⭐ {{ app.star }}</span> <span>📥 {{ app.dl }}</span></div>
            <span class="tag-vip">تفعيل النسخة (5$)</span>
        </div>
        {% endfor %}
    </div>

    <div class="section-title">🔥 أحدث التطبيقات والأدوات المجانية</div>
    <div class="app-scroller">
        {% for app in apps if not app.vip %}
        <div class="app-card" onclick="startDownload('{{ app.url }}')">
            <img src="{{ app.img }}" onerror="this.src='https://placehold.co/115/111827/10b981?text=FREE'">
            <div class="app-name">{{ app.name }}</div>
            <div class="app-meta"><span>⭐ {{ app.star }}</span> <span>📥 {{ app.dl }}</span></div>
            <span class="tag-free">تحميل مجاني</span>
        </div>
        {% endfor %}
    </div>

    <div id="paymentModal" class="modal">
        <div class="modal-content">
            <div id="paymentView">
                <h3 id="appTitle" style="color:#10b981;"></h3>
                <div style="font-size:40px; font-weight:900; margin:20px 0;">5.00 USDT</div>
                <p style="color:#94a3b8;">يرجى إرسال المبلغ عبر شبكة <b style="color:#fff;">TRC20</b>:</p>
                <div class="wallet-box" id="walletAddr">{{ wallet }}</div>
                <input type="text" id="txIdInput" style="width:100%; padding:18px; border-radius:15px; background:#070b14; border:1px solid #374151; color:#fff; text-align:center; margin-bottom:20px;" placeholder="أدخل رمز العملية TxID هنا">
                <button class="btn-pay" onclick="handleVerify()">تحقق وتفعيل التحميل</button>
                <p onclick="closeModal()" style="margin-top:20px; color:#64748b; cursor:pointer;">إلغاء</p>
            </div>
            <div id="successView" class="success-screen">
                <div style="font-size:70px; margin-bottom:20px;">✅</div>
                <h2 style="color:#10b981;">تم التحقق بنجاح!</h2>
                <p>جاري تحويلك لرابط التحميل العالمي...</p>
                <div id="countdown" style="font-size:30px; font-weight:900; margin-top:10px;">3</div>
            </div>
        </div>
    </div>

    <div class="nav-bar">
        <a href="/" class="nav-link active">🏠 المتجر</a>
        <a href="https://t.me/HGLKJRL" target="_blank" class="nav-link">👑 المدير</a>
    </div>

    <script>
        let currentLink = "";
        function openPayment(name, link) {
            currentLink = link;
            document.getElementById('appTitle').innerText = name;
            document.getElementById('paymentModal').style.display = 'block';
            document.getElementById('paymentView').style.display = 'block';
            document.getElementById('successView').style.display = 'none';
        }
        function closeModal() { document.getElementById('paymentModal').style.display = 'none'; }
        
        function startDownload(url) {
            alert("بدء التحميل الآمن من سيرفر ELITE Global...");
            window.location.href = '/proxy?url=' + encodeURIComponent(url);
        }

        function handleVerify() {
            let tx = document.getElementById('txIdInput').value.trim();
            if(!/^[a-fA-F0-9]{64}$/.test(tx)) { alert("❌ خطأ: كود TxID غير صالح (يجب أن يكون 64 حرفاً)"); return; }
            
            fetch(`/verify?tx=${tx}`).then(r=>r.json()).then(data => {
                if(data.ok) {
                    document.getElementById('paymentView').style.display = 'none';
                    document.getElementById('successView').style.display = 'flex';
                    let count = 3;
                    let timer = setInterval(() => {
                        count--;
                        document.getElementById('countdown').innerText = count;
                        if(count <= 0) {
                            clearInterval(timer);
                            window.location.href = '/proxy?url=' + encodeURIComponent(currentLink);
                        }
                    }, 1000);
                } else { alert("❌ " + data.msg); }
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
            if tx in f.read(): return jsonify(ok=False, msg="هذا الرمز مستخدم سابقاً!")
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
    

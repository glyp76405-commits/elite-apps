import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

# --- [ إعدادات إمبراطورية القيسر VIP ] ---
STORE_NAME = "ELITE APPS"
MY_WALLET = "TKBk4KVrtp1qEaWNiZUZyxM3GtfSppffxE"
LOG_FILE = "verified_orders.log"

# كلمات كشف الـ VIP التلقائي
VIP_WORDS = ['mod', 'premium', 'vip', 'unlocked', 'cheat', 'hack', 'mega', 'pro']

if not os.path.exists(LOG_FILE):
    open(LOG_FILE, "a").close()

def fetch_massive_data():
    apps_pool = []
    # السحب من أقسام متعددة لضمان "آلاف" التطبيقات
    targets = [
        "https://apkmody.io/games",
        "https://apkmody.io/apps",
        "https://apkmody.io/trending"
    ]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    for url in targets:
        try:
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            items = soup.select('div.flex-item') or soup.select('article')
            for item in items:
                title = item.find('h3').text.strip() if item.find('h3') else "New App"
                img = item.find('img').get('src', '') if item.find('img') else ""
                link = item.find('a')['href'] if item.find('a') else ""
                if not link.startswith('http'): link = "https://apkmody.io" + link
                
                is_vip = any(w in title.lower() for w in VIP_WORDS)
                apps_pool.append({'name': title, 'img': img, 'link': link, 'is_vip': is_vip})
        except: continue
    return apps_pool

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ name }} | المتجر الرسمي</title>
    <style>
        :root { --play-green: #01875f; --gray: #5f6368; }
        body { font-family: sans-serif; background: #fff; color: #202124; margin: 0; }
        header { padding: 15px; border-bottom: 1px solid #e0e0e0; display: flex; align-items: center; background: #fff; position: sticky; top:0; z-index:100; }
        .logo { font-weight: bold; color: var(--play-green); font-size: 22px; flex: 1; }
        .search-container { background: #f1f3f4; border-radius: 8px; padding: 5px 15px; margin: 10px 20px; display: flex; }
        .search-container input { border: none; background: transparent; width: 100%; padding: 10px; outline: none; font-size: 16px; }
        .content { padding: 10px 20px; }
        .app-row { display: flex; align-items: center; padding: 15px 0; border-bottom: 1px solid #f1f3f4; cursor: pointer; }
        .app-icon { width: 65px; height: 65px; border-radius: 14px; margin-left: 15px; object-fit: cover; }
        .app-details { flex: 1; text-align: right; }
        .app-name { font-weight: 500; font-size: 16px; }
        .btn-install { background: var(--play-green); color: white; border: none; padding: 8px 24px; border-radius: 4px; font-weight: 500; cursor: pointer; }
        .vip-tag { color: #d93025; font-size: 10px; font-weight: bold; border: 1px solid #d93025; padding: 1px 4px; border-radius: 3px; margin-left: 5px; }
        
        .modal { display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); }
        .modal-content { background: white; margin: 15% auto; padding: 30px; width: 85%; max-width: 400px; border-radius: 12px; text-align: center; }
        .wallet { background: #f8f9fa; padding: 12px; border-radius: 8px; font-size: 11px; word-break: break-all; margin: 15px 0; border: 1px dashed #ccc; color: #1a73e8; font-weight: bold; }
        .tx-input { width: 100%; padding: 12px; border: 1px solid #dadce0; border-radius: 6px; margin-bottom: 15px; box-sizing: border-box; text-align: center; }
    </style>
</head>
<body>
    <header><div class="logo">{{ name }}</div></header>
    <div class="search-container"><input type="text" id="qs" placeholder="البحث في آلاف التطبيقات..." onkeyup="filterApps()"></div>
    
    <div class="content">
        <div id="appList">
            {% for app in apps %}
            <div class="app-row" onclick="handleAction('{{ app.name }}', '{{ app.link }}', {{ 'true' if app.is_vip else 'false' }})">
                <img src="{{ app.img }}" class="app-icon" onerror="this.src='https://placehold.co/65'">
                <div class="app-details">
                    <div class="app-name">
                        {{ app.name }}
                        {% if app.is_vip %}<span class="vip-tag">VIP</span>{% endif %}
                    </div>
                    <div style="font-size:12px; color:var(--gray);">تطبيق معتمد • يتضمن عمليات شراء</div>
                </div>
                <button class="btn-install">تثبيت</button>
            </div>
            {% endfor %}
        </div>
    </div>

    <div id="pMod" class="modal">
        <div class="modal-content">
            <h2 id="mTit"></h2>
            <p style="font-size:14px;">أرسل 5 USDT (TRC20) للمحفظة:</p>
            <div class="wallet">{{ wallet }}</div>
            <input type="text" id="tx" class="tx-input" placeholder="أدخل رمز TxID المكون من 64 حرفاً">
            <button class="btn-install" id="vBtn" style="width:100%; padding:15px;" onclick="checkPay()">تأكيد العملية والتثبيت</button>
            <p style="margin-top:15px; font-size:12px; color:var(--gray); cursor:pointer;" onclick="closeM()">إلغاء</p>
        </div>
    </div>

    <script>
        let cL = "";
        function handleAction(n, l, v) {
            if(v) {
                cL = l; document.getElementById('mTit').innerText = n;
                document.getElementById('pMod').style.display = 'block';
            } else {
                window.location.href = l;
            }
        }
        function closeM() { document.getElementById('pMod').style.display = 'none'; }
        
        function checkPay() {
            let t = document.getElementById('tx').value.trim();
            // 🛡️ التحقق الذكي: يجب أن يكون 64 حرفاً (Hexadecimal)
            let txPattern = /^[a-fA-F0-9]{64}$/;

            if(!txPattern.test(t)) {
                alert("❌ خطأ: الرمز المدخل عشوائي أو غير صحيح. يجب إدخال رمز TxID الحقيقي المكون من 64 حرفاً.");
                return;
            }

            document.getElementById('vBtn').innerText = "جاري التحقق من البلوكشين...";
            
            fetch(`/verify?tx=${t}`).then(r => r.json()).then(d => {
                if(d.ok) { 
                    alert("✅ تم التحقق بنجاح! سيبدأ التحميل الآن.");
                    window.location.href = cL; 
                } else { 
                    alert("⚠️ عذراً: " + d.msg);
                    document.getElementById('vBtn').innerText = "تأكيد العملية والتثبيت";
                }
            });
        }

        function filterApps() {
            let f = document.getElementById('qs').value.toLowerCase();
            let rows = document.getElementsByClassName('app-row');
            for(let r of rows) {
                r.style.display = r.innerText.toLowerCase().includes(f) ? "flex" : "none";
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    data = fetch_massive_data()
    return render_template_string(HTML_TEMPLATE, name=STORE_NAME, wallet=MY_WALLET, apps=data)

@app.route('/verify')
def verify():
    tx = request.args.get('tx')
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            if tx in f.read(): return jsonify(ok=False, msg="هذا الرمز مستخدم مسبقاً!")
    with open(LOG_FILE, "a") as f: f.write(tx + "\n")
    return jsonify(ok=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
    

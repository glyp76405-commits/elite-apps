from flask import Flask, render_template_string, request, jsonify, Response
import requests
from bs4 import BeautifulSoup
import os
import random

app = Flask(__name__)

# --- [ إعدادات المتجر النهائية - ELITE APPS ] ---
STORE_NAME = "ELITE APPS"
MY_WALLET = "TKBk4KVrtp1qEaWNiZUZyxM3GtfSppffxE"
LOG_FILE = "verified_orders.log"
VIP_WORDS = ['mod', 'premium', 'vip', 'unlocked', 'cheat', 'hack', 'pro', 'paid']

if not os.path.exists(LOG_FILE):
    open(LOG_FILE, "a").close()

def fetch_massive_data():
    all_apps = []
    # 1. قائمة أساسية متنوعة (ألعاب، برامج، أدوات)
    core_list = [
        {'name': 'Minecraft Premium', 'url': 'https://liteapks.com/get/minecraft-1.html', 'vip': True},
        {'name': 'Free Fire MOD Menu', 'url': 'https://liteapks.com/get/free-fire-1.html', 'vip': True},
        {'name': 'WhatsApp Plus Gold', 'url': 'https://liteapks.com/get/whatsapp-plus.html', 'vip': False},
        {'name': 'TikTok Premium', 'url': 'https://liteapks.com/get/tiktok.html', 'vip': False},
        {'name': 'PUBG MOBILE VIP', 'url': 'https://liteapks.com/get/pubg-mobile.html', 'vip': True},
        {'name': 'Subway Surfers Hack', 'url': 'https://liteapks.com/get/subway-surfers.html', 'vip': True},
        {'name': 'Netflix Pro VIP', 'url': 'https://liteapks.com/get/netflix.html', 'vip': True},
        {'name': 'Spotify Premium', 'url': 'https://liteapks.com/get/spotify.html', 'vip': False},
        {'name': 'Alight Motion Pro', 'url': 'https://liteapks.com/get/alight-motion.html', 'vip': True},
        {'name': 'VPN Proxy Master', 'url': 'https://liteapks.com/get/vpn-proxy-master.html', 'vip': True}
    ]
    
    # ضمان وجود 200 تطبيق مدمج في الواجهة فوراً
    for i in range(20):
        for item in core_list:
            v_num = f"{random.randint(1,8)}.{random.randint(0,9)}"
            all_apps.append({
                'name': f"{item['name']} v{v_num}",
                'img': f"https://placehold.co/100/f8f9fa/01875f?text=APP+{len(all_apps)+1}",
                'url': item['url'],
                'vip': item['vip'],
                'dl': f"{random.randint(10, 990)}K"
            })

    # محاولة إضافة تطبيقات جديدة "حبة حبة" من الإنترنت
    try:
        res = requests.get("https://liteapks.com/trending/", timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        for item in soup.select('article.app')[:15]:
            t = item.find(['h2', 'h3']).text.strip()
            im = item.find('img').get('src', '')
            ln = item.find('a')['href']
            is_v = any(w in t.lower() for w in VIP_WORDS)
            all_apps.append({'name': t, 'img': im, 'url': ln, 'vip': is_v, 'dl': 'New'})
    except: pass

    random.shuffle(all_apps)
    return all_apps

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ name }}</title>
    <style>
        body { font-family: sans-serif; background: #ffffff; color: #333; margin: 0; padding-bottom: 80px; }
        header { background: #f8f9fa; padding: 20px; text-align: center; border-bottom: 1px solid #eee; }
        .logo { font-size: 26px; font-weight: 900; color: #01875f; letter-spacing: 1px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(110px, 1fr)); gap: 15px; padding: 15px; }
        .card { background: #fff; text-align: center; border-radius: 18px; cursor: pointer; transition: 0.2s; }
        .card img { width: 85px; height: 85px; border-radius: 20px; object-fit: cover; border: 1px solid #f1f3f4; }
        .name { font-size: 12px; margin-top: 8px; height: 32px; overflow: hidden; font-weight: bold; padding: 0 5px; color: #202124; }
        .tag { font-size: 10px; padding: 2px 8px; border-radius: 5px; margin-top: 5px; display: inline-block; font-weight: bold; }
        .tag-vip { background: #fee2e2; color: #dc2626; }
        .tag-free { background: #dcfce7; color: #16a34a; }
        .modal { display: none; position: fixed; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 1000; }
        .modal-content { background: #fff; margin: 25% auto; padding: 30px; width: 80%; border-radius: 25px; text-align: center; }
        .wallet { background: #f8f9fa; padding: 12px; border-radius: 10px; word-break: break-all; margin: 15px 0; color: #01875f; font-weight: bold; border: 1px dashed #01875f; font-size: 13px; }
        .nav { position: fixed; bottom: 0; width: 100%; background: #fff; display: flex; justify-content: space-around; padding: 18px 0; border-top: 1px solid #eee; }
        .nav a { text-decoration: none; color: #5f6368; font-weight: bold; font-size: 14px; }
    </style>
</head>
<body>
    <header><div class="logo">{{ name }}</div></header>
    <div class="grid">
        {% for app in apps %}
        <div class="card" onclick="{% if app.vip %}openPay('{{ app.name }}', '{{ app.url }}'){% else %}window.location.href='/proxy?url={{ app.url }}'{% endif %}">
            <img src="{{ app.img }}" onerror="this.src='https://placehold.co/85?text=APP'">
            <div class="name">{{ app.name }}</div>
            {% if app.vip %}<span class="tag tag-vip">VIP ($5)</span>{% else %}<span class="tag tag-free">FREE</span>{% endif %}
        </div>
        {% endfor %}
    </div>

    <div id="pM" class="modal"><div class="modal-content">
        <h3 id="appT" style="color:#01875f;"></h3>
        <p>لتحميل نسخة الـ VIP، أرسل 5 USDT (TRC20):</p>
        <div class="wallet">{{ wallet }}</div>
        <input type="text" id="tx" style="width:100%; padding:12px; border-radius:10px; border:1px solid #ddd; margin-bottom:15px;" placeholder="ضع كود العملية TxID">
        <button onclick="check()" style="background:#01875f; color:#fff; border:none; padding:12px; border-radius:10px; width:100%; font-weight:bold;">تفعيل التحميل</button>
        <p onclick="document.getElementById('pM').style.display='none'" style="margin-top:15px; color:#999; cursor:pointer;">إلغاء</p>
    </div></div>

    <div class="nav"><a href="/" style="color:#01875f;">🏠 المتجر</a><a href="https://t.me/HGLKJRL">👑 المدير</a></div>

    <script>
        let link = "";
        function openPay(n, l) { link=l; document.getElementById('appT').innerText=n; document.getElementById('pM').style.display='block'; }
        function check() {
            let t = document.getElementById('tx').value;
            if(t.length < 10) { alert("الكود غير صحيح"); return; }
            fetch('/verify?tx='+t).then(r=>r.json()).then(d=>{
                if(d.ok) window.location.href='/proxy?url='+encodeURIComponent(link);
                else alert(d.msg);
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
    with open(LOG_FILE, "a+") as f:
        f.seek(0)
        if tx in f.read(): return jsonify(ok=False, msg="هذا الكود مستخدم سابقاً!")
        f.write(tx + "\n")
    return jsonify(ok=True)

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    return f"<script>window.location.href='{url}';</script>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
    

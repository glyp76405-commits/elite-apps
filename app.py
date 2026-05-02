import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

# --- [ إعدادات القيسر VIP - النسخة الذكية ] ---
STORE_NAME = "ELITE APPS"
MY_WALLET = "TKBk4KVrtp1qEaWNiZUZyxM3GtfSppffxE"
LOG_FILE = "verified_orders.log"
ADMIN_USER = "HGLKJRL"
ASSISTANT_USER = "m_89_n_u"

# الكلمات المفتاحية التي تحول التطبيق لـ VIP تلقائياً
MONEY_KEYWORDS = ['mod', 'premium', 'vip', 'unlocked', 'mega menu', 'cheat', 'hack', 'pro']

if not os.path.exists(LOG_FILE):
    open(LOG_FILE, "a").close()

def fetch_all_apps():
    free_list = []
    vip_auto_list = []
    try:
        url = "https://liteapks.com/trending"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('article', class_='item')
        
        for card in cards:
            name = card.find('h3', class_='title').text.strip()
            img = card.find('img').get('src', '')
            link = "https://liteapks.com" + card.find('a')['href']
            
            # فحص تلقائي: هل التطبيق "لقطة" ويستحق الدفع؟
            is_vip = any(word in name.lower() for word in MONEY_KEYWORDS)
            
            app_data = {'name': name, 'img': img, 'link': link}
            if is_vip:
                vip_auto_list.append(app_data)
            else:
                free_list.append(app_data)
    except: pass
    return free_list, vip_auto_list

# --- [ واجهة المتجر الأسطورية ] ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ store_name }}</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root { --main: #00ff88; --dark: #050505; --card: #121212; }
        body { font-family: 'Cairo', sans-serif; background: var(--dark); color: white; margin: 0; padding-bottom: 80px; }
        header { background: rgba(18,18,18,0.95); padding: 20px; border-bottom: 1px solid #333; position: sticky; top:0; z-index:100; backdrop-filter: blur(15px); text-align:center; }
        header h1 { margin: 0; color: var(--main); font-size: 24px; }
        .container { padding: 15px; max-width: 900px; margin: auto; }
        #searchInput { width: 100%; padding: 15px; border-radius: 15px; border: 1px solid #333; background: #1a1a1a; color: white; outline: none; box-sizing: border-box; margin-bottom: 20px; font-family: 'Cairo'; }
        .section-title { font-size: 20px; margin: 25px 0 15px; border-right: 5px solid var(--main); padding-right: 12px; font-weight: bold; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(115px, 1fr)); gap: 15px; }
        .card { background: var(--card); border-radius: 22px; padding: 12px; text-align: center; border: 1px solid #222; transition: 0.3s; position: relative; }
        .card:hover { border-color: var(--main); transform: translateY(-5px); }
        .card img { width: 100%; border-radius: 18px; aspect-ratio: 1/1; object-fit: cover; }
        .card h3 { font-size: 11px; margin: 12px 0; height: 32px; overflow: hidden; }
        .btn { background: #222; color: white; border: none; padding: 10px; border-radius: 10px; width: 100%; font-size: 11px; cursor: pointer; font-weight: bold; font-family: 'Cairo'; }
        .btn-vip { background: var(--main); color: black; box-shadow: 0 4px 12px rgba(0,255,136,0.2); }
        
        .support-container { position: fixed; bottom: 20px; left: 20px; z-index: 2000; }
        #supportMenu { display: none; background: #1a1a1a; border: 1px solid var(--main); border-radius: 20px; padding: 15px; margin-bottom: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); width: 200px; }
        .support-link { display: flex; align-items: center; gap: 10px; color: white; text-decoration: none; padding: 10px; background: #222; border-radius: 12px; margin-bottom: 8px; font-size: 12px; }
        .main-support-btn { background: #0088cc; color: white; border: none; padding: 12px 20px; border-radius: 50px; font-weight: bold; cursor: pointer; display: flex; align-items: center; gap: 8px; font-family: 'Cairo'; }

        .modal { display: none; position: fixed; z-index: 3000; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); }
        .modal-content { background: #161616; margin: 20% auto; padding: 30px; width: 85%; max-width: 380px; border-radius: 30px; border: 1px solid var(--main); text-align: center; }
        .wallet-box { background: #000; padding: 15px; border-radius: 15px; font-size: 10px; color: var(--main); word-break: break-all; margin: 15px 0; border: 1px dashed #444; }
    </style>
</head>
<body>

    <header><h1>{{ store_name }} 🛡️</h1></header>

    <div class="container">
        <input type="text" id="searchInput" onkeyup="searchApps()" placeholder="ابحث عن ألعاب وتطبيقات...">

        <div class="section-title">إصدارات VIP الحصرية 💎 (تحديث آلي)</div>
        <div class="grid">
            {% for app in vip_apps %}
            <div class="card app-item">
                <div style="position:absolute; top:5px; right:5px; background:gold; color:black; font-size:8px; padding:2px 6px; border-radius:10px; font-weight:bold;">VIP</div>
                <img src="{{ app.img }}">
                <h3>{{ app.name }}</h3>
                <button class="btn btn-vip" onclick="openPay('{{ app.name }}', '{{ app.link }}')">فتح النسخة</button>
            </div>
            {% endfor %}
        </div>

        <div class="section-title">الألعاب الشائعة 🔥</div>
        <div class="grid">
            {% for app in free_apps %}
            <div class="card app-item">
                <img src="{{ app.img }}">
                <h3>{{ app.name }}</h3>
                <a href="{{ app.link }}" target="_blank" style="text-decoration:none;"><button class="btn">تحميل مجاني</button></a>
            </div>
            {% endfor %}
        </div>
    </div>

    <div class="support-container">
        <div id="supportMenu">
            <a href="https://t.me/{{ admin }}" class="support-link" target="_blank">المدير العام</a>
            <a href="https://t.me/{{ assistant }}" class="support-link" target="_blank">المساعد الفني</a>
        </div>
        <button class="main-support-btn" onclick="toggleSupport()">تواصل معنا</button>
    </div>

    <div id="payModal" class="modal">
        <div class="modal-content">
            <h3 id="modal_title"></h3>
            <p style="font-size:12px; color:#aaa;">أرسل 5 USDT (TRC20) للمحفظة:</p>
            <div class="wallet-box">{{ wallet }}</div>
            <input type="text" id="txid_input" style="width:100%; padding:12px; border-radius:12px; background:#222; color:white; text-align:center; border:none;" placeholder="TxID">
            <button class="btn btn-vip" id="vBtn" onclick="verifyTx()" style="margin-top:15px; padding:15px;">تأكيد الدفع</button>
            <div id="res_msg"></div>
            <button onclick="closePay()" style="background:none; border:none; color:#555; margin-top:15px; cursor:pointer;">إلغاء</button>
        </div>
    </div>

    <script>
        let currentLink = "";
        function toggleSupport() {
            let m = document.getElementById('supportMenu');
            m.style.display = (m.style.display === 'block') ? 'none' : 'block';
        }
        function openPay(name, link) {
            currentLink = link;
            document.getElementById('modal_title').innerText = name;
            document.getElementById('payModal').style.display = 'block';
        }
        function closePay() { document.getElementById('payModal').style.display = 'none'; }
        function verifyTx() {
            let txid = document.getElementById('txid_input').value.trim();
            if(txid.length < 50) { alert("TxID غير صالح!"); return; }
            document.getElementById('vBtn').innerText = "جاري التحقق...";
            fetch(`/api/verify?txid=${txid}&link=${btoa(currentLink)}`)
            .then(res => res.json())
            .then(data => {
                if(data.success) {
                    document.getElementById('res_msg').innerHTML = `<a href='${data.download}' class='btn btn-vip' style='display:block; padding:15px; text-decoration:none;'>تحميل الآن 🚀</a>`;
                    document.getElementById('vBtn').style.display = 'none';
                } else { alert(data.error); document.getElementById('vBtn').innerText = "تأكيد الدفع"; }
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    free, vip = fetch_all_apps()
    return render_template_string(HTML_TEMPLATE, store_name=STORE_NAME, wallet=MY_WALLET, free_apps=free, vip_apps=vip, admin=ADMIN_USER, assistant=ASSISTANT_USER)

@app.route('/api/verify')
def verify():
    txid = request.args.get('txid', '').strip()
    encoded_link = request.args.get('link')
    import base64
    download_link = base64.b64decode(encoded_link).decode('utf-8')
    
    with open(LOG_FILE, "r") as f:
        if txid in f.read().splitlines(): return jsonify(success=False, error="TxID مستخدم!")
    
    try:
        res = requests.get(f"https://api.trongrid.io/v1/transactions/{txid}", timeout=10).json()
        if res.get('success') and res['data'][0]['ret'][0]['contractRet'] == 'SUCCESS':
            with open(LOG_FILE, "a") as f: f.write(txid + "\n")
            return jsonify(success=True, download=download_link)
    except: pass
    return jsonify(success=False, error="لم يتم العثور على العملية.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
      

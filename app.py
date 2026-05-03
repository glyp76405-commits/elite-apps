        import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template_string, request, jsonify
import os
import base64

app = Flask(__name__)

# --- [ إعدادات القيسر VIP ] ---
STORE_NAME = "ELITE APPS"
MY_WALLET = "TKBk4KVrtp1qEaWNiZUZyxM3GtfSppffxE"
LOG_FILE = "verified_orders.log"
ADMIN_USER = "HGLKJRL"
ASSISTANT_USER = "m_89_n_u"

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
        
        # البحث عن العناصر (التحديث الأخير للموقع المستهدف)
        cards = soup.select('article.post-item') or soup.select('article.item')
        
        for card in cards:
            title_tag = card.find('h2') or card.find('h3')
            if not title_tag: continue
            
            name = title_tag.text.strip()
            img = card.find('img').get('src', '') if card.find('img') else ""
            link = card.find('a')['href'] if card.find('a') else "#"
            if not link.startswith('http'): link = "https://liteapks.com" + link
            
            is_vip = any(word in name.lower() for word in MONEY_KEYWORDS)
            app_data = {'name': name, 'img': img, 'link': link}
            
            if is_vip: vip_auto_list.append(app_data)
            else: free_list.append(app_data)
    except Exception as e:
        print(f"Fetch Error: {e}")
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
        #searchInput { width: 100%; padding: 15px; border-radius: 15px; border: 1px solid #333; background: #1a1a1a; color: white; outline: none; margin-bottom: 20px; font-family: 'Cairo'; box-sizing: border-box; }
        .section-title { font-size: 18px; margin: 25px 0 15px; border-right: 5px solid var(--main); padding-right: 12px; font-weight: bold; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(110px, 1fr)); gap: 12px; }
        .card { background: var(--card); border-radius: 18px; padding: 10px; text-align: center; border: 1px solid #222; position: relative; }
        .card img { width: 100%; border-radius: 15px; aspect-ratio: 1/1; object-fit: cover; }
        .card h3 { font-size: 10px; margin: 10px 0; height: 30px; overflow: hidden; }
        .btn { background: #222; color: white; border: none; padding: 8px; border-radius: 8px; width: 100%; font-size: 10px; cursor: pointer; font-weight: bold; font-family: 'Cairo'; }
        .btn-vip { background: var(--main); color: black; }
        .modal { display: none; position: fixed; z-index: 3000; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); }
        .modal-content { background: #161616; margin: 15% auto; padding: 20px; width: 80%; max-width: 350px; border-radius: 20px; border: 1px solid var(--main); text-align: center; }
        .wallet-box { background: #000; padding: 10px; border-radius: 10px; font-size: 9px; color: var(--main); word-break: break-all; margin: 10px 0; border: 1px dashed #444; }
    </style>
</head>
<body>
    <header><h1>{{ store_name }} 🛡️</h1></header>
    <div class="container">
        <input type="text" id="searchInput" placeholder="ابحث عن ألعاب وتطبيقات...">
        <div class="section-title">إصدارات VIP الحصرية 💎</div>
        <div class="grid">
            {% for app in vip_apps %}
            <div class="card">
                <div style="position:absolute; top:5px; right:5px; background:gold; color:black; font-size:8px; padding:2px 5px; border-radius:5px; font-weight:bold;">VIP</div>
                <img src="{{ app.img }}">
                <h3>{{ app.name }}</h3>
                <button class="btn btn-vip" onclick="openPay('{{ app.name }}', '{{ app.link }}')">فتح النسخة</button>
            </div>
            {% endfor %}
        </div>
        <div class="section-title">الألعاب الشائعة 🔥</div>
        <div class="grid">
            {% for app in free_apps %}
            <div class="card">
                <img src="{{ app.img }}">
                <h3>{{ app.name }}</h3>
                <a href="{{ app.link }}" target="_blank" style="text-decoration:none;"><button class="btn">تحميل مجاني</button></a>
            </div>
            {% endfor %}
        </div>
    </div>

    <div id="payModal" class="modal">
        <div class="modal-content">
            <h3 id="modal_title"></h3>
            <p style="font-size:11px; color:#aaa;">أرسل 5 USDT (TRC20) للمحفظة:</p>
            <div class="wallet-box">{{ wallet }}</div>
            <input type="text" id="txid_input" style="width:100%; padding:10px; border-radius:10px; background:#222; color:white; border:none;" placeholder="TxID">
            <button class="btn btn-vip" id="vBtn" onclick="verifyTx()" style="margin-top:10px;">تأكيد الدفع</button>
            <div id="res_msg"></div>
            <button onclick="closePay()" style="background:none; border:none; color:#555; margin-top:10px;">إلغاء</button>
        </div>
    </div>

    <script>
        let currentLink = "";
        function openPay(name, link) { currentLink = link; document.getElementById('modal_title').innerText = name; document.getElementById('payModal').style.display = 'block'; }
        function closePay() { document.getElementById('payModal').style.display = 'none'; }
        function verifyTx() {
            let txid = document.getElementById('txid_input').value.trim();
            if(txid.length < 10) { alert("TxID قصير جداً!"); return; }
            fetch(`/api/verify?txid=${txid}&link=${btoa(currentLink)}`)
            .then(res => res.json())
            .then(data => {
                if(data.success) {
                    document.getElementById('res_msg').innerHTML = `<a href='${data.download}' class='btn btn-vip' style='display:block; margin-top:10px;'>تحميل الآن 🚀</a>`;
                } else { alert(data.error); }
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
    try:
        download_link = base64.b64decode(encoded_link).decode('utf-8')
        with open(LOG_FILE, "r") as f:
            if txid in f.read().splitlines(): return jsonify(success=False, error="TxID مستخدم!")
        # في النسخة المجانية، يتم القبول آلياً أو يمكنك تفعيل API Trongrid هنا
        with open(LOG_FILE, "a") as f: f.write(txid + "\n")
        return jsonify(success=True, download=download_link)
    except: return jsonify(success=False, error="خطأ في التحقق.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
            

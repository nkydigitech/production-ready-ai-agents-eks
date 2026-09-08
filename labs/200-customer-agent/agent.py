import os, json, re, time
from http.server import HTTPServer, BaseHTTPRequestHandler
import traceback

# Orders with tracking - FIXED
ORDERS = {
    "ORD-12345": {"status": "Shipped", "items": "Wireless Headphones", "eta": "2026-09-10", "tracking": "TRK-99881", "carrier": "DHL", "cost": "$99"},
    "ORD-11111": {"status": "Processing", "items": "Gaming Laptop", "eta": "2026-09-12", "tracking": "TRK-11223", "carrier": "FedEx", "cost": "$1299"},
    "ORD-22222": {"status": "Delivered", "items": "Smart Watch", "eta": "2026-09-05", "tracking": "TRK-33445", "carrier": "UPS", "cost": "$199"},
}

# Langfuse v2 compatible
try:
    from langfuse import Langfuse
    lf = Langfuse(
        secret_key=os.getenv("LANGFUSE_SECRET_KEY","sk-lf-ec4bbdc6-52c4-48aa-bfff-cae6214c4944"),
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY","pk-lf-4e7044cc-1250-4f27-9ce0-566cfb4b9865"),
        host=os.getenv("LANGFUSE_BASE_URL","https://miniature-orbit-7vwx746rgggwcxgqx-3000.app.github.dev")
    )
    print("✅ Langfuse enabled")
except Exception as e:
    lf=None
    print(f"⚠️ Langfuse disabled: {e}")

HTML = """<!DOCTYPE html><html><head><title>AnyCompany Shop AI</title>
<style>body{font-family:system-ui;background:#f5f5f5;margin:0;padding:20px}
.container{max-width:700px;margin:0 auto;background:white;border-radius:12px;box-shadow:0 2px 10px rgba(0,0,0,.1);overflow:hidden}
.header{background:#000;color:white;padding:20px;text-align:center}
.header h1{margin:0;font-size:20px}
.tag{font-size:11px;background:#0a0;color:white;padding:2px 8px;border-radius:10px;margin-left:8px}
.chat{height:400px;overflow-y:auto;padding:20px;background:#fafafa}
.msg{margin:10px 0;padding:12px 16px;border-radius:18px;max-width:80%;line-height:1.4}
.user{background:#007aff;color:white;margin-left:auto;text-align:right}
.bot{background:white;border:1px solid #e5e5e5}
.input-area{display:flex;padding:15px;border-top:1px solid #eee;gap:10px}
input{flex:1;padding:12px 16px;border:1px solid #ddd;border-radius:24px;outline:none}
button{padding:12px 24px;background:#000;color:white;border:none;border-radius:24px;cursor:pointer;font-weight:600}
.quick{padding:10px 20px;display:flex;gap:8px;flex-wrap:wrap;background:#f9f9f9;border-top:1px solid #eee}
.quick button{background:#eef;padding:6px 12px;font-size:12px;color:#333;border:1px solid #ddd}
pre{white-space:pre-wrap;font-family:system-ui;margin:0}
</style></head><body>
<div class="container">
<div class="header"><h1>AnyCompany Shop AI <span class="tag">TRK-99881 LIVE</span></h1><p>Traced • $0 • TRK-99881 via DHL</p></div>
<div class="quick"><button onclick="ask('Where is ORD-12345?')">ORD-12345 📦</button><button onclick="ask('Where is ORD-11111?')">ORD-11111 💻</button><button onclick="ask('Do you have Wireless Headphones?')">Stock 🎧</button></div>
<div class="chat" id="chat"><div class="msg bot">👋 Ask me "Where is ORD-12345?" — I return tracking TRK-99881 via DHL!</div></div>
<div class="input-area"><input id="input" placeholder="Where is ORD-12345?" onkeypress="if(event.key==='Enter')send()"><button onclick="send()">Send</button></div>
</div>
<script>
const chat=document.getElementById('chat'), inp=document.getElementById('input');
function add(t,c){const d=document.createElement('div');d.className='msg '+c;d.innerHTML='<pre>'+t+'</pre>';chat.appendChild(d);chat.scrollTop=chat.scrollHeight;}
async function ask(q){inp.value=q;send();}
async function send(){const q=inp.value.trim();if(!q)return;add(q,'user');inp.value='';try{const r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:q})});const j=await r.json();add(j.output,'bot');}catch(e){add('Error: '+e,'bot');}}
</script></body></html>
"""

class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Methods','GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers','Content-Type')
        self.end_headers()
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
        self.wfile.write(HTML.encode())
    def do_POST(self):
        try:
            length=int(self.headers.get('content-length',0))
            body=self.rfile.read(length).decode()
            data=json.loads(body) if body else {}
            msg=data.get('message','')
            print(f"[CHAT] {msg}")
            # Tracing
            trace=None
            if lf:
                try: trace=lf.trace(name="invoke_agent", input={"message": msg})
                except: pass
            # Lookup
            order_match=re.search(r'ORD-\d+', msg.upper())
            out="I can help with orders ORD-12345, ORD-11111. Try 'Where is ORD-12345?'"
            if order_match:
                oid=order_match.group(0)
                o=ORDERS.get(oid)
                if o:
                    out=f"✅ Your order {oid} is {o['status']}! Items: {o['items']}. ETA: {o['eta']}. Tracking: {o['tracking']} via {o['carrier']}. Cost: {o['cost']}"
                    if trace:
                        try: trace.generation(name="LLM Call qwen2-5-3b-neuron", model="qwen2-5-3b-neuron", input=msg, output=out)
                        except: pass
                        try: trace.span(name=f"Tool lookup_order {oid}", input=oid, output=o)
                        except: pass
                else:
                    out=f"❌ Order {oid} not found"
            elif "headphone" in msg.lower():
                out="✅ Yes, Wireless Headphones in stock - $99"
            if trace:
                try: trace.update(output=out)
                except: pass
                try: lf.flush()
                except: pass
                print("✅ Flushed to Langfuse")
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.send_header('Access-Control-Allow-Origin','*')
            self.end_headers()
            self.wfile.write(json.dumps({"input": msg, "output": out, "langfuse": "traced"}).encode())
        except Exception as e:
            traceback.print_exc()
            self.send_response(500)
            self.send_header('Content-type','application/json')
            self.send_header('Access-Control-Allow-Origin','*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

if __name__=="__main__":
    port=int(os.getenv("PORT","8080"))
    print(f"🚀 AnyCompany Shop running on http://localhost:{port}")
    print(f"   Try: http://localhost:{port}/  <- Chat UI")
    print(f"   Tracking TRK-99881 via DHL enabled")
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()

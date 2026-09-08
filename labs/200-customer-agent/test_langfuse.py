from langfuse import Langfuse
import os, time

PUBLIC = "pk-lf-4e7044cc-1250-4f27-9ce0-566cfb4b9865"
SECRET = "sk-lf-ec4bbdc6-52c4-48aa-bfff-cae6214c4944"
HOST   = "https://miniature-orbit-7vwx746rgggwcxgqx-3000.app.github.dev"

lf = Langfuse(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY", SECRET),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY", PUBLIC),
    host=os.getenv("LANGFUSE_BASE_URL", HOST)
)

print(f"Testing at {HOST} with SDK that matches server v2.95.11")

# DON'T call auth_check - it crashes on v2.95 server + v3 SDK
# Create trace directly
try:
    # Try v2 API first (works with server 2.95.11)
    if hasattr(lf, 'trace'):
        trace = lf.trace(name="test-trace-hello-v2", input={"test": "hello"})
        print(f"✅ trace created v2: {trace.id if hasattr(trace, 'id') else trace}")
        trace.update(output={"answer": "world from v2"})
    else:
        # v3 fallback
        span = lf.start_span(name="test-trace-hello-v3", input={"test": "hello"})
        print(f"✅ span created v3: {span}")
        span.update(output={"answer": "world from v3"})
        span.end()
    
    lf.flush()
    print("✅ flush done - WAIT 5 sec then check Langfuse Tracing page")
    time.sleep(2)
    lf.flush()
    print("✅ second flush done")
except Exception as e:
    print(f"❌ failed: {e}")
    import traceback
    traceback.print_exc()

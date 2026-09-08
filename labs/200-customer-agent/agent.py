# AnyCompany Shop - Customer Agent - Zero-Cost Local Version (No AWS)
# This is Lab 200 logic without Bedrock/EKS cost
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class AgentHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {
            "agent": "AnyCompany Customer Agent",
            "status": "Running locally - $0.00 cost",
            "mode": "Broke mode - mock LLM, no Bedrock",
            "tools": ["get_order_history", "check_product", "return_item"],
            "message": "Hello! I'm AnyCompany Shop assistant. How can I help? (This is Lab 200 - no EKS needed)"
        }
        self.wfile.write(json.dumps(response, indent=2).encode())

    def log_message(self, format, *args):
        return  # quiet

print("🚀 AnyCompany Customer Agent starting on http://localhost:8080 - $0.00 cost")
print("📦 Workshop name = anycompany (correct, not your company name)")
print("💰 AWS Cost = $0.00 - running locally, not on EKS")
HTTPServer(("0.0.0.0", 8080), AgentHandler).serve_forever()

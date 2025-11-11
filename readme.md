python -m venv venv

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

python get-pip.py

pip install -r  requirements.txt  


# Get Api keys
# Open Api key

https://platform.openai.com/docs/overview

#hugging face portal
https://huggingface.co/


# prepare env
pip install transformers datasets accelerate

# example trainer script (train_intent.py) - use Hugging Face 
python train_intent.py --model distilbert-base-uncased --data my_intent_dataset.csv


# Step-by-Step Setup for Grafana Dashboard (with Prometheus)
# Step 1 — Install and Start Prometheus

    #Option 1: via Docker (recommended)

    docker run -d --name=prometheus -p 9090:9090 prom/prometheus


    # Option 2: manual setup

    Download from https://prometheus.io/download/

    # Extract and edit prometheus.yml:

    scrape_configs:
    - job_name: "smartassist"
        static_configs:
        - targets: ["localhost:8000"]

# Step 2 — Install and Start Grafana

Using Docker

docker run -d --name=grafana -p 3000:3000 grafana/grafana


Default Login:

Username: admin

Password: admin

⚙️ Step 3 — Expose Metrics from Python Services

Each sub-task (Chat, Intent, RAG, CV, ASR) should expose metrics using prometheus_client.

Install it:

pip install prometheus_client


In each service (or a combined monitor.py), add:

from prometheus_client import Counter, Histogram, start_http_server
import time, random

# Start metrics server (e.g., http://localhost:8000/metrics)
start_http_server(8000)

REQUEST_COUNT = Counter("requests_total", "Total number of requests", ["service"])
REQUEST_ERRORS = Counter("requests_errors_total", "Total errors", ["service"])
REQUEST_LATENCY = Histogram("request_latency_seconds", "Latency per service", ["service"])

def simulate_request(service):
    start = time.time()
    try:
        # simulate work
        time.sleep(random.uniform(0.2, 1.5))
        if random.random() < 0.1:
            raise Exception("Simulated error")
        latency = time.time() - start
        REQUEST_LATENCY.labels(service).observe(latency)
        REQUEST_COUNT.labels(service).inc()
    except Exception:
        REQUEST_ERRORS.labels(service).inc()

if __name__ == "__main__":
    print("🚀 Metrics server running at http://localhost:8000/metrics")
    while True:
        for s in ["chat", "intent", "rag", "cv", "asr"]:
            simulate_request(s)


✅ This exposes metrics like:

# HELP request_latency_seconds Latency per service
# TYPE request_latency_seconds histogram
request_latency_seconds_bucket{service="chat",le="0.5"} 2.0

📊 Step 4 — Add Prometheus as Data Source in Grafana

Open Grafana → http://localhost:3000

Go to Settings → Data Sources → Add data source

Choose Prometheus

Set URL → http://localhost:9090

Click Save & Test

🧩 Step 5 — Create Dashboard Panels

Create new dashboard → Add panels like:

🔹 Panel 1: Request Latency

Query:

histogram_quantile(0.95, sum(rate(request_latency_seconds_bucket[1m])) by (le, service))


Title: P95 Latency per Service

Visualization: Line chart

🔹 Panel 2: Request Count

Query:

rate(requests_total[1m])


Title: Requests per Service

Visualization: Bar chart

🔹 Panel 3: Error Rate

Query:

(sum(rate(requests_errors_total[1m])) by (service)) 
/ (sum(rate(requests_total[1m])) by (service))


Title: Error Rate (%)

Visualization: Time series or gauge

🔹 Panel 4: Service Heatmap

Query:

sum by (service) (rate(request_latency_seconds_sum[1m]))


Title: Service Load

Visualization: Heatmap

🖼️ Example Layout (student-style report diagram)
┌───────────────────────────────┐
│   SmartAssist Metrics Dashboard │
├───────────────────────────────┤
│  [ P95 Latency per Service  ]  │  ⟶  line chart
│  [ Error Rate Gauge         ]  │  ⟶  red if >10%
│  [ Request Count Histogram   ] │  ⟶  volume visualization
│  [ Service Heatmap (Load)   ]  │  ⟶  per-service traffic
└───────────────────────────────┘

📈 Step 6 — (Optional) Simulate Real Data from Your AI Tasks

Each module (chat, intent, etc.) should push metrics using the same labels:

REQUEST_LATENCY.labels("chat").observe(duration)
REQUEST_ERRORS.labels("chat").inc()


This allows the Grafana dashboard to automatically update with your model’s live data.

✅ Step 7 — Snapshot for Submission

Once graphs show data:

Click Share → Snapshot → Create Public Snapshot

Copy snapshot link or export as PNG.

Add to your report with caption:

“Figure X: Grafana Dashboard showing model latency and error metrics for SmartAssist pipeline.”
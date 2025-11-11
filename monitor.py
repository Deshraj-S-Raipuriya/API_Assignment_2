from prometheus_client import Counter, Histogram, start_http_server
import time, random

start_http_server(8000)

REQUEST_COUNT = Counter("requests_total", "Total number of requests", ["service"])
REQUEST_ERRORS = Counter("requests_errors_total", "Total errors", ["service"])
REQUEST_LATENCY = Histogram("request_latency_seconds", "Latency per service", ["service"])

def simulate_request(service):
    start = time.time()
    try:
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
    for _ in range(50):  # 🔁 run only 50 iterations instead of infinite
        for s in ["chat", "intent", "rag", "cv", "asr"]:
            simulate_request(s)
    print("✅ Simulation finished. You can now stop Prometheus/Grafana.")

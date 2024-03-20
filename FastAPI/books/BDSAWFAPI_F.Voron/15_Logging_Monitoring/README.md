# Instruction

## Commands

Run worker

```bash
PROMETHEUS_MULTIPROC_DIR=./assets/prometheus-tmp-dramatiq dramatiq_prom_db=./assets/prometheus-tmp-dramatiq dramatiq workers.worker
```

Run FastAPI App

```bash
uvicorn app:app --reload
```

Run Grafana Agent

```bash
./grafana-agent-linux-amd64 -config.file=agent-config.yaml
```

Test worker

```bash
python -m workers.worker
```

Install Grafana agent

```bash
curl -O -L "https://github.com/grafana/agent/releases/latest/download/grafana-agent-linux-amd64.zip" \
 && unzip "grafana-agent-linux-amd64.zip" \
 && chmod a+x grafana-agent-linux-amd64
```

Create Grafana Agent configuration file

```bash
cat << EOF > ./agent-config.yaml
metrics:
  global:
    scrape_interval: 60s
  configs:
    - name: hosted-prometheus
      scrape_configs:
        - job_name: node
          static_configs:
            - targets: ['localhost:9100']
      remote_write:
        - url: https://prometheus-prod-37-prod-ap-southeast-1.grafana.net/api/prom/push
          basic_auth:
            username: ""
            password: ""
EOF
```

## Links

- [Worker metrics](http://localhost:9191/metrics)

<!--
```bash

```
-->

import add_packages

from fastapi import FastAPI

from prometheus_fastapi_instrumentator import Instrumentator, metrics

from routers import router_test_logging, router_test_monitoring
#*=============================================================================
app = FastAPI()

app.include_router(
  router_test_logging.router, prefix="/test-logging", tags=["test-logging"],
)
app.include_router(
  router_test_monitoring.router, prefix="/test-monitoring", tags=["test-monitoring"],
)

instrumentator = Instrumentator()
# Enable default metrics
instrumentator.add(metrics.default()) 
# Wire it to FastAPI app and expose /metrics endpoint
instrumentator.instrument(app).expose(app)

#*=============================================================================

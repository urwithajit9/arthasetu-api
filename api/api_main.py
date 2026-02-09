from ninja import NinjaAPI
from api.routes.v1 import router as v1_router

api = NinjaAPI(title="ArthaSetu API", version="1.0.0")
api.add_router("/v1/", v1_router)

# FastApi
from fastapi                    import FastAPI
from fastapi.middleware.cors    import CORSMiddleware

# Controllers
from routers.lov        import lov
from routers.lov_vals   import lov_vals


app = FastAPI(title = 'Profile Back', description = 'My personal profile')


app.add_middleware(
    CORSMiddleware,
    allow_origins       = ["*"],
    allow_credentials   = True,
    allow_methods       = ["*"],
    allow_headers       = ["*"],
)


app.include_router(lov)
app.include_router(lov_vals)
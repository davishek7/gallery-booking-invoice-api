from fastapi import FastAPI, status, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from .configs.context_manager import lifespan
from .routes.gallery import router as gallery_router
from .routes.booking import router as booking_router
from .routes.auth import router as auth_router
from .routes.contact import router as contact_router
from .routes.admin_stat import router as admin_stat_router
from .exceptions.handlers import register_exception_handlers
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .configs.settings import settings
from .listeners import send_email_listener


app = FastAPI(
    title="Photo Gallery App API",
    description="This API handles Photo Gallery APIs.",
    version="1.0.0",
    contact={
        "name": "Avishek Das",
        "email": "davishek7@gmail.com",
    },
    lifespan=lifespan,
)

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

origins = ["http://localhost:5173", settings.DASHBOARD_APP_URL]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home_page(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Booking, Gallery App API",
            "subtitle": "This API handles Booking, Gallery, and Contacts made with FastAPI",
            "dashboard_app_url": settings.DASHBOARD_APP_URL,
            "api_docs": "/docs",
            "current_year": datetime.now().year,
        },
    )


URL_PREFIX = "/api"

app.include_router(auth_router, prefix=f"{URL_PREFIX}/auth", tags=["Auth"])
app.include_router(admin_stat_router, prefix=f"{URL_PREFIX}/admin", tags=["Stats"])
app.include_router(booking_router, prefix=f"{URL_PREFIX}/booking", tags=["Booking"])
app.include_router(gallery_router, prefix=f"{URL_PREFIX}/gallery", tags=["Gallery"])
app.include_router(contact_router, prefix=f"{URL_PREFIX}/contact", tags=["Contact"])

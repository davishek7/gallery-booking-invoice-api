from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from .configs.context_manager import lifespan
from .routes.gallery import router as gallery_router
from .routes.booking import router as booking_router


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

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

URL_PREFIX = "/api"

app.include_router(gallery_router, prefix=f"{URL_PREFIX}/gallery", tags=["Gallery"])
app.include_router(booking_router, prefix=f"{URL_PREFIX}/booking", tags=["Booking"])

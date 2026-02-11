from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.v1 import scan

app = FastAPI(
    title="E-Commerce Scanner AI",
    description="A scalable AI agent for scraping and analyzing e-commerce product pages.",
    version="1.0.0"
)

# CORS Configuration
# Allow all origins for simplicity in this demo, but restrict in production
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(scan.router, prefix="/api/v1", tags=["Scanning"])

# Mount static files (if any backend static assets are needed)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the frontend (simple workaround for single-file Vue app)
# In a real setup, we might use Nginx or a separate frontend server
from fastapi.responses import FileResponse

@app.get("/")
async def read_root():
    return FileResponse("app/templates/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)

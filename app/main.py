from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse
from app.core.config import settings
from app.api.v1 import scan

app = FastAPI(
    title="E-Commerce Scanner AI",
    description="A scalable AI agent for scraping and analyzing e-commerce product pages.",
    version="1.0.0",
    root_path=settings.ROOT_PATH
)

# CORS Configuration
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cookie Verification Dependency
async def verify_cookie(request: Request):
    auth_cookie = request.cookies.get("auth_session")
    if auth_cookie != "valid_session": # Simple check, can be enhanced with tokens
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    return True

# Include API routers - Protected
app.include_router(
    scan.router, 
    prefix="/api/v1", 
    tags=["Scanning"],
    dependencies=[Depends(verify_cookie)]
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    auth_cookie = request.cookies.get("auth_session")
    if auth_cookie == "valid_session":
        return FileResponse("app/templates/index.html")
    # Using Jinja2Template response would be better, but since we are using FileResponse for now,
    # we need to switch to TemplateResponse to pass variables, OR we can't pass variables to FileResponse.
    # Wait, the user has been using FileResponse. To pass 'root_path', we MUST use a template engine or client-side JS.
    # Let's switch to a simple string replacement or use Jinja2. The project has 'fastapi[all]' which includes jinja2.
    # checking requirements.txt... it has fastapi.
    # Let's try to just read the file and replace a placeholder, to avoid adding Jinja2 dependency if not present.
    # Actually, let's check if Jinja2 is installed.
    # requirements.txt doesn't explicitly list jinja2 but fastapi usually implies it for templates.
    # However, to be safe and minimal:
    with open("app/templates/login.html", "r") as f:
        content = f.read()
    # Replace a placeholder or inject the variable.
    # Let's assume we can use basic formatted string injection for this simple case to avoid dependencies.
    # But wait, the file is on disk.
    
    # Let's switch to returning HTMLResponse with substituted content.
    return HTMLResponse(content=content.replace("{{ root_path }}", settings.ROOT_PATH))

@app.post("/login")
async def login(password: str = Form(...)):
    if password == settings.ACCESS_PASSWORD:
        # Redirect to root (respecting root_path of the app)
        response = RedirectResponse(url=f"{settings.ROOT_PATH}/", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="auth_session", value="valid_session", httponly=True)
        return response
    
    # Return login page with error (simplified for now, just reload login)
    return FileResponse("app/templates/login.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)

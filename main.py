import os
import uuid

from fastapi import FastAPI, Response, Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from playwright.async_api import async_playwright
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import httpx


engine = create_engine(
    "sqlite:///./test.db",
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

class FeedbackDB(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    feedback = Column(String)

Base.metadata.create_all(bind=engine)


app = FastAPI()

api_keys = [
    "SCAPICGLg66znNb6vzsuC",
    "SCAPIUT8ghO0aaoUZqcrh",
    "SCAPIvONKOg9eudJZDVeh",
    "SCAPIjEQwaF86A6FeejCF",
    "SCAPI6xmt2DJLZet7iIwP",
    "SCAPIzDTyYtZCIQehjtUJ",
    "SCAPI9ERHV1V5scuLK6H1",
    "SCAPI92yktnfcB8WwN24I",
    "SCAPIUD5MPOLIxfxJUf0T",
    "SCAPIXGEycIltO5jBYJzF",
    "SCAPICnQntKyPYc3KvVg0",
    "SCAPI4CKKk6uaFkdPr5z6",
    "SCAPIhoAbT8kIXsL2dUBE",
    "SCAPInZBGTM4bisx3CLBy",
    "SCAPIO4gYOW3vY5l14MGE",
    "SCAPISDStebEnNd78E1xT",
    "SCAPIm19gHvSRENoxI8Ys",
    "SCAPI61bXh623nLci5qGN",
    "SCAPI0o6WGgAklGXccZbQ",
    "SCAPI7TS1MOi2RJZ913oz",
    "SCAPIf3BPpDG5hcKB6mMd",
    "SCAPIBk1b3rtpNJWL8OGm",
    "SCAPIAMYAvg7uRvvPhrmr",
    "SCAPIK4fIsQDPuAlpSMKH",
    "SCAPI8GzARh6J6kTGUAeu",
    "SCAPIYwdgo2kVucR5SwAT",
    "SCAPIgif7xZRpqPyGvHTS",
    "SCAPI7JgwP2hUC6cHiHZ5",
    "SCAPIMqqAyvTomQsDDhMD",
    "SCAPIup97y7pY3iVb91Px",
    "SCAPIOb2mJcgXeUZZ6y59",
    "SCAPISgp46rVJ5kp7JkEt",
    "SCAPIv7jbO5e99FBv6YAK",
    "SCAPIjJnku9pYADh2Qjux",
    "SCAPILWMQwXm6D8ws0xQa",
    "SCAPIVIt7hZVjmqa7WWQn",
    "SCAPI8uhIDZS709PXr7aC",
    "SCAPI5umJBSLdTpQagDxY",
    "SCAPI4hwdVusLPsym9wKV",
    "SCAPIuEXJj7zRVQ83zYKn",
    "SCAPIuqJxuSKTzId2GWeT",
    "SCAPI0RG1WfnllIcYDDX0",
    "SCAPILd86wImE1d6jfxt5",
    "SCAPIGdzS7WPzoAbWG470",
    "SCAPIisWJlK5MIiDVli7m",
    "SCAPI9u3kKXjPjPBXXxKv",
    "SCAPIhbusiI9V6KPkQ0iF",
    "SCAPItQdc0e6O0S5JawND",
    "SCAPI2MaGGbxqIxqYQJGt",
    "SCAPIRbv0P9zayWwqR4rN",
]

@app.exception_handler(Exception)
async def global_error(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "detail": str(exc)}
    )

class Feedback(BaseModel):
    feedback: str
    name: str

@app.get("/website-info/{domain}")
async def website_info(domain: str):

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://dns.google/resolve?name={domain}"
        )

    return response.json()

@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)

@app.get("/{api_key}/{my_path}")
async def screenshot(api_key: str, my_path: str):
    if api_key not in api_keys:
        return JSONResponse(
            status_code=401,
            content={"Error": "Enter a valid API key to continue."}
        )
    if my_path == "about":
        return {"about": "ScreenshotAPI was created to make developers' lives easier! Simply use it anywhere you can call an API, and need a screenshot of a website embedded into, well, anywhere you can call an API :) For full usage docs, see /docs"}

    elif "fullpage" in my_path:
        target = my_path.replace(", fullpage", "")
        screenshot_path = f"screenshot-{uuid.uuid4().hex}.png"
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            try:
                page = await browser.new_page()
                await page.goto(f"https://{target}")
                await page.screenshot(path=screenshot_path, full_page=True)
            finally:
                await browser.close()
        return FileResponse(
            screenshot_path,
            media_type="image/png",
            background=_cleanup(screenshot_path),
        )

    elif "fullpage" not in my_path and my_path != "howtouse":
        screenshot_path = f"screenshot-{uuid.uuid4().hex}.png"
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            try:
                page = await browser.new_page()
                await page.goto(f"https://{my_path}")
                await page.screenshot(path=screenshot_path, full_page=False)
            finally:
                await browser.close()
        return FileResponse(
            screenshot_path,
            media_type="image/png",
            background=_cleanup(screenshot_path),
        )

    else:
        return {"How to use": "How to use: To run a GET, simply type '/example.com' (replace example.com with the website you want to screenshot! To screenshot a full page (top to bottom), simply add ', fullpage' to the end of the GET. For example, '/example.com, fullpage'. Other GET requests include: /about"}

@app.post("/feedback/", status_code=201)
def get_feedback(user: Feedback):

    db = SessionLocal()
    try:
        item = FeedbackDB(
            name=user.name,
            feedback=user.feedback
        )
        db.add(item)
        db.commit()
    finally:
        db.close()
    return {
        "message": "Feedback submitted successfully",
        "user_data": user.model_dump()
    }

@app.get("/feedback")
def list_feedback(page: int = 1, size: int = 10):
    db = SessionLocal()
    try:
        offset = (page - 1) * size
        results = (
            db.query(FeedbackDB)
            .offset(offset)
            .limit(size)
            .all()
        )
        return results
    finally:
        db.close()

@app.get("/status")
def status():
    return {"status": "ok"}


def _cleanup(path: str):
    from starlette.background import BackgroundTask

    def remove():
        try:
            os.remove(path)
        except OSError:
            pass

    return BackgroundTask(remove)

@app.get("/headers/{domain}")
async def http_headers(domain: str):
    async with httpx.AsyncClient(follow_redirects=True, timeout=10) as client:
        r = await client.get(f"https://{domain}")
    return dict(r.headers)
@app.get("/ip-geo/{ip}")
async def ip_geo(ip: str):
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"http://ip-api.com/json/{ip}")
    return r.json()
@app.get("/title/{url}")
async def page_title(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        try:
            page = await browser.new_page()
            await page.goto(f"https://{url}")
            title = await page.title()
        finally:
            await browser.close()
    return {"url": url, "title": title}
@app.get("/wordcount")
def word_count(text: str):
    words = text.split()
    return {"words": len(words), "chars": len(text), "unique": len(set(words))}
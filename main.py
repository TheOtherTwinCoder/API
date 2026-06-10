from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from playwright.async_api import Request, async_playwright
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from fastapi.responses import JSONResponse
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
        return {"Error":"Enter a valid API key to continue."}
    if my_path == "about":
        return {"about": "ScreenshotAPI was created to make developers' lives easier! Simply use it anywhere you can call an API, and need a screenshot of a website embedded into, well, anywhere you can call an API :) Other GET requests: /howtouse"}
    
    elif "fullpage" in my_path:
        async with async_playwright() as p:
            extra = my_path.replace(", fullpage", "")
            print(extra)
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(f"https://{extra}")
            screenshot_path = "screenshot.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            await browser.close()
        return FileResponse(screenshot_path, media_type="image/png")
        
    elif "fullpage" not in my_path and my_path != "howtouse":
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(f"https://{my_path}")
            screenshot_path = "screenshot.png"
            await page.screenshot(path=screenshot_path, full_page=False)
            await browser.close()
        return FileResponse(screenshot_path, media_type="image/png")
        
    else:
        return {"How to use": "How to use: To run a GET, simply type '/example.com' (replace example.com with the website you want to screenshot! To screenshot a full page (top to bottom), simply add ', fullpage' to the end of the GET. For example, '/example.com, fullpage'. Other GET requests include: /about"}
@app.post("/feedback/", status_code=201)
def get_feedback(user: Feedback):

    db = SessionLocal()
    item = FeedbackDB(
        name=user.name,
        feedback=user.feedback
    )
    db.add(item)
    db.commit()
    return {
        "message": "Feedback submitted successfully",
        "user_data": user.model_dump() 
    }
@app.get("/feedback")
def list_feedback(page: int = 1, size: int = 10):
    db = SessionLocal()
    offset = (page - 1) * size
    results = (
    db.query(FeedbackDB)
    .offset(offset)
    .limit(size)
    .all()
    )
    return results

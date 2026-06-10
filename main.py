from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from playwright.async_api import async_playwright
from pydantic import BaseModel 

app = FastAPI()

class Feedback(BaseModel):
    feedback: str
    name: str

@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)

@app.get("/{my_path}")
async def screenshot(my_path: str):
    if my_path == "about":
        return {"about": "ScreenshotAPI was created to make developers' lives easier! Simply use it anywhere you can call an API, and need a screenshot of a website embedded into, well, anywhere you can call an API :) Other GET requests: /howtouse"}
    
    elif "fullpage" in my_path:
        async with async_playwright() as p:
            newpath = my_path
            extra = newpath.replace(", fullpage", "")
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
    return {
        "message": "Feedback submitted successfully",
        "user_data": user.model_dump() 
    }

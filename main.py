from fastapi import FastAPI, HTTPException
from playwright.async_api import async_playwright
import asyncio

app = FastAPI()

@app.get("/scrape")
async def scrape(gtin: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            await page.goto("https://www.gs1.org/services/verified-by-gs1", timeout=15000)
            await page.fill("#edit-gtin", gtin)
            await page.click("#edit-submit")
            await page.wait_for_selector(".views-field-title a", timeout=15000)
            
            company_elem = await page.query_selector(".views-field-title a")
            company_name = await company_elem.inner_text()
            
            await browser.close()
            return {"company": company_name}
        except Exception as e:
            await browser.close()
            raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

@app.get("/scrape")
def scrape(gtin: str):
    url = "https://www.gs1.org/services/verified-by-gs1"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return {"html_snippet": response.text[:500]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

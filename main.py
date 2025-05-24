from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

app = FastAPI()

@app.get("/scrape")
def scrape(gtin: str):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)
    try:
        driver.get("https://www.gs1.org/services/verified-by-gs1")
        time.sleep(5)

        input_box = driver.find_element("id", "edit-gtin")
        input_box.send_keys(gtin)

        submit_btn = driver.find_element("id", "edit-submit")
        submit_btn.click()

        time.sleep(5)

        # Buradaki selector'ı gerçek selector ile değiştirin:
        company_elem = driver.find_element("css selector", ".views-field-title a")
        company_name = company_elem.text

        return {"company": company_name}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        driver.quit()

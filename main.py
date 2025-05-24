from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

app = FastAPI()

@app.get("/scrape")
def scrape(gtin: str):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    try:
        driver.get("https://www.gs1.org/services/verified-by-gs1")
        time.sleep(5)

        input_box = driver.find_element(By.ID, "edit-gtin")
        input_box.send_keys(gtin)

        submit_btn = driver.find_element(By.ID, "edit-submit")
        submit_btn.click()

        time.sleep(5)

        company_elem = driver.find_element(By.CSS_SELECTOR, ".views-field-title a")
        company_name = company_elem.text

        return {"company": company_name}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import pandas as pd
from bs4 import BeautifulSoup

load_dotenv()
accounts = [
    {'login': os.getenv('LOGIN1'), 'password': os.getenv('PASSWORD1')},
    {'login': os.getenv('LOGIN2'), 'password': os.getenv('PASSWORD2')},
    {'login': os.getenv('LOGIN3'), 'password': os.getenv('PASSWORD3')},
    {'login': os.getenv('LOGIN4'), 'password': os.getenv('PASSWORD4')},]
url = os.getenv("URL")
all_data = []
options = webdriver.ChromeOptions()
options.add_argument("--headless")

for acc in accounts:
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    try:
        print('Wait until the login element is visible')
        user_input = wait.until(EC.visibility_of_element_located((By.ID, "username")))
        user_input.send_keys(acc["login"])
        print('Login loaded successfully')

        print('Wait until the password element is visible')
        user_pwd = wait.until(EC.visibility_of_element_located((By.ID, "password")))
        user_pwd.send_keys(acc["password"])
        print('Password loaded successfully') 

        print('Wait until the login button is visible')
        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']")))
        login_btn.click()
        print('Login button clicked successfully')

        print('Wait until the dashboard is visible')
        dashboard = wait.until(EC.visibility_of_element_located((By.ID, "divModule")))  
        print('Succesfully logged')
        
        print('Wait until the transcript element is visible')
        trnsct = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@href='?mod=transkript']")))
        trnsct.click()
        print('Successfully clicked on transcript')

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.select("tr")
        for row in rows:
            cells = row.select('td')
            if 7 < len(cells) <= 9:
                values = [cell.get_text(strip=True) for cell in cells]
                values.insert(0, acc["login"])
                all_data.append(values)       

    except Exception as e:
        print('Error:', e)

    finally:    
        print('Closing the browser')
        driver.quit()


columns = ["Login", "Course Code", "Title", "Credit", "ECTS", "Grade", "Letter", "Point", "Traditional"]
df = pd.DataFrame(all_data, columns=columns[:len(all_data[0])])

df = df[df["Course Code"].str.len() == 7]

df.to_csv("week1/all_transcripts.csv", index=False)
print('Successfully saved to all_transcripts.csv')
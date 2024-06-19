from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json

with open('creds.json', 'r') as jsonFile:
  credentials = json.load(jsonFile)

def main():
  url = "https://freesound.org/"
  driver = webdriver.Chrome()
  searchTerms =  ["microphone feedback", "mic feedback", "audio feedback", "live sound feedback", "PA feedback"]

  try:
    driver.get(url)
    print("Connected")
    
    try:
      login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-secondary[data-toggle='login-modal']"))
      )
      login_button.click()
      
      username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "id_username"))
      )
      username.send_keys(credentials['username'])
      
      pin = driver.find_element(By.ID, "id_password")
      pin.send_keys(credentials['pwd'])
      pin.send_keys(Keys.RETURN)
      print("Successfully Logged In")
    except:
      print("Login Failed")
        
    searchInput = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "search-sounds"))
    )
    searchInput.send_keys(searchTerms[0])
    searchInput.send_keys(Keys.RETURN)

    audioElements = driver.find_elements(By.CLASS_NAME, "bw-search__result")
    print(audioElements)

    for ele in audioElements: 
      duration = ele.find_element(By.CLASS_NAME, "bw-total__sound_duration")
      if float(duration.text.split(":")[0]) < 1.0:
        name = ele.find_element(By.CLASS_NAME, "bw-link--black")
        name.click()
        
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sound-download-button")))
        
        download = driver.find_element(By.CLASS_NAME, "sound-download-button")
        download.click()
        
        print("Downloading... ")
        driver.back()
        print("Download finsihed.")

    input("Press a key to exit....")


  finally:
    driver.quit()
  

if __name__ == "__main__":
  main()

import os
import json
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login(d):
  try:
    login_button = WebDriverWait(d, 10).until(
      EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-secondary[data-toggle='login-modal']"))
    )
    login_button.click()
    
    username = WebDriverWait(d, 10).until(
      EC.presence_of_element_located((By.ID, "id_username"))
    )
    username.send_keys(credentials['username'])
    
    pin = d.find_element(By.ID, "id_password")
    pin.send_keys(credentials['pwd'])
    pin.send_keys(Keys.RETURN)
    print("Successfully Logged In")
  except:
    print("Login Failed")
  
  
def downloadSample(url):
  print(url)
  if not os.path.exists("sound_samples"):
    os.makedirs("sound_samples")
        
  # Extract the filename from the URL
  filename = url.split("/")[-1]
  file_path = os.path.join("sound_samples", filename)
  
  try:
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
      # Write the content to a file
      with open(file_path, 'wb') as file:
        file.write(response.content)
      print(f"File downloaded successfully and saved to {file_path}")
    else:
      print(f"Failed to download file. HTTP Status Code: {response.status_code}")
  except Exception as e:
      print(f"An error occurred: {e}")
      

def main():
  url = "https://freesound.org/"
  driver = webdriver.Chrome()
  searchTerms =  ["microphone feedback", "mic feedback", "audio feedback", "live sound feedback", "PA feedback"]

  try:
    driver.get(url)
    print("Connected")
    
    login(driver)
    for searchTerm in searchTerms:
      searchInput = WebDriverWait(driver, 10).until(
          EC.element_to_be_clickable((By.ID, "search-sounds"))
      )
      searchInput.send_keys(searchTerm)
      searchInput.send_keys(Keys.RETURN)

      while True: 
        audioElements = driver.find_elements(By.CLASS_NAME, "bw-search__result")
        print("Audio Elements", audioElements)

        for ele in audioElements: 
          duration = ele.find_element(By.CLASS_NAME, "bw-total__sound_duration")
          if float(duration.text.split(":")[0]) < 1.0:
            srcFile = ele.find_element(By.XPATH, ".//source[@type='audio/ogg']")
            # print("Source", srcFile.get_attribute("src"))
            downloadSample(srcFile.get_attribute("src"))

        try:
          nextBtn = driver.find_element(By.XPATH, "//a[@title='Next Page']")
          driver.execute_script("arguments[0].scrollIntoView(true);", nextBtn)  # Scroll the button into view
          time.sleep(5)  # Wait a moment for the scroll action to complete
          nextBtn.click()
          time.sleep(3)
        except Exception as error:
          print("No more pages to navigate.")
          print(f"Error: {error}")
          break

    input("Press a key to exit....\n")

  finally:
    driver.quit()

if __name__ == "__main__":
  
  with open('creds.json', 'r') as jsonFile:
    credentials = json.load(jsonFile)
  
  main()
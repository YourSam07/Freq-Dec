from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def main():
  url = "https://freesound.org/"
  driver = webdriver.Chrome()
  searchTerms =  ["feedback", "audio feedback", "microphone feedback"]

  try:
    driver.get(url)
  finally:
    driver.quit()



if __name__ == "__main__":
  main()

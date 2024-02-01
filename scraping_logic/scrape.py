from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import os
from dotenv.main import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

site = os.getenv('SITE')




def create_webdriver_instance():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--disable-gpu")  
    chrome_options.add_argument("--no-sandbox")  
    chrome_options.add_argument("start-maximized")  
    chrome_options.add_argument("disable-infobars")  
    chrome_options.add_argument("--disable-extensions")  


    driver = webdriver.Chrome(options=chrome_options)
    return driver






async def scrapeNBAStats(data):

    player = data.player
    bet = data.bet
    driver = create_webdriver_instance()
    driver.get(site)

    time.sleep(2)

    stat_keys = driver.find_elements(By.CSS_SELECTOR, '.row-1.odd')
    print(stat_keys[0].text)

    statKeys = stat_keys[0].text


    tbody = driver.find_elements(By.CSS_SELECTOR, 'tbody.row-hover')[0]

    rows = tbody.find_elements(By.TAG_NAME, 'tr')

    for row in rows:
        if player in row.text:
            player_stats = row.text
            print(player_stats)
            break

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(2)

    glossary_div = driver.find_element(By.CLASS_NAME, 'x-columnize')
    glossary_text = glossary_div.text

    print(glossary_text)
    driver.quit()

    analyzation = await analyzeStats( player, statKeys, player_stats, glossary_text, bet)

    return analyzation


async def analyzeStats(player, statKeys, stats, glossary, bet):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a master sports better and are playing a prop bet"},
        {"role": "user", "content": f"You are betting on NBA player {player}. You are going to be betting that he will get {bet}. This is the stats table for him: \n {statKeys} \n {stats} \n Here is a glossary of what the stats mean: {glossary}. Do you think it's better to bet over or under? if so, why?"}
    ]
    )

    analyzation = completion.choices[0].message.content

    print(analyzation)

    return analyzation
    

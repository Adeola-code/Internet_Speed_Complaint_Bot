import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from decouple import config
PROMISED_UP = 150
PROMISED_DOWN = 20
USERNAME = config('USERNAME')
PASSWORD = config('PASSWORD')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)


class InternetSpeedTwitterBot:
    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://www.speedtest.net/")
        self.driver.maximize_window()
        self.down = PROMISED_DOWN
        self.up = PROMISED_UP

    def get_internet_speed(self):
        time.sleep(2)
        continue_button = self.driver.find_element(By.XPATH, value='//*[@id="onetrust-accept-btn-handler"]')
        continue_button.click()
        print("continue clicked")
        time.sleep(3)
        Go_button = self.driver.find_element(By.XPATH,
                                             value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a')
        Go_button.click()
        time.sleep(60)
        try:
            billion_button = self.driver.find_element(By.XPATH,
                                                      value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[8]/div/div/p[2]/button')
            billion_button.click()
            time.sleep(3)
        except:
            pass
        down_speed = self.driver.find_element(By.XPATH,
                                              value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span')
        up_speed = self.driver.find_element(By.XPATH,
                                            value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span')
        print(down_speed.text, up_speed.text)
        print("speed found")

        return f"{down_speed.text} mbps down/{up_speed.text} mbps up"

    def tweet_at_provider(self, upanddown):

        self.driver.get("https://twitter.com/i/flow/login")
        time.sleep(2)
        username = self.driver.find_element(By.NAME, value="text")
        username.send_keys(USERNAME)
        next_button = self.driver.find_element(By.XPATH,
                                               value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]')
        next_button.click()
        time.sleep(5)
        password = self.driver.find_element(By.NAME, value="password")
        password.send_keys(PASSWORD)
        time.sleep(1)
        login_button = self.driver.find_element(By.XPATH,
                                                value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div')
        login_button.click()
        print("twitter login done")
        time.sleep(10)
        tweet = self.driver.find_element(By.XPATH,
                                         value='//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a')
        tweet.click()
        if float(upanddown[0:4]) <= int(self.up) or float(upanddown[16:20]) <= int(self.down) <= 30:
            time.sleep(5)
            # Find and click the compose button to open the tweet box
            compose_button = self.driver.find_element(By.XPATH,
                                                      value='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[1]/div[2]/div/div/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div')
            compose_button.click()

            # Switch to the tweet input element and send keys to it
            tweet_input = self.driver.find_element(By.XPATH,
                                                   value='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[1]/div[2]/div/div/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div/div/div/div')
            tweet_input.send_keys(
                f"Hey ISP, why is my internet speed {upanddown} when I pay for {self.down} mbps down/{self.up} mbps up")

            # Then, find the post button and click it
            post_button = self.driver.find_element(By.XPATH,
                                                   value='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div/div[4]')
            post_button.click()


        else:
            print("Internet speed is satisfactory")


bot = InternetSpeedTwitterBot()

upanddown = bot.get_internet_speed()
bot.tweet_at_provider(upanddown)

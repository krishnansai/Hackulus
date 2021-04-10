import itertools,sys

from explicit import waiter, XPATH
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep

def login(driver):
    username = "cl_me_krrish"  # <username here>
    password = "Gokul@321"  # <password here>

    # Load page
    driver.get("https://www.instagram.com/accounts/login/")
    sleep(3)
    # Login
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    submit = driver.find_element_by_tag_name('form')
    submit.submit()

    # Wait for the user dashboard page to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.LINK_TEXT, "See All")))


def scrape_followers(driver, account,members):
    # Load account page
    driver.get("https://www.instagram.com/{}/".format(account))

    sleep(4)
    driver.find_element_by_partial_link_text("follower").click()

    # Wait for the followers modal to load
    waiter.find_element(driver, "//div[@role='dialog']", by=XPATH)
    allfoll = int((driver.find_element_by_xpath("//li[2]/a/span").text).replace(",", ""))
    posts = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span').text
    print(allfoll)
    print("Posts ", posts)

    follower_css = "ul div li:nth-child({}) a.notranslate"  # Taking advange of CSS's nth-child functionality
    for group in itertools.count(start=1, step=12):
        for follower_index in range(group,group+12):
            if follower_index > members:
                return None

            yield [waiter.find_element(driver, follower_css.format(follower_index)).text,allfoll,posts]
        last_follower = waiter.find_element(driver, follower_css.format(group + 11))
        driver.execute_script("arguments[0].scrollIntoView();", last_follower)


def main():
    account ="cl_me_krrish"
  
    driver = webdriver.Firefox(executable_path="./geckodriver")
    acc_name=[]
    try:
        login(driver)
        print('Followers of the "{}" account'.format(account))
       
        for count, follower in enumerate(scrape_followers(driver, account=account,members=10), 1):
            acc_name.append(follower[0])
    finally:
        follower_count = []
        posts = []
        for i in acc_name:
            for count, f in enumerate(scrape_followers(driver, account=i,members=6), 1):
                if f[1] not in follower_count:
                    follower_count.append(f[1])
                    posts.append(f[2])
        print("Followers ", follower_count)

        final_data = {}
        temp = {}
        for i in range(len(acc_name)):
            temp["Post_count"] = posts[i-1]
            temp["Followers"] = follower_count[i-1]

            final_data[acc_name[i]] = temp

            temp = {}
        wanted_list = []
        for x, y in final_data.items():
            if y["Post_count"] == "1" and y["Followers"] < 35:
                wanted_list.append(x)

        driver.quit()
        return wanted_list

if __name__ == "__main__":
    a = main()
    print('The Fake ID in my account :')
    for i in a:
        print(i)


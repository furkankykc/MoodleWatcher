from datetime import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options


class Watcher:
    def __init__(self, username, password, driver_executable=None, chromeProfilePath=None):
        self.username = username
        self.password = password
        self.login_url = 'https://dys.mu.edu.tr/login/index_auth.php'
        self.wait = 5
        self.percent = 80
        if driver_executable is None:
            if os.name == 'posix':
                chromedriver = 'chromedriver'
            else:
                chromedriver = 'chromedriver.exe'
        else:
            chromedriver = driver_executable

        chromeProfilePath = '/Users/furkankykc/Library/Application Support/Google/Chrome/'
        chrome_options = webdriver.ChromeOptions()
        if chromeProfilePath is not None:
            chrome_options.add_argument("user-data-dir=" + chromeProfilePath)
            chrome_options.add_argument("profile-directory=Default")
        self.driver = webdriver.Chrome(chromedriver, options=chrome_options)

    def kill_adobe(self):
        import psutil
        for proc in psutil.process_iter():
            if proc.name() == 'Adobe Connect':
                proc.kill()

    def waitfor(self, t):
        import time
        format1 = '%Hs %Mdk %Ssn'
        format1 = '%Hs %Mdk %Ssn'
        format2 = '%Mdk %Ssn'
        format3 = '%Ssn'
        if 's ' in t:
            format = format1
        elif 'dk' in t:
            format = format2
        else:
            format = format3

        date_time = datetime.strptime(t, format)
        time_delta = date_time - datetime(1900, 1, 1)
        seconds = time_delta.total_seconds()
        print('Wait for ', seconds)
        time.sleep(seconds)

    def login(self):
        email = self.driver.find_element_by_xpath('//*[@id="u_name"]')
        passw = self.driver.find_element_by_xpath('//*[@id="pass"]')
        login = self.driver.find_element_by_xpath('//*[@id="loginbtn"]')
        email.clear()
        passw.clear()
        email.send_keys(self.username)
        passw.send_keys(self.password)
        login.click()

    'chrome//version'
    'Tarayıcıda'

    def run(self):
        self.driver.get("https://dys.mu.edu.tr")
        self.login()
        lessons = WebDriverWait(self.driver, 100).until(
            lambda x: x.find_elements_by_css_selector('h3.coursename>a.aalink'))
        lessons = [(l.get_attribute('href'), l.get_attribute('innerHTML')) for l in lessons]
        import time
        for i in range(6, len(lessons)):
            try:
                if self.wait is not None:
                    time.sleep(self.wait)
                self.driver.get(lessons[i][0])
                lesson = self.driver.find_element_by_css_selector(
                    'div.activityinstance>a')  # add foreach top of this line so it couldnt miss any lesson
                self.driver.get(lesson.get_attribute('href'))
                watchings = self.driver.find_elements_by_class_name('aconrecordingrow')
                # watch_list = [w for w in watchings if not '% 100' in w.find_elements_by_css_selector('td')[-1]]
                watch_list = [w for w in watchings if not self.percent <= int(
                    w.find_elements_by_css_selector('td')[-1].get_attribute('innerHTML').replace('% ', ''))]
                # for i in watchings:
                #     complete = i.find_elements_by_css_selector('td')[-1].get_attribute('innerHTML')
                #     t = i.find_elements_by_css_selector('td')[-2].get_attribute('innerHTML')
                #     name = i.find_elements_by_css_selector('td')[-3].get_attribute('innerHTML')
                #     link = i.find_elements_by_css_selector('td')[-4].get_attribute('innerHTML')
                for i in watch_list:
                    t = i.find_elements_by_css_selector('td')[-2].get_attribute('innerHTML')
                    complete = i.find_elements_by_css_selector('td')[-1].get_attribute('innerHTML')
                    self.driver.get(
                        i.find_element_by_css_selector('a').get_attribute('href') + '&launcher=false&proto=false')
                    if self.driver.current_url == self.login_url:
                        self.login()
                    self.waitfor(t)
                    self.kill_adobe()
            except:
                print(lessons[i][1], 'Bulunamadi')

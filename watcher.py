from datetime import datetime
import os
from mimetypes import init

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time


class Lesson:
    def __init__(self, name, duration, link, percent, status, date, remaining, course):
        self.course = course
        self.name = name
        self.duration = duration
        self.link = link
        self.percent = percent
        self.status = status
        self.date = date
        self.remaining = remaining

    def __str__(self):
        return f'{self.name} / {self.percent} /{self.remaining}/ {self.status}/'


class Watcher:
    def __init__(self, username, password, driver_executable=None,
                 chromeProfilePath='/Users/furkankykc/Library/Application Support/Google/Chrome/'):
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

        # chromeProfilePath = '/Users/furkankykc/Library/Application Support/Google/Chrome/'
        chrome_options = webdriver.ChromeOptions()
        if chromeProfilePath is not None:
            chrome_options.add_argument("user-data-dir=" + chromeProfilePath)
            chrome_options.add_argument("profile-directory=Default")
        self.driver = webdriver.Chrome(executable_path='/Users/furkankykc/PycharmProjects/MoodleWatcher/chromedriver',
                                       options=chrome_options)
        self.watch_list = []

    def kill_adobe(self):
        import psutil
        for proc in psutil.process_iter():
            if proc.name() == 'Adobe Connect':
                proc.kill()

    def waitfor(self, t):

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
        self.driver.get("https://dys.mu.edu.tr")
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

    def getCourses(self):
        lessons = WebDriverWait(self.driver, 100).until(
            lambda x: x.find_elements_by_css_selector('h3.coursename>a.aalink'))
        lessons = [(l.get_attribute('href'), l.get_attribute('innerHTML')) for l in lessons]
        return lessons

    def open_course(self, lesson):
        # open course bazen course olmayan seyleri aciyor mesela quiz veya rapor gibi
        self.driver.get(lesson)
        lesson = self.driver.find_element_by_css_selector(
            'div.activityinstance>a')  # add foreach top of this line so it couldnt miss any lesson
        self.driver.get(lesson.get_attribute('href'))
        # <span class="accesshide "> Adobe Connect</span>
    def getLessons(self):
        array = []
        watchings = self.driver.find_elements_by_class_name('dashboard-card')
        # [w.find_element_by_tag_name('a').get_attribute('href') for w in watchings]
        for w in watchings:
            link = w.find_element_by_tag_name('a').get_attribute('href')
            name = w.find_element_by_class_name('multiline').text
            date = w.find_element_by_class_name('ml-2').text
            percent = w.find_elements_by_css_selector(".text-center.mb-2")[0].find_element_by_tag_name('div').text
            try:
                remaining = w.find_elements_by_css_selector(".time-remaining.bold.text-danger.mt-2")[0].text
                duration = w.find_elements_by_css_selector(".time-remaining.bold.text-danger.mt-2")[0].get_attribute(
                    'data-seconds')
                status = True
            except Exception as ex:
                remaining = ''
                duration = ''
                status = False
                continue
            percent = percent.replace('Tamamlanma: %', '')
            array.append(Lesson(name, duration, link, percent, status, date, remaining,course=''))
        return array

    def getUnwatchedLessons(self, watchings):
        # watch_list = [w for w in watchings if not self.percent <= int(
        #     w.find_elements_by_css_selector('td')[-1].get_attribute('innerHTML').replace('% ', ''))]
        watch_list = [w for w in watchings if w.status]
        return watch_list

    def watchLesson(self, lesson, waitFor=True):
        # t = lesson.find_elements_by_css_selector('td')[-2].get_attribute('innerHTML')
        # complete = lesson.find_elements_by_css_selector('td')[-1].get_attribute('innerHTML')
        # self.driver.get(
        #     lesson.find_element_by_css_selector('a').get_attribute('href') + '&launcher=false&proto=false')
        self.driver.get(lesson.link + '&launcher=false&proto=false')
        if self.driver.current_url == self.login_url:
            self.login()

        if waitFor:
            # self.waitfor(lesson.duration)
            time.sleep(int(lesson.duration))
            self.kill_adobe()

    def run(self):
        self.login()
        lessons = self.getCourses()
        import time
        for i in range(6, len(lessons)):
            try:
                if self.wait is not None:
                    time.sleep(self.wait)
                self.open_course(lessons[i][0])

                watchings = self.getLessons()
                self.watch_list.extend(self.getUnwatchedLessons(watchings))

            except:
                print(lessons[i][1], 'Bulunamadi')

        # for i in watch_list:
        #     self.watchLesson(i)
        [print(i) for i in self.watch_list]

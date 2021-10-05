from datetime import datetime
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time


class ThereIsNoLinkToConnect(Exception):

    def __init__(self, message="Tried to fetch lesson link but there is no related link"):
        self.message = message
        super().__init__(self.message)


class ThereIsNoActivity(Exception):

    def __init__(self, message="Tried to fetch lesson link but there is no activity at all"):
        self.message = message
        super().__init__(self.message)


class Course:
    def __init__(self, name, page_url, lessons: list = None):
        self.name = name
        self.page_url = page_url
        self.lessons = lessons if lessons else []

    def get_unwatched_lessons(self):
        # watch_list = [w for w in watchings if not self.percent <= int(
        #     w.find_elements_by_css_selector('td')[-1].get_attribute('innerHTML').replace('% ', ''))]
        watch_list = [w for w in self.lessons if w.status]
        return watch_list

    def __str__(self):
        return f'Name:{self.name}  \n\t' \
               f'Page_url:{self.page_url} \n\t' \
               f'Lessons:[{self.lessons}] \n\t'

    def __repr__(self):
        return self.__str__()


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
        return f'Name:{self.name}  \n\t' \
               f'Percent:{self.percent} \n\t' \
               f'Remaining:{self.remaining} \n\t' \
               f'Status:{self.status} \n\t' \
               f'Date:{self.date} \n\t'

    def __repr__(self):
        return self.__str__()


class Watcher:
    def __init__(self, username, password, driver_executable=None,
                 chrome_profile_path='/Users/furkankykc/Library/Application Support/Google/Chrome/'):
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

        # chromeProfilePath = None
        chrome_options = webdriver.ChromeOptions()
        if chrome_profile_path is not None:
            chrome_options.add_argument("user-data-dir=" + chrome_profile_path)
            chrome_options.add_argument("profile-directory=Default")
        self.driver = webdriver.Chrome(executable_path=chromedriver,
                                       options=chrome_options)
        self.watch_list = []
        self.courses = None
        self.rememberChoice = False
        self.openApp = True

    @staticmethod
    def kill_adobe():
        import psutil
        for proc in psutil.process_iter():
            if proc.name() == 'Adobe Connect':
                proc.kill()

    @staticmethod
    def waitfor(t):
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

        if self.driver.current_url == self.login_url:
            # email = self.driver.find_element_by_xpath('//*[@id="u_name"]')
            # passw = self.driver.find_element_by_xpath('//*[@id="pass"]')
            # login = self.driver.find_element_by_xpath('//*[@id="loginbtn"]')
            email = WebDriverWait(self.driver, 30).until(
                ec.element_to_be_clickable((By.XPATH, '//*[@id="u_name"]')))
            passw = WebDriverWait(self.driver, 30).until(
                ec.element_to_be_clickable((By.XPATH, '//*[@id="pass"]')))
            login = WebDriverWait(self.driver, 30).until(
                ec.element_to_be_clickable((By.XPATH, '//*[@id="loginbtn"]')))

            email.clear()
            passw.clear()

            email.send_keys(self.username)
            passw.send_keys(self.password)

            login.click()

    'chrome//version'
    'Tarayıcıda'

    def switch_to_popup(self):
        for handle in self.driver.window_handles:
            if handle != self.driver.current_window_handle:
                popup_page = handle
                self.driver.switch_to.window(popup_page)

    def handle_popup(self):
        "open-in-browser-button" """//*[@id="launchOptionsDialog"]/div[2]/coral-dialog-content/div[1]/div[1]"""
        "open-in-app-button" """//*[@id="launchOptionsDialog"]/div[2]/coral-dialog-content/div[1]/div[2]"""
        "coral-id-0" """//*[@id="coral-id-0"]"""
        if self.rememberChoice:
            rememberButton = self.driver.find_element_by_xpath('//*[@id="coral-id-0"]')
            rememberButton.click()
        if self.openApp:
            openAppButton = self.driver.find_element_by_xpath(
                '//*[@id="launchOptionsDialog"]/div[2]/coral-dialog-content/div[1]/div[2]')
            openAppButton.click()
        else:
            openBrowserButton = self.driver.find_element_by_xpath(
                '//*[@id="launchOptionsDialog"]/div[2]/coral-dialog-content/div[1]/div[1]')
            openBrowserButton.click()

    def click_watch_live_button(self):
        liveButton = self.driver.find_element_by_xpath('//*[@id="meetingsummary"]/form/div/div/div[2]/div')
        liveButton.click()

    def watch_live_course(self, course: Course):
        self.kill_adobe()
        self.open_course(course)
        self.click_watch_live_button()

    def watch_lesson(self, lesson, waitFor=True):
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

    def open_course(self, course: Course):
        # open course bazen course olmayan seyleri aciyor mesela quiz veya rapor gibi
        self.driver.get(course.page_url)
        try:
            lesson = self.driver.find_element_by_css_selector(
                'div.activityinstance>a')  # add foreach top of this line so it couldnt miss any lesson
        except:
            raise ThereIsNoActivity
        link = lesson.get_attribute('href')
        # print(link, str(link).find("adobeconnect"))

        if not str(link).find("adobeconnect") == -1:
            self.driver.get(link)
        else:
            raise ThereIsNoLinkToConnect
        # <span class="accesshide "> Adobe Connect</span>

    def get_courses(self):
        courses = WebDriverWait(self.driver, 100).until(
            lambda x: x.find_elements_by_css_selector('h3.coursename>a.aalink'))

        courses = [Course(course.get_attribute('innerHTML'), course.get_attribute('href')) for course in
                   courses]
        # initialize lessons

        courses = self.get_all_lessons(courses)
        return courses

    def get_lessons(self, course: Course):
        # if driver url not course url
        lessons = []
        try:
            self.open_course(course)
        except (ThereIsNoLinkToConnect, ThereIsNoActivity) as ex:
            print(ex)
            return course
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
            except:
                remaining = ''
                duration = ''
                status = False
            percent = percent.replace('Tamamlanma: %', '')
            lessons.append(Lesson(name, duration, link, percent, status, date, remaining, course=''))
        course.lessons = lessons
        return course

    def get_all_lessons(self, courses):
        return [self.get_lessons(course) for course in courses]

    def run(self, watch=False):
        self.login()
        self.courses = self.get_courses()
        # import time
        # for i in range(6, len(self.courses)):
        #     try:
        #         if self.wait is not None:
        #             time.sleep(self.wait)
        #         self.watch_list.extend(self.courses[i].getUnwatchedLessons())
        #
        #     except:
        #         print(self.courses[i], 'Bulunamadi')
        #
        # [print(i) for i in self.watch_list]
        # if watch:
        #     for i in self.watch_list:
        #         self.watchLesson(i)

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

uname = ''
passw = ''
login_url = 'https://dys.mu.edu.tr/login/index_auth.php'

chromedriver = '/Users/furkankykc/Downloads/chromedriver'
chromeProfilePath = '/Users/furkankykc/Library/Application Support/Google/Chrome/'

def kill_adobe():
    import psutil
    for proc in psutil.process_iter():
        if proc.name() == 'Adobe Connect':
            proc.kill()


def waitfor(t):
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


'''defaults write com.google.Chrome ExternalProtocolDialogShowAlwaysOpenCheckbox -bool true'''

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=" + chromeProfilePath)
chrome_options.add_argument("profile-directory=Default")

#
# prefs = {"protocol_handler.excluded_schemes": {"afp": True, "data": True, "disk": True, "disks": True, "file": True,
#                                                "hcp": True, "intent": True, "itms-appss": True, "itms-apps": True,
#                                                "itms": True, "market": True, "javascript": True, "mailto": True,
#                                                "ms-help": True, "news": True, "nntp": True, "shell": True, "sip": True,
#                                                "snews": False, "vbscript": True, "view-source": True,
#                                                "vnd": {"ms": {"radio": True}}}}
# prefs = {"protocol_handler": {"excluded_schemes": {"connectpro": "true"}}}

'https://forum.katalon.com/t/open-browser-with-custom-profile/19268'
# chrome_options.add_experimental_option("prefs", prefs)
# chrome_options.add_experimental_option(
#     'excludeSwitches',
#     ['disable-hang-monitor',
#      'disable-prompt-on-repost',
#      'disable-background-networking',
#      'disable-sync',
#      'disable-translate',
#      'disable-web-resources',
#      'disable-client-side-phishing-detection',
#      'disable-component-update',
#      'disable-default-apps',
#      'disable-zero-browsers-open-for-tests'])
driver = webdriver.Chrome(chromedriver, options=chrome_options)


# driver.execute_script("window.confirm = function(msg) { return true; }")
# '/Users/furkankykc/Library/Application Support/Google/Chrome/Default'
# 'connectpro:https://adobe-pool.mu.edu.tr/common/meetingAS3/shell/shell.swf?aicc_url=https%3A%2F%2Fadobe-pool.mu.edu.tr%2Fservlet%2Fverify%3Fsco-id%3D22339469%26airspeed%3D1&aicc_sid=oou3pwi4tde88fu7e3yqceken2q4cuvn&airspeed=1%2Flmsproxy%3Fsco-id%3D22339469%26sid%3Doou3pwi4tde88fu7e3yqceken2q4cuvn%26qdata%3D&baseurl=%2Fcommon%2FmeetingAS3%2Fshell%2F&plugin=plugin.swf&host=adobe-pool.mu.edu.tr&path=%2Fpxrzbc3m3jde%2F&proto=true&sco-id=22339469&session=breezgk47psgurninkx8p&ticket=oou3pwi4tde88fu7e3yqceken2q4cuvn&transcript-id=44721231&isLive=false&room=22339469;session=breezgk47psgurninkx8p&ticket=oou3pwi4tde88fu7e3yqceken2q4cuvn&proxy=false&appInstance=7/22339469-1/output/&ott=3i49535kzk&css=airspeed&fcsContent=true&pbMode=normal&conStrings=rtmps%3A%2F%2Fadobe-08-rtmp.mu.edu.tr%3A443%2F%3Frtmp%3A%2F%2Flocalhost%3A8506%2F&connectors=adobe-acts.mu.edu.tr&connector_proto=wss:443&lang=tr&account_id=7&streamName=/content/7/22339469-1/output/&spFixFlashPlayerVersion=10%2C1%2C50%2C469&hasHTMLContent=false&pacProxyFlag=false&pacProxyFlag=false&htmlUrl=https://adobe-pool.mu.edu.tr/pxrzbc3m3jde/?launcher=false&fcsContent=true&pbMode=normal&mode=auto&lang=tr&close_meeting=javascript:window.close();&isHTMLCustomPodEnabled=false&msg=view&hasHTMLContent=false&showLoginLogo=1'
def login(username, password):
    driver.get("https://dys.mu.edu.tr")
    print(driver.page_source.encode("utf-8"))
    email = driver.find_element_by_xpath('//*[@id="u_name"]')
    passw = driver.find_element_by_xpath('//*[@id="pass"]')
    login = driver.find_element_by_xpath('//*[@id="loginbtn"]')
    email.send_keys(username)
    passw.send_keys(password)
    login.click()


'chrome//version'
'Tarayıcıda'
login(uname, passw)
lessons = WebDriverWait(driver, 100).until(lambda x: x.find_elements_by_css_selector('h3.coursename>a.aalink'))

lessons = [(l.get_attribute('href'), l.get_attribute('innerHTML')) for l in lessons]
import time

for i in range(6, len(lessons)):
    try:

        time.sleep(5)
        driver.get(lessons[i][0])
        lesson = driver.find_element_by_css_selector('div.activityinstance>a')
        driver.get(lesson.get_attribute('href'))
        watchings = driver.find_elements_by_class_name('aconrecordingrow')
        # watch_list = [w for w in watchings if not '% 100' in w.find_elements_by_css_selector('td')[-1]]
        watch_list = [w for w in watchings if not 80 <= int(
            w.find_elements_by_css_selector('td')[-1].get_attribute('innerHTML').replace('% ', ''))]
        for i in watch_list:
            t = i.find_elements_by_css_selector('td')[-2].get_attribute('innerHTML')
            complete = i.find_elements_by_css_selector('td')[-1].get_attribute('innerHTML')
            print(i.find_element_by_css_selector('a').get_attribute('href') + '&launcher=false$html-view=true')
            driver.get(i.find_element_by_css_selector('a').get_attribute('href') + '&launcher=false&proto=false')
            if driver.current_url == login_url:
                login(uname, passw)
            waitfor(t)
            kill_adobe()
    except:
        print(lessons[i][1], 'Bulunamadi')

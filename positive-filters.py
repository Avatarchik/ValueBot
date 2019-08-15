from selenium import webdriver
import settings as st
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
pause_done=0
sleep_done=0
browser = webdriver.Chrome(executable_path=r'chromedriver.exe')
action=ActionChains(browser)
k_path=''

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

def random_num(a,b):
    random.seed()
    brk = a + random.random()*(b-a)
    return brk

def random_click(el):
    size=el.size
    h=size['height']
    w=size['width']
    action.move_to_element_with_offset(el, int(random_num(w/4,w*3/4)), int(random_num(h/4,h*3/4))).click()

def get_value(x):
    y = (((1) / ((1) / (x) - 0.045)) / (x) - 1)*100+0.1
    if y<9.1:
        y=9.1
    if x>=1.5 and x<1.75:
        y=10
    elif x>=1.75 and x<2.0:
        y=y+1.5
    elif x>=2.0 and x<3.0:
        y=y+2.0
    elif x>=3.0 and x<4.0:
        y=y+2.5
    elif x>=4.0 and x<5.0:
        y=y+3.0
    elif x>=5.0:
        y=y+4.0
    return float(toFixed(y, 2))

def update_bets():
    browser.find_element_by_id("btnRefresh").click()
    time.sleep(random_num(0.4, 0.6))

def update_calc():
    browser.find_element_by_id("aRefreshOdd1").click()
    time.sleep(random_num(0.8, 1))

def find_bet():
    global auto_update_timer
    update_bets()
    while True:
        if int(time.time())-auto_update_timer>25:
            time.sleep(random_num(0,2))
            update_bets()
            auto_update_timer=int(time.time())
        try:
            browser.find_element_by_class_name('addToCalc')
            print("Нашел ставку: " + str(time.ctime()))
            auto_update_timer=int(time.time())
            break
        except NoSuchElementException:
            pass

def write_log(x):
    f = open(k_path+'log.txt', 'a')
    f.write("\n" + x)
    f.close()

def write_to_bet_name_file(s):
    f = open(k_path+'placed_name.txt', 'a')
    f.write(s + "\n")
    f.close()

def check_max_one_game_count(s):
    f = open(k_path+'placed_name.txt', 'r')
    line=f.readline()
    counter=0
    while line:
        if s in line:
            counter=counter+1
            if counter > st.max_one_game_count:
                d = open(k_path+'black_list.txt', 'a')
                d.write(s + "\n")
                d.close()
                return
        line=f.readline()
    f.close()
    return

def check_black_list(s):
    f = open(k_path+'black_list.txt', 'r')
    line = f.readline()
    while line:
        if s in line:
            return 0
        line = f.readline()
    return 1

def get_bet_type(a):
    out=""
    if a==1:
        current_window = browser.current_window_handle
        browser.switch_to.window(browser.window_handles[0])
        bet_type = str(browser.find_element_by_xpath("//a[@id='lBet1']").text).split(' ')[0]
        if "Тб" in bet_type or "Тм" in bet_type:
            if "Тб" in bet_type:
                out="tb"
            else:
                out="tm"
            bet_type=bet_type[0:-1]
            bet_type=bet_type.split("(")
            out = out+bet_type[-1]
        browser.switch_to.window(current_window)
    if a==0:
        current_window = browser.current_window_handle
        browser.switch_to.window(browser.window_handles[1])
        WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        browser.switch_to.frame("bsFrame")
        bet_type = str(browser.find_element_by_xpath("//div[@class='bs-Selection_Desc']").text)
        splited=bet_type.split(" ")
        if splited[0]=="Under" or splited[0]=="Over":
            if splited[0]=="Under":
                out="tm"
                out = out + splited[1]
            if splited[0]=="Over":
                out="tb"
                out = out + splited[1]
        else:
            out=""

        browser.switch_to.window(current_window)
    return str(out)

browser.get("https://positivebet.com/ru/user/login")
element_username = browser.find_element_by_id("UserLogin_username")
element_pass = browser.find_element_by_id("UserLogin_password")
element_username.send_keys(st.login_pos)
element_pass.send_keys(st.pass_pos)
#action.move_to_element(browser.find_element_by_name("yt0")).click()
#random_click(browser.find_element_by_name("yt0"))
browser.find_element_by_name("yt0").click()
time.sleep(random_num(0.9,1.1))
#random_click(browser.find_element_by_link_text("Valuebets"))
browser.find_element_by_link_text("Valuebets").click()
time.sleep(random_num(0.9,1.1))
browser.find_element_by_id("btnSettings").click()
time.sleep(random_num(0.9,1.1))
browser.find_element_by_id("Settings_name").clear()
browser.find_element_by_id("Settings_name").send_keys("1-1.5")
time.sleep(random_num(0.9,1.1))

browser.find_element_by_id("Settings_minProfit").clear()
browser.find_element_by_id("Settings_minProfit").send_keys("9.01")
time.sleep(random_num(0.9,1.1))

browser.find_element_by_id("Settings_minOdds").clear()
browser.find_element_by_id("Settings_minOdds").send_keys("1.00")
time.sleep(random_num(0.9,1.1))

browser.find_element_by_id("Settings_maxOdds").clear()
browser.find_element_by_id("Settings_maxOdds").send_keys("1.5")
time.sleep(random_num(0.9,1.1))

browser.find_element_by_id("Settings_lifetime_min").clear()
browser.find_element_by_id("Settings_lifetime_min").send_keys("10")
time.sleep(random_num(0.9,1.1))

browser.find_element_by_id("Settings_initiator_involved_min").clear()
browser.find_element_by_id("Settings_initiator_involved_min").send_keys("10")
time.sleep(random_num(0.9,1.1))

browser.find_element_by_id("Sport_5_is_break").click()
time.sleep(random_num(0.9,1.1))

browser.find_element_by_id("Sport_7_is_break").click()
time.sleep(random_num(0.9,1.1))

browser.find_element_by_id("btnCheck_all").click()
time.sleep(random_num(0.9,1.1))

browser.find_element_by_xpath("input[@id='chkBooker_42_active', @type='checkbox']").click()
time.sleep(random_num(0.9,1.1))

browser.find_element_by_id("BetTypeGroupSport_104_active").click()
time.sleep(random_num(0.9,1.1))

browser.find_element_by_id("BetTypeGroupSport_26_active").click()
time.sleep(random_num(0.9,1.1))

browser.find_element_by_id("BetTypeGroupSport_45_active").click()
time.sleep(random_num(0.9,1.1))

browser.find_element_by_xpath("//button[@name='yt36']").click()
time.sleep(random_num(0.9,1.1))

print("Заебааали")



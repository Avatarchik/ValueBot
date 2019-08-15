from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import keyboard
import os
import configparser

auto_update_timer=0
on_p=0
pause_done=0
sleep_done=0
bet_counter=0

browser = webdriver.Chrome(executable_path=r'chromedriver.exe')
action=ActionChains(browser)

#Пути
k_path=os.getcwd()+'\\'
config_path=k_path+'config.txt'

#ЧТЕНИЕ НАСТРОЕК ИЗ КОНФИГА
config = configparser.ConfigParser()
config.read(config_path)
font = config.get("Settings", "max_one_game_count")
login_pos = config.get("Settings", "login_pos")
pass_pos = config.get("Settings", "pass_pos")
login_bet= config.get("Settings", "login_bet")
pass_bet= config.get("Settings", "pass_bet")
bet_mirror= config.get("Settings", "bet_mirror")
fix_bet= config.get("Settings", "fix_bet")
max_one_game_count=int(config.get("Settings", "max_one_game_count"))

def editConfig(a,b):
    config.set("Settings", a, b)
    with open(config_path, "w") as config_file:
        config.write(config_file)

def pause_bet():
    global on_p
    if on_p==0:
        on_p=1
        print("Стоп")
    else:
        on_p=0
        print("Продолжаем")

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
            if counter > max_one_game_count:
                d = open(k_path+'black_litxt', 'a')
                d.write(s + "\n")
                d.close()
                return
        line=f.readline()
    f.close()
    return

def check_black_list(s):
    f = open(k_path+'black_litxt', 'r')
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


keyboard.add_hotkey('ctrl+shift+s', pause_bet)
browser.get("https://positivebet.com/ru/user/login")
browser.execute_script("window.open('','_blank');")
time.sleep(random_num(0.5,0.9))
browser.switch_to.window(browser.window_handles[1])
time.sleep(0.5)
browser.get("chrome://extensions")
while not input()=="s":
   time.sleep(1)
browser.switch_to.window(browser.window_handles[0])
element_username = browser.find_element_by_id("UserLogin_username")
element_pass = browser.find_element_by_id("UserLogin_password")
element_username.send_keys(login_pos)
element_pass.send_keys(pass_pos)
#action.move_to_element(browser.find_element_by_name("yt0")).click()
#random_click(browser.find_element_by_name("yt0"))
browser.find_element_by_name("yt0").click()
time.sleep(random_num(1,1.5))
#random_click(browser.find_element_by_link_text("Valuebets"))
browser.find_element_by_link_text("Valuebets").click()
time.sleep(random_num(1.9,2.3))
#random_click(browser.find_element_by_id(auto_keff_update_checkbox))
browser.find_element_by_id("chkAutoUpdateOdd1").click()
browser.find_element_by_id("tfStake1").clear()
browser.find_element_by_id("tfStake1").send_keys(fix_bet)
time.sleep(random_num(0.9,1.5))
browser.find_element_by_id("btnAutoRefresh").click()
time.sleep(random_num(0.5, 0.9))
browser.execute_script("window.open('','_blank');")
time.sleep(random_num(0.9,1.3))
browser.switch_to.window(browser.window_handles[1])
time.sleep(random_num(1,1.3))
browser.get("http://"+ bet_mirror)
browser.find_element_by_link_text("English").click()
element_bet_username = WebDriverWait(browser, 5).until(
    EC.presence_of_element_located((By.XPATH, "//div[@class='hm-Login_UserNameWrapper ']/input")))
element_bet_username.send_keys(login_bet)
element_bet_pass = browser.find_element_by_xpath("//div[@class='hm-Login_PasswordWrapper ']/input")
element_bet_pass.click()
time.sleep(random_num(0.3,0.4))
element_bet_pass = browser.find_element_by_xpath("//div[@class='hm-Login_PasswordWrapper ']/input[@type='password']")
element_bet_pass.send_keys(pass_bet)
browser.find_element_by_xpath("//div[@class='hm-Login_PasswordWrapper ']/button").click()
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "hm-MembersInfoButton_Deposit ")))
time.sleep(random_num(3,3.2))
browser.close()
browser.switch_to.window(browser.window_handles[0])
update_bets()

print("Сколько ставок проставить???")
bet_count_to=int(input())
while True:
    write_log("\n-----------------------------------------------------------------\n")
    while bet_counter<bet_count_to:
        if on_p == 0:
            browser.switch_to.window(browser.window_handles[0])
            current_window = browser.current_window_handle
            try:
                print("")
                for i in browser.window_handles:
                    if not i == current_window:
                        browser.switch_to.window(i)
                        browser.close()
                        browser.switch_to.window(current_window)
            except:
                print("")
            time.sleep(random_num(0.9, 1.1))

            if bet_counter%80==0 and sleep_done==0 and not bet_counter==0:
                print("Ушли поспать")
                browser.find_element_by_xpath("//a[@href='/ru/user/logout']").click()
                time.sleep(random_num(1, 1.9))
                browser.execute_script("window.open('','_blank');")
                time.sleep(random_num(0.5, 0.9))
                browser.switch_to.window(browser.window_handles[0])
                time.sleep(random_num(1, 1.9))
                browser.close()
                time.sleep(1)
                browser.switch_to.window(browser.window_handles[0])
                time.sleep(random_num(1080,1500))
                browser.get("https://positivebet.com/ru/user/login")
                time.sleep(random_num(2, 2.9))
                browser.switch_to.window(browser.window_handles[0])
                element_username = browser.find_element_by_id("UserLogin_username")
                element_pass = browser.find_element_by_id("UserLogin_password")
                element_username.send_keys(login_pos)
                element_pass.send_keys(pass_pos)
                browser.find_element_by_name("yt0").click()
                time.sleep(random_num(1, 1.5))
                browser.find_element_by_link_text("Valuebets").click()
                time.sleep(random_num(1.9, 2.3))
                browser.find_element_by_id(auto_keff_update_checkbox).click()
                browser.find_element_by_id("tfStake1").clear()
                browser.find_element_by_id("tfStake1").send_keys(fix_bet)
                time.sleep(random_num(0.9, 1.5))
                browser.find_element_by_id("btnAutoRefresh").click()
                time.sleep(random_num(0.9, 1.5))
                print("Пришли сосна!")
                sleep_done=1

            if bet_counter%25==1:
                pause_done=0
            if not bet_counter==0 and bet_counter%25==0 and pause_done==0:
                print("Ушли пописать")
                time.sleep(random_num(180,360))
                print("Вернулись с писанья")
                pause_done=1
            try:
                find_bet()
                element_add_to_calc=WebDriverWait(browser, 3).until(
                     EC.presence_of_element_located((By.XPATH, "//*[@class='items table table-striped table-bordered table-condensed']/tbody/tr/td/a[@class='addToCalc']")))
                time.sleep(random_num(0.4, 0.8))
                element_add_to_calc.click()
                time.sleep(random_num(0.4,0.6))
                browser.find_element_by_class_name('hideBet').click()
                WebDriverWait(browser, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Только этот valuebet')]"))).click()
                etalon_preval= float(browser.find_element_by_id("lProfitForBoth").text[0:-1])
                etalon_kef=float(browser.find_element_by_xpath("//input[@id='tfCoef1']").get_attribute('value'))
                print("\tПереоценка " + str(etalon_preval ))
                print("\tКэф " + str(etalon_kef))
                bet_type_scen=get_bet_type(1)

                print(bet_type_scen)
                time.sleep(random_num(0.3,0.5))
                current_bet=str(browser.find_element_by_xpath("//*[@id='lEvent_name1']/b").text)
                print(current_bet)
                if not check_black_list(current_bet):
                    print("Слишком много ставок на этот матч!")
                    continue
                browser.find_element_by_id("btn_bet1").click()

                current_window = browser.current_window_handle
                old_windows = browser.window_handles

                WebDriverWait(browser, 5).until(EC.new_window_is_opened(old_windows))
                new_window = [i for i in browser.window_handles if i not in old_windows]
                browser.switch_to.window(new_window[0])

                try:
                    browser.find_element_by_xpath("//div[@id='error-information-popup-container']") #Если вылезла ошибкка при открытии бетки
                    print("Сайт не открылся! Следующая ставка.\n")
                    browser.close()
                    browser.switch_to.window(browser.window_handles[0])
                    continue
                except:
                    pass

                WebDriverWait(browser, 5).until(
                    EC.presence_of_element_located((By.TAG_NAME, "iframe")))
                browser.switch_to.frame("bsFrame")
                time.sleep(random_num(0.3,1))
                try:
                    element = WebDriverWait(browser, 11).until(
                            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Place Bet')]")))
                    print("Купон открыт.")
                except TimeoutException:
                    print("Купон не открылся! Следующая ставка.\n")
                    browser.close()
                    browser.switch_to.window(browser.window_handles[0])
                    continue

                coup_kef= float(browser.find_element_by_class_name('bs-Odds').text)
                print("Кэф в купоне " + str(coup_kef))
                if coup_kef-etalon_kef<=-0.01:
                    print("Кэф просел. Следующая ставка.\n")
                    browser.switch_to.window(browser.window_handles[1])
                    browser.close()
                    browser.switch_to.window(browser.window_handles[0])
                    continue
                bet_type_coup = get_bet_type(0)
                print(bet_type_coup)
                if not bet_type_coup == bet_type_scen:
                    print("Исход поменялся")
                    browser.switch_to.window(browser.window_handles[1])
                    browser.close()
                    browser.switch_to.window(browser.window_handles[0])
                    continue
                browser.switch_to.window(browser.window_handles[0])
                time.sleep(0.2)
                update_calc()
                time.sleep(0.2)
                if "line-through" in str(browser.find_element_by_xpath("//a[@id='lBet1']").get_attribute('style')):
                    print("Ставку закрыли. Следующая.")
                    browser.switch_to.window(browser.window_handles[1])
                    browser.close()
                    browser.switch_to.window(browser.window_handles[0])
                    continue

                etalon_preval=float(browser.find_element_by_id("lProfitForBoth").text[0:-1])
                final_kef = float(browser.find_element_by_xpath("//input[@id='tfCoef1']").get_attribute('value'))
                preval=get_value(final_kef)
                if etalon_preval-preval<=-0.1:
                    print("Переоценка просела (" + str(etalon_preval) +"%). Следующая ставка.")
                    browser.switch_to.window(browser.window_handles[1])
                    browser.close()
                    browser.switch_to.window(browser.window_handles[0])
                    continue
                print(preval)
                print(etalon_preval)
                browser.switch_to.window(browser.window_handles[1])
                time.sleep(random_num(0.3,0.5))
                browser.switch_to.frame("bsFrame")
                if not float(browser.find_element_by_xpath("//*[@class='bs-TotalStake totalStake']").text[1:]) == float(
                        fix_bet):
                    browser.switch_to.window(browser.window_handles[1])
                    browser.close()
                    browser.switch_to.window(browser.window_handles[0])
                    time.sleep(random_num(0.4, 0.6))
                    browser.find_element_by_id("tfStake1").clear()
                    browser.find_element_by_id("tfStake1").send_keys(fix_bet)
                    print("Сумма ставки слетела!")
                    continue
                coup_kef = float(browser.find_element_by_class_name('bs-Odds').text)
                if coup_kef - final_kef <= -0.01:
                    print("Кэф просел("+ str(coup_kef) + "). Следующая ставка.\n")
                    browser.switch_to.window(browser.window_handles[1])
                    browser.close()
                    browser.switch_to.window(browser.window_handles[0])
                    continue
                try:
                    place_bet_button=browser.find_element_by_xpath("//span[contains(text(), 'Place Bet')]")
                    print("Загружаем ставку!")
                    print("\tКэф в купоне: " + str(coup_kef))
                    print("\tПереоценка: " + str(etalon_preval) + "%")
                    place_bet_button.click()
                    try:
                        WebDriverWait(browser, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Bet Placed')]")))
                        print("Готово!.\n")
                        bet_counter = bet_counter + 1
                        write_log(str(bet_counter) + " -> Кэф в купоне: " + str(coup_kef) + "\tПереоценка: " + str(etalon_preval) + "% " + str(time.ctime()))
                        write_to_bet_name_file(current_bet)
                        check_max_one_game_count(current_bet)
                    except TimeoutException:
                        print("Не проставляется. Следующая ставка.\n")
                    browser.switch_to.window(browser.window_handles[1])
                    browser.close()
                    browser.switch_to.window(browser.window_handles[0])

                except Exception as e:
                    print("Не удалось проставить ставку, следующая")
                    print(str(e))
                #Здесь и закончился наш чудо цикл
            except Exception as e:
                print("Произошла неведомая херня:")
                print("")
                print(str(e))
                print("")
    print("Я сделяль!")
    write_log("Всего ставок: " + str(bet_count_to))
    while True:
        a=input()
        if a=="n":
            print("Сколько ставок проставить???")
            bet_count_to = int(input())
            bet_counter=0
            break
        if a=="e":
            exit(0)



#Сравнение исходов






import base64
import random
import time

import keyboard
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def login(br, usr, pas):
    WebDriverWait(br, 20).until(EC.element_to_be_clickable((By.XPATH, "//p[@id='intro']/a")))
    br.find_element_by_class_name("searchbox").send_keys('Dalton lyceum Barendrecht')
    WebDriverWait(br, 20).until(EC.element_to_be_clickable((By.XPATH, "//li[text() = 'Dalton Lyceum Barendrecht ']"))).click()
    WebDriverWait(br, 20).until(EC.element_to_be_clickable((By.ID, "submitIt"))).click()

    WebDriverWait(br, 20).until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_nativeLoginButton")))
    br.find_element_by_id("ctl00_ContentPlaceHolder1_Username_input").send_keys(usr)
    br.find_element_by_id("ctl00_ContentPlaceHolder1_Password_input").send_keys(pas)
    WebDriverWait(br, 20).until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_nativeLoginButton"))).click()
    WebDriverWait(br, 40).until(EC.element_to_be_clickable((By.ID, "button-with-name")))

def get_answers(br, correctpercentage):
    WebDriverWait(br, 50).until(EC.presence_of_element_located((By.ID, 'frame-viewer')))
    br.switch_to.frame(br.find_element_by_id('frame-viewer'))
    try:
        if br.find_elements_by_xpath("//div[@class='topStepsButtons']/div"):
            questions = br.find_elements_by_xpath("//div[@class='topStepsButtons']/div")
            multiple = True
        else:
            questions = [0]
            multiple = False
    except:
        questions = [0]
        multiple = False
        
    i = 2
    for question in questions:
        print(str(i-1) + ':')
        if multiple == True:
            question.click()
        if 'block' in br.find_element_by_xpath('//div[@id="pages-container"]/div/div[{}]/div[contains(@class, "page-buttons")]/div[@id="action-buttonfollowing"]'.format(i)).value_of_css_property('display'):
            print('Question already made, skipping...')
        elif br.find_elements_by_xpath('//div[@id="pages-container"]/div/div[{}]/div[{}]/div[@id="plselfScoreFeedback"]'.format(i, len(br.find_elements_by_xpath('//div[@id="pages-container"]/div/div[{}]/div'.format(i))) - 1)):
            #open question
            print('Open question')
            br.execute_script('document.evaluate("//div[@id=\'pages-container\']/div/div[{}]/div[{}]/div[@id=\'plselfScoreFeedback\']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.style.display = "block";'.format(i, len(br.find_elements_by_xpath('//div[@id="pages-container"]/div/div[{}]/div'.format(i))) - 1))
            waituntildone(i, br)
        elif br.find_elements_by_xpath("//div[@id='pages-container']/div/div[{}]/div[contains(@class, 'interaction')]/ul/li/div[contains(@class, 'statement')]/div[contains(@class, 'dropdown-box-correct')]".format(i)):
            #select menu
            done = False
            while done == False:
                k = 0
                base64strings = br.find_elements_by_xpath("//div[@id='pages-container']/div/div[{}]/div[contains(@class, 'interaction')]/ul/li/div[contains(@class, 'statement')]/div[contains(@class, 'dropdown-box-correct')]/div[contains(@class, 'dropOption')]".format(i))
                for base64string in base64strings:
                    correct = base64.b64decode(base64string.get_attribute('innerHTML')).decode("utf-8")
                    if random.randrange(1,101) <= correctpercentage:
                        answercorrect = True
                    else:
                        answercorrect = False
                    done = False
                    for j in range(2,40):
                        if done == False:
                            option = br.find_elements_by_xpath("//div[@id='pages-container']/div/div[{}]/div[contains(@class, 'interaction')]/ul/li/div[contains(@class, 'statement')]/div[contains(@class, 'dropdown-box')]/div[contains(@class, 'drop-box')]/div[{}]".format(i, j))[k]
                            print(option.get_attribute('innerHTML'), correct)
                            if option.get_attribute('innerHTML') in correct or answercorrect == False:
                                (br.find_elements_by_xpath("//div[@id='pages-container']/div/div[{}]/div[contains(@class, 'interaction')]/ul/li/div[contains(@class, 'statement')]/div[contains(@class, 'dropdown-box')]".format(i))[k*2]).click()
                                WebDriverWait(br, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='pages-container']/div/div[{}]/div[contains(@class, 'interaction')]/ul/li[{}]/div[contains(@class, 'statement')]/div[contains(@class, 'dropdown-box')]/div[contains(@class, 'drop-box')]/div[{}]".format(i, (k+1)*2, j)))).click()
                                done = True
                                break
                    k += 1
                br.find_element_by_xpath('//div[@id="pages-container"]/div/div[{}]/div[contains(@class, "page-buttons")]/div[@id="action-buttoncontrol"]'.format(i)).click()
                try:
                    if not 'block' in br.find_element_by_xpath('//div[@id="pages-container"]/div/div[{}]/div[contains(@class, "page-buttons")]/div[@id="action-buttonretry"]'.format(i)).value_of_css_property('display'):
                        done = True
                    else:
                        br.find_element_by_xpath('//div[@id="pages-container"]/div/div[{}]/div[contains(@class, "page-buttons")]/div[@id="action-buttonretry"]'.format(i)).click()
                except:
                    done = True
        elif br.find_elements_by_xpath('//div[@id="pages-container"]/div/div[{}]/div[{}]/ul[contains(@class, "normal")]'.format(i, len(br.find_elements_by_xpath('//div[@id="pages-container"]/div/div[{}]/div'.format(i))) - 1)) or br.find_elements_by_xpath('//div[@id="pages-container"]/div/div[{}]/div[{}]/ul'.format(i, len(br.find_elements_by_xpath('//div[@id="pages-container"]/div/div[{}]/div'.format(i))) - 2)):
            #Inputs
            done = False
            while done == False:
                j = 0
                for answer in br.find_elements_by_xpath("//div[@id='pages-container']/div/div[{}]/div[contains(@class, 'interaction')]/ul/li/div[contains(@class, 'statement')]/div/div[contains(@class, 'textEntryInput-correct')]/div".format(i)):
                    answertxt = answer.get_attribute('innerHTML')
                    inputstr = base64.b64decode(answertxt).decode("utf-8")
                    if random.randrange(1,101) > correctpercentage:
                        tmpint = random.randrange(5)
                        try:
                            if tmpint == 0:
                                inputstr = '?'
                            elif tmpint == 1:
                                tmpint2 = random.randrange(1, len(inputstr))
                                alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
                                tmpchar = alphabet[random.randrange(len(alphabet))]
                                inputstr = inputstr[:tmpint2] + tmpchar + inputstr[tmpint2:]
                            elif tmpint == 2:
                                inputstr = inputstr[:-1]
                            elif tmpint == 3 and not inputstr.lower() == inputstr:
                                inputstr = inputstr.lower()
                            else:
                                tmpint2 = random.randrange(1, len(inputstr)-1)
                                inputstr = inputstr[:tmpint2] + inputstr[tmpint2+1:]
                        except:
                            pass
                    try:
                        inputfields = br.find_elements_by_xpath("//div[@id='pages-container']/div/div[{}]/div[contains(@class, 'interaction')]/ul/li/div[contains(@class, 'statement')]/div/div/textarea[contains(@class, 'answerInput')]".format(i))
                        inputfields.index(br.find_element_by_xpath("//div[@id='pages-container']/div/div[{}]/div[contains(@class, 'interaction')]/ul/li[1]/div[contains(@class, 'statement')]/div/div[contains(@class, 'textEntryInput')]/textarea[1]".format(i)))
                        inputfields[j].send_keys(inputstr)
                    except:
                        pass
                    j += 1
                br.find_element_by_xpath('//div[@id="pages-container"]/div/div[{}]/div[contains(@class, "page-buttons")]/div[@id="action-buttoncontrol"]'.format(i)).click()
                try:
                    if not 'block' in br.find_element_by_xpath('//div[@id="pages-container"]/div/div[{}]/div[contains(@class, "page-buttons")]/div[@id="action-buttonretry"]'.format(i)).value_of_css_property('display'):
                        done = True
                    else:
                        br.find_element_by_xpath('//div[@id="pages-container"]/div/div[{}]/div[contains(@class, "page-buttons")]/div[@id="action-buttonretry"]'.format(i)).click()
                except:
                    done = True
        elif br.find_elements_by_xpath('//div[@id="pages-container"]/div/div[{}]/ul/li'.format(i)):
            #multiple choice
            mogelijke_opties = br.find_elements_by_xpath('//div[@id="pages-container"]/div/div[{}]/ul/li/div[contains(@class, "alt-mcItem")]'.format(i))
            goede_antwoord = None
            for optie in mogelijke_opties:
                if 'act' in str(optie.get_attribute('class')):
                    goede_antwoord = mogelijke_opties.index(optie)
            goede_goede_antwoord = goede_antwoord
            done = False
            print(goede_antwoord)
            while done == False:
                goede_antwoord = goede_goede_antwoord
                if random.randrange(1,101) > correctpercentage:
                    goede_antwoord = random.randrange(0,len(mogelijke_opties))
                br.find_elements_by_xpath('//div[@id="pages-container"]/div/div[{}]/ul/li/div[contains(@class, "tickable")]'.format(i))[goede_antwoord].click()
                br.find_element_by_xpath('//div[@id="pages-container"]/div/div[{}]/div[contains(@class, "page-buttons")]/div[@id="action-buttoncontrol"]'.format(i)).click()
                try:
                    if not 'block' in br.find_element_by_xpath('//div[@id="pages-container"]/div/div[{}]/div[contains(@class, "page-buttons")]/div[@id="action-buttonretry"]'.format(i)).value_of_css_property('display'):
                        done = True
                    else:
                        br.find_element_by_xpath('//div[@id="pages-container"]/div/div[{}]/div[contains(@class, "page-buttons")]/div[@id="action-buttonretry"]'.format(i)).click()
                except:
                    done = True
        elif br.find_elements_by_xpath("//div[@id='pages-container']/div/div[{}]/div[contains(@class, 'interaction')]/ul/li/div[contains(@class, 'toggleColumn')]".format(i)):
            #yes/no
            for answer in br.find_elements_by_xpath("//div[@id='pages-container']/div/div[{}]/div[contains(@class, 'interaction')]/ul/li/div[contains(@class, 'toggleColumn')]/div[contains(@class, 'toggleAnswer')]".format(i)):
                answer.click
        elif br.find_elements_by_xpath("//div[@id='pages-container']/div/div[{}]/div[contains(@class, 'interaction')]/div/div[contains(@class, 'ctm-drop-area')]/dl/li[contains(@class, 'drop-area')]".format(i)):
            #drag and drop
            for option in br.find_elements_by_xpath("//div[@id='pages-container']/div/div[{}]/div[contains(@class, 'interaction')]/div/div[contains(@class, 'ctm-drop-area')]/dl/li[contains(@class, 'drop-area')]/div[contains(@class, 'ui-droppable-correct')]/div[contains(@class, 'text-item')]".format(i)):
                print(option.get_attribute("title"))
            waituntildone(i, br)
        else:
            #else
            print('Not found...')
        i += 1

def waituntildone(i, br):
    print('Fill in the open question or press F4 to skip...')
    while not 'block' in br.find_element_by_xpath('//div[@id="pages-container"]/div/div[{}]/div[contains(@class, "page-buttons")]/div[@id="action-buttonfollowing"]'.format(i)).value_of_css_property('display') and not keyboard.is_pressed('F4'):
        time.sleep(0.02)

def init():
    br = webdriver.Chrome()
    url = 'https://neuekontakte.digitaal.noordhoff.nl/?SSOid=d45d3472-41ee-40c8-a109-0895e5e0f74e#/plp/book/dee7cd52-5444-497f-8d67-5e17a0e37ce4/lesson-material/de612365-ed93-4972-b669-686a0ab6f2f9'
    loginurl = 'https://entreeserviceprovider.ecservices.nu/idpLogin?returnUrl=https://neuekontakte.digitaal.noordhoff.nl/'
    br.get(loginurl)
    return br, url 

def start(usr, pas):
    print('Loging in with: ' + usr)
    DISCONNECTED_MSG = 'Unable to evaluate script: disconnected: not connected to DevTools\n'
    br, url = init()

    done = False

    correctpercentage = 70

    while done == False:
        try:
            login(br, usr, pas)
            done = True
        except:
            pass
    print('Press F2 to solve...')
    br.get(url)
    while 1:
        while not keyboard.is_pressed('F2'):
            pass
        get_answers(br, correctpercentage)
    br.close()

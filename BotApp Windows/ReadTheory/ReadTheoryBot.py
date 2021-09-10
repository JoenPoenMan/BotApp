import json
import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def readJSON():
    with open('newquestions.json', 'r') as f:
        data = f.read()
    return json.loads(data)

def updateJSON(NewDict):
    with open('newquestions.json', 'w') as f:
        json.dump(NewDict, f)

def login(usr,pas,br):
    user=br.find_element_by_css_selector("#username") 
    user.clear()
    user.send_keys(usr) 
    pasd=br.find_element_by_css_selector("#password")
    pasd.clear()
    pasd.send_keys(pas) 
    btn=br.find_element_by_css_selector("#loginForm-button")
    btn.click() 

def detectquestions(DaCode, br):
    questions = []
    allAnswers = []
    for x in DaCode['mergedQuestionList']:
        answers = []
        try:
            for y in x['answerList']:
                answers.append(y['answerId'])
        except:
            answers = x['answerIDs']
        questions.append(x['GUIId'])
        allAnswers.append(answers)
    return questions, allAnswers
    
def findcorrect(questions, answers, NewDict, DaCode, niveau, br):
    numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve']
    currniveau = numbers.index(DaCode['level'].lower()) + 1
    correctanswers = []
    for x in range(len(questions)):
        try:
            correctanswers.append(NewDict[questions[x]])
        except:
            try:
                answer = int(NewDict[('questionId-' + questions[x])])
                if DaCode['mergedQuestionList'][x]['difficult'] == True:
                    answer -= 1
                if not DaCode['mergedQuestionList'][x]['associatedPassageTextBeginIndex'] == None:
                    answer -= 1
                answer -= 3
                correctanswers.append(answers[x][answer])
                del NewDict[('questionId-' + questions[x])]
                NewDict[questions[x]] = answers[x][answer]
            except:
                correctanswers.append(answers[x][0])

    print('Curr grade: ' + str(currniveau) + ', Goal: ' + str(niveau))
    for x in range(len(correctanswers)):
        if ((currniveau == niveau and random.randrange(1, 101) > 90) or (currniveau > niveau and random.randrange(1, 101) > 40)) and not niveau == 12:
            newrandom = correctanswers[x]
            while newrandom == correctanswers[x]:
                newrandom = answers[x][random.randrange(len(answers[x]))]
            correctanswers[x] = newrandom
        
        correctanswers[x] = answers[x].index(correctanswers[x])+1

    correct = False
    for j in range(5):
        if br.find_elements_by_xpath('//div[contains(@class, "btn-full-screen")]'):
            correct = True
            currquestion = br.find_elements_by_xpath("//div[contains(@class,'question-marker')]").index(br.find_element_by_xpath("//div[contains(@class,'active')]"))
            for i in range(currquestion, len(correctanswers)):
                curranswer = correctanswers[i]
                newcorranswer = enter_answer(
                    "//div[contains(@class, 'student-quiz-page__question-wrapper')]/div/div/div/div[contains(@class, 'student-quiz-page__answer')][{}]".format(curranswer),
                    "//div[contains(@class,'quiz-action__answer-btn')]", 
                    "//div[contains(@class,'quiz-action__next-btn')]", br
                    )
                NewDict[questions[i]] = answers[i][newcorranswer]
            br.get("https://readtheory.org/app/student/quiz")
            return NewDict
        else:
            if br.find_elements_by_xpath("//button[contains(@class,'fc-cta-consent')]"):
                WebDriverWait(br, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'fc-cta-consent')]"))).click()
                br.get("https://readtheory.org/app/student/quiz")
    if correct == False:
        raise Exception('This version of read theory is not supported...')

def enter_answer(xpath1, xpath2, xpath3, br):
    done = False
    finished = False
    counter = 0
    corranswer = 0
    while done == False:
        try:
            br.find_element_by_xpath(xpath1).click()
        except:
            pass

        try:
            br.find_element_by_xpath(xpath2).click()
        except:
            pass
        
        try:
            if br.find_elements_by_xpath("//div[contains(@class, 'marked')]"):
                corranswer = br.find_elements_by_xpath("//div[contains(@class, 'answer-card-wrapper')]").index(br.find_element_by_xpath("//div[contains(@class, 'marked')]"))
                br.find_element_by_xpath(xpath3).click()
                finished = True
            elif br.find_elements_by_xpath("//div[contains(@class, 'passed')]"):
                corranswer = br.find_elements_by_xpath("//div[contains(@class, 'answer-card-wrapper')]").index(br.find_element_by_xpath("//div[contains(@class, 'passed')]"))
                br.find_element_by_xpath(xpath3).click()
                finished = True
        except:
            pass

        if (finished == True and 'disabled' in br.find_element_by_xpath(xpath3).get_attribute('class')) or ('Continue' in br.find_element_by_xpath(xpath3).text):
            time.sleep(0.5)
            if (finished == True and 'disabled' in br.find_element_by_xpath(xpath3).get_attribute('class')) or ('Continue' in br.find_element_by_xpath(xpath3).text):
                done = True

        counter += 1
        if counter > 500:
            raise Exception('Could not enter answer')

        time.sleep(0.05)
    return corranswer

def start(usr, pas, niveau, aantal):
    br = webdriver.Chrome()
    br.get("https://readtheory.org/auth/login")

    login(usr, pas, br)
    NewDict = readJSON()

    counter = 1
    for text in range(aantal):
        DaCode = br.execute_script("return window.rt_bridge_page_data.command")
        questions, answers = detectquestions(DaCode, br)
        NewDict = findcorrect(questions, answers, NewDict, DaCode, niveau, br)
        updateJSON(NewDict)
        print('Finished making text (' + str(counter) + '/' + str(aantal) + ')!\n')
        counter += 1

    br.close()

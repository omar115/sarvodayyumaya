import pandas as pd
import pytesseract as pie
from PIL import Image
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import Select
from selenium import webdriver
import os
import datetime as dt
from datetime import datetime


from reporting.creatinglogs import logs
import config

# pie.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def driver_init():
    # browser setup
    opts = webdriver.ChromeOptions()
    driver = webdriver.Remote(desired_capabilities=opts.to_capabilities(),
        command_executor=config.NODE_URL)

    driver.maximize_window()
    driver.set_page_load_timeout(25)
    return driver


# story 1

def loginPage(driver):
    #logs("loginPage")
    # go to the link

    driver.get(config.SITE_URL)

    
        # click close button
    driver.find_element_by_xpath(
            "/html/body/div[2]/div/table/tbody/tr[4]/td/input").click()
    
    # inputting username
    driver.find_element_by_id("username").send_keys("shrcechs")

    # inputting password
    driver.find_element_by_id("password").send_keys("billing@456")  
    driver.implicitly_wait(10)
    try:
        src = driver.find_element_by_id(
            "img_captcha").screenshot("image/abc.png")

        img = Image.open("image/abc.png")

        txt = pie.image_to_string(img)

        driver.find_element_by_id("txtCaptcha").send_keys(txt)
        driver.find_element_by_xpath(
            "/html/body/table/tbody/tr[2]/td[2]/form/table/tbody/tr[1]/td[3]/table/tbody/tr[13]/td/input").click()
        driver.implicitly_wait(2)
        driver.find_element_by_xpath(
            "/html/body/div[2]/div/table/tbody/tr[4]/td/input").click()
        
        driver.find_element_by_id("ihaveseennmi").click()  
            
        #driver.find_element_by_id("ihaveseennmi").click()
        #driver.find_element_by_id("li_0").click()
        #driver.find_element_by_xpath(
            #"/html/body/table/tbody/tr[2]/td[1]/form/div/ul/li[1]/ul/li[1]/a").click()
        #driver.implicitly_wait(2)
            
    
    except:
        print("there is an error")
        driver.implicitly_wait(10)
        #driver.find_element_by_xpath('/html/body/div[2]/div/table/tbody/tr[4]/td/input').click() 
        #driver.close()
        loginPage(driver)

    # login successful

# secondPage


def secondPage(driver, df, index):

    print(df)

    #driver.find_element_by_xpath(
        #"/html/body/div[2]/div/table/tbody/tr[4]/td/input").click()
            
    #driver.find_element_by_id("ihaveseennmi").click()
    driver.find_element_by_id("li_0").click()
    driver.find_element_by_xpath(
        "/html/body/table/tbody/tr[2]/td[1]/form/div/ul/li[1]/ul/li[1]/a").click()

    select = Select(driver.find_element_by_name('cardType'))

    # selecting card type
    select.select_by_visible_text("Old Card")

    # inputting service id
    serviceid = (df['Service ID'].values[index])
    regid = df['Registration Number'].values[index]
    print(serviceid)

    if int(serviceid) == True:
        print('fuuuuuuu')
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table/tbody/tr[5]/td[2]/input').send_keys(int(serviceid))
    else:
        print('ohh ho')
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table/tbody/tr[5]/td[2]/input').send_keys(str(serviceid))

    print(regid)

    # inputting registration id
    driver.find_element_by_xpath(
        '/html/body/table/tbody/tr[2]/td[2]/form/table/tbody/tr[6]/td[2]/input').send_keys(regid)

    # click the submit button
    driver.implicitly_wait(10)
    driver.find_element_by_id('btnsubmit').click()

    # logs("secondPage")
    # secondpage -- card selection successful


# patient details fillup
def PatientDetails(driver, df, index):
    # not in the list continue anyway
    # driver.find_element_by_xpath(
    # '/html/body/table/tbody/tr[2]/td[2]/form/div[1]/table[2]/tbody/tr/td/input').click()

    # clicking on the card no
    driver.find_element_by_xpath(
        '/html/body/table/tbody/tr[2]/td[2]/form/div[1]/table[1]/tbody/tr/td[1]/a').click()

    # finding the patient name
    name = df["Patient Name"].values[index]
    print(name)
    i = 1
    while(i <= 10):
        tdname = driver.find_element_by_xpath(
            '/html/body/div[5]/div[2]/div/div/table/tbody/tr['+str(i)+']/td[3]')
        namep = tdname.text

        if namep == name:

            driver.find_element_by_xpath(
                '/html/body/div[5]/div[2]/div/div/table/tbody/tr['+str(i)+']/td[1]/input').click()
            funOfPatientDetails(driver, df, index)
            break
        else:
            print("hazzelnut")
            # print(name)
            # print(namep)
        i = i + 1
    # logs("PatientDetails")
    # patientDetails form fillup successful


# admission form fillup
def admissionFill(driver, df, index):

    # click admission
    driver.find_element_by_xpath(
        '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/ul/li[2]/a').click()

    # selecting polyclinic
    # polyclinic-dropdown

    poly = df["Polyclinic"].values[index]

    funOfPoly(driver, poly)

    # adission/opd date

    # selecting hour
    hr = int(df["Hour"].values[index])
    mins = int(df["Min"].values[index])
    print(hr)
    funOfHour(driver, hr, mins)

    # selecting admission / opd date
    driver.find_element_by_xpath(
        '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[2]/table[1]/tbody/tr[5]/td[2]/img').click()

    date = df["Admission/OPD Date"].values[index]
    st = date.split('/')
    din = int(st[0])
    mn = int(st[1])
    yr = int(st[2])

    fundOfOPDDate(driver, mn, yr, din)

    # inputting admission/opd number
    hasText = driver.find_element_by_xpath(
        '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[2]/table[1]/tbody/tr[6]/td[2]/input')
    if len(hasText.text) == 0:
        print('Yes')
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[2]/table[1]/tbody/tr[6]/td[2]/input').send_keys(df["Admission/OPD Number"].values[index])

    # selecting expected date change

    edate = df["Expected Discharge Date"].values[index]
    est = edate.split('/')
    edin = int(est[0])
    emn = int(est[1])
    eyr = int(est[2])
    print(edin)
    print(emn)
    print(eyr)
    

    driver.find_element_by_xpath(
     '/html/body/table[2]/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[2]/table[1]/tbody/tr[6]/td[4]/img').click()

    funOfEDDDate(driver, edin, emn, eyr)

    # inputting treatment cost
    driver.find_element_by_xpath(
        '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[2]/table[1]/tbody/tr[7]/td[2]/input').send_keys(int(df["Approx treatment Cost"].values[index]))

    # selecting roomtype

    room = df["Room Type"].values[index]

    if room == 'General':
        select = Select(driver.find_element_by_id('hospitalRoomType'))

        select.select_by_visible_text("General")

    elif room == 'Private':
        select = Select(driver.find_element_by_id('hospitalRoomType'))

        select.select_by_visible_text("Private")

    elif room == 'Semi-Private':
        select = Select(driver.find_element_by_id('hospitalRoomType'))

        select.select_by_visible_text("Semi-Private")

    # inputting room number
    driver.find_element_by_xpath(
        '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[2]/table[1]/tbody/tr[8]/td[4]/input').send_keys(int(df["Room Number"].values[index]))

    # logs("admissionFill")
    # admission formfillup successful

# patienHistory


def patientHistory(driver, df, index):
    # navigate to that tab

    driver.find_element_by_xpath(
        '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/ul/li[3]/a').click()

    hyp = df["HyperTension"].values[index]
    dia = df["Diabetic"].values[index]
    hrt = df["Heart"].values[index]
    cpd = df["COPD"].values[index]
    brn = df["Bronchail Asthma"].values[index]
    std = df["STD"].values[index]
    alco = df["Alcohol/Drug"].values[index]
    other = df["Other Disease"].values[index]

    # inputting hypertension
    if hyp == 'Yes':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='Y'][name='preailment[0].anyAilment']").click()
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[3]/table/tbody/tr[2]/td[2]/input[4]').send_keys(df["Hypertension(v)"].values[index])

    if hyp == 'N.M':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='M'][name='preailment[0].anyAilment']").click()

    if hyp == 'No':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='N'][name='preailment[0].anyAilment']").click()
    # diabetic
    if dia == 'Yes':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='Y'][name='preailment[1].anyAilment']").click()
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[3]/table/tbody/tr[3]/td[2]/input[4]').send_keys(df["Diabetic(v)"].values[index])

    if dia == 'No':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='N'][name='preailment[1].anyAilment']").click()

    if dia == 'N.M':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='M'][name='preailment[1].anyAilment']").click()
    # heart
    if hrt == 'Yes':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='Y'][name='preailment[2].anyAilment']").click()
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[3]/table/tbody/tr[4]/td[2]/input[4]').send_keys(df["Heart(v)"].values[index])

    if hrt == 'No':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='N'][name='preailment[2].anyAilment']").click()

    if hrt == 'N.M':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='M'][name='preailment[2].anyAilment']").click()

    # copd
    if cpd == 'Yes':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='Y'][name='preailment[3].anyAilment']").click()
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[3]/table/tbody/tr[5]/td[2]/input[4]').send_keys(df["COPD(v)"].values[index])

    if cpd == 'No':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='N'][name='preailment[3].anyAilment']").click()

    if cpd == 'N.M':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='M'][name='preailment[3].anyAilment']").click()

    # bronchail

    if brn == 'Yes':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='Y'][name='preailment[4].anyAilment']").click()
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[3]/table/tbody/tr[6]/td[2]/input[4]').send_keys(df["Bronchail Asthma(v)"].values[index])

    if brn == 'No':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='N'][name='preailment[4].anyAilment']").click()

    if brn == 'N.M':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='M'][name='preailment[4].anyAilment']").click()

    # std

    if std == 'Yes':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='Y'][name='preailment[5].anyAilment']").click()
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[3]/table/tbody/tr[7]/td[2]/input[4]').send_keys(df["STD(v)"].values[index])

    if std == 'No':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='N'][name='preailment[5].anyAilment']").click()

    if std == 'N.M':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='M'][name='preailment[5].anyAilment']").click()

    # alco

    if alco == 'Yes':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='Y'][name='preailment[6].anyAilment']").click()
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[3]/table/tbody/tr[8]/td[2]/input[4]').send_keys(df["Alcohol/drug(v)"].values[index])

    if alco == 'No':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='N'][name='preailment[6].anyAilment']").click()

    if alco == 'N.M':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='M'][name='preailment[6].anyAilment']").click()

    # other
    if other == 'Yes':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='Y'][name='preailment[7].anyAilment']").click()
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[3]/table/tbody/tr[9]/td[2]/input[4]').send_keys(df["Other Disease(v)"].values[index])

    if other == 'No':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='N'][name='preailment[7].anyAilment']").click()

    if other == 'N.M':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='M'][name='preailment[7].anyAilment']").click()

    # logs("patientHistory")
    # patienthistory is successful

# clinicFind


def clinicFind(driver, df, index):

    driver.find_element_by_xpath(
        '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/ul/li[4]/a').click()

    bp = df["Blood Pressure"].values[index]
    cvs = df["CVS"].values[index]
    rs = df["RS"].values[index]
    abdo = df["Abdomen"].values[index]
    cns = df["CNS"].values[index]
    otr = df["Other"].values[index]

    # inputting blood pressure
    if bp == 'Yes':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='Y'][name='clinicalfinding[0].anyTest']").click()

        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[4]/table/tbody/tr[2]/td[2]/input[4]').send_keys(df["Blood Pressure(v)"].values[index])

    if bp == 'No':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='N'][name='clinicalfinding[0].anyTest']").click()

    if bp == 'N.M':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='M'][name='clinicalfinding[0].anyTest']").click()

    if cvs == 'Yes':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='Y'][name='clinicalfinding[1].anyTest']").click()
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[4]/table/tbody/tr[3]/td[2]/input[4]').send_keys(df["CVS(v)"].values[index])

    if cvs == 'No':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='N'][name='clinicalfinding[1].anyTest']").click()

    if cvs == 'N.M':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='M'][name='clinicalfinding[1].anyTest']").click()

    if rs == 'Yes':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='Y'][name='clinicalfinding[2].anyTest']").click()
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[4]/table/tbody/tr[4]/td[2]/input[4]]').send_keys(df["RS(v)"].values[index])

    if rs == 'No':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='N'][name='clinicalfinding[2].anyTest']").click()

    if rs == 'N.M':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='M'][name='clinicalfinding[2].anyTest']").click()

    if abdo == 'Yes':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='Y'][name='clinicalfinding[3].anyTest']").click()
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[4]/table/tbody/tr[5]/td[2]/input[4]').send_keys(df["Abdomen(v)"].values[index])

    if abdo == 'No':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='N'][name='clinicalfinding[3].anyTest']").click()

    if abdo == 'N.M':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='M'][name='clinicalfinding[3].anyTest']").click()

    if cns == 'Yes':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='Y'][name='clinicalfinding[4].anyTest']").click()
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[4]/table/tbody/tr[6]/td[2]/input[4]').send_keys(df["CNS(v)"].values[index])

    if cns == 'No':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='N'][name='clinicalfinding[4].anyTest']").click()

    if cns == 'N.M':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='M'][name='clinicalfinding[4].anyTest']").click()

    if otr == 'Yes':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='Y'][name='clinicalfinding[5].anyTest']").click()
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[4]/table/tbody/tr[7]/td[2]/input[4]').send_keys(df["Other(v)"].values[index])

    if otr == 'No':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='N'][name='clinicalfinding[5].anyTest']").click()

    if otr == 'N.M':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='M'][name='clinicalfinding[5].anyTest']").click()

    # logs("clinicFind")
    # clinicfind is successful

# diagnose


def diagnose(driver, df, index):

    driver.find_element_by_xpath(
        '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/ul/li[5]/a').click()

    # RTA Type - YEs
    rta = df["RTA"].values[index]

    # inputting rta
    if rta == 'Yes':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='Y'][name='RTAType']").click()

        hasText = driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[5]/table[1]/tbody/tr[3]/td[2]/input')
        if len(hasText.text) == 0:
            print('Yes')
            driver.find_element_by_xpath(
                '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[5]/table[1]/tbody/tr[3]/td[2]/input').send_keys(df["Reason"].values[index])

        # inputting admission alignment
        hasText = driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[5]/table[1]/tbody/tr[5]/td[2]/textarea')
        if len(hasText.text) == 0:
            print('Yes')
            driver.find_element_by_xpath(
                '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[5]/table[1]/tbody/tr[5]/td[2]/textarea').send_keys(df["Admission Alignment"].values[index])

    if rta == 'No':
        # inputting admission alignment
        hasText = driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[5]/table[1]/tbody/tr[5]/td[2]/textarea')
        if len(hasText.text) == 0:
            print('Yes')
            driver.find_element_by_xpath(
                '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[5]/table[1]/tbody/tr[5]/td[2]/textarea').send_keys(df["Admission Alignment"].values[index])

    # logs("diagnose")
    # diagnose is succssful

# proposeTreatment


def proposeTreat(driver, df, index):
    driver.find_element_by_xpath(
        '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/ul/li[6]/a').click()

    inves = df["Investigations"].values[index]
    inten = df["Intensive Care"].values[index]
    medi = df["Medical Management"].values[index]
    surgi = df["Surgical Management"].values[index]
    mpro = df["Procedure Description [Minor]"].values[index]
    mapro = df["Procedure Description[Major]"].values[index]
    otr = df["Other Treatment/ Procedure"].values[index]

    # selecting and inputting Investigation
    if inves == 'Yes':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='Y'][name='proposedtreatment[0].anyTreatment']").click()

        hasText = driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[6]/table/tbody/tr[2]/td[2]/textarea')
        if len(hasText.text) == 0:
            print('Yes')

            driver.find_element_by_xpath(
                '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[6]/table/tbody/tr[2]/td[2]/textarea').send_keys(df["Investigations(v)"].values[index])

    if inves == 'No':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='N'][name='proposedtreatment[0].anyTreatment']").click()

    if inves == 'N.M':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='M'][name='proposedtreatment[0].anyTreatment']").click()

    # selecting and Inputting Intensive Care
    if inten == 'Yes':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='Y'][name='proposedtreatment[1].anyTreatment']").click()
        hasText = driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[6]/table/tbody/tr[3]/td[2]/textarea')
        if len(hasText.text) == 0:
            print('Yes')
            driver.find_element_by_xpath(
                '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[6]/table/tbody/tr[3]/td[2]/textarea').send_keys(df["Intensive Care (v)"].values[index])

    if inten == 'No':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='N'][name='proposedtreatment[1].anyTreatment']").click()

    if inten == 'N.M':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='M'][name='proposedtreatment[1].anyTreatment']").click()

    # selecting and inputting medical management
    if medi == 'Yes':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='Y'][name='proposedtreatment[2].anyTreatment']").click()

        hasText = driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[6]/table/tbody/tr[4]/td[2]/textarea')
        if len(hasText.text) == 0:
            print('Yes')
            driver.find_element_by_xpath(
                '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[6]/table/tbody/tr[4]/td[2]/textarea').send_keys(df["Medical Management(v)"].values[index])

    if medi == 'No':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='N'][name='proposedtreatment[2].anyTreatment']").click()

    if medi == 'N.M':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='M'][name='proposedtreatment[2].anyTreatment']").click()

    # selectitng and inputting surgical management
    if surgi == 'Yes':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='Y'][name='proposedtreatment[3].anyTreatment']").click()
        hasText = driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[6]/table/tbody/tr[5]/td[2]/textarea')
        if len(hasText.text) == 0:
            print('Yes')
            driver.find_element_by_xpath(
                '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[6]/table/tbody/tr[5]/td[2]/textarea').send_keys(df["Surgical Management(v)"].values[index])

    if surgi == 'No':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='N'][name='proposedtreatment[3].anyTreatment']").click()

    if surgi == 'N.M':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='M'][name='proposedtreatment[3].anyTreatment']").click()

    # selecting and inputting procedure description minor
    if mpro == 'Yes':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='Y'][name='proposedtreatment[4].anyTreatment']").click()
        hasText = driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[6]/table/tbody/tr[6]/td[2]/textarea')
        if len(hasText.text) == 0:
            print('Yes')
        driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[6]/table/tbody/tr[6]/td[2]/textarea').send_keys(
            df["Procedure Description [Minor](v)"].values[index])

    if mpro == 'No':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='N'][name='proposedtreatment[4].anyTreatment']").click()

    if mpro == 'N.M':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='M'][name='proposedtreatment[4].anyTreatment']").click()

    # selecting and inputting procedure description major
    if mapro == 'Yes':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='Y'][name='proposedtreatment[5].anyTreatment']").click()
        hasText = driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[6]/table/tbody/tr[7]/td[2]/textarea')
        if len(hasText.text) == 0:
            print('Yes')
        driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[6]/table/tbody/tr[7]/td[2]/textarea').send_keys(
            df["Procedure Description[Major](v)"].values[index])

    if mapro == 'No':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='N'][name='proposedtreatment[5].anyTreatment']").click()

    if mapro == 'N.M':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='M'][name='proposedtreatment[5].anyTreatment']").click()

    # selecting and inputting other treatment
    if otr == 'Yes':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='Y'][name='proposedtreatment[6].anyTreatment']").click()
        hasText = driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[6]/table/tbody/tr[8]/td[2]/textarea')
        if len(hasText.text) == 0:
            print('Yes')
            driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[6]/table/tbody/tr[8]/td[2]/textarea').send_keys(
                df["Other Treatment/ Procedure"].values[index])

    if otr == 'No':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='N'][name='proposedtreatment[6].anyTreatment']").click()

    if otr == 'N.M':
        driver.find_element_by_css_selector(
            "input[type='radio'][value='M'][name='proposedtreatment[6].anyTreatment']").click()

    # logs("proposeTreat")
    # propose treatment is successful

# upload document


def upDoc(driver, df, start_time, index):
    # navigate the site
    driver.find_element_by_xpath(
        '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/ul/li[7]/a').click()

    # clicking save and continue
    driver.find_element_by_xpath(
        '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[4]/td[1]/input[1]').click()

    # clicking close button
    driver.find_element_by_xpath(
        '/html/body/div[2]/div/table/tbody/tr[4]/td/input').click()

    # clicking pending information
    driver.find_element_by_xpath(
        '/html/body/table/tbody/tr[2]/td[1]/form/div/ul/li[1]/ul/li[2]').click()
    id1 = df["Registration Number"].values[index]
    date1 = df["Admission/OPD Date"].values[index]
    print(date1)
    print(id1)

    # service--id--tr--row
    trs = 2
    # std--service--id---td---after 25 iter changed
    std = 5

    # link er id
    linkid = 2

    # service---id---iter
    i = 1
    # no.of pages
    page = 1
    while(i <= 25):
        # service--id--nibo ami

        tdname = driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/div[2]/table/tbody/tr['+str(trs)+']/td[5]')
        idea2 = tdname.text
        id2 = str(idea2)
        # print(id2)

        # date e click korbo ami
        datefind2 = driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/div[2]/table/tbody/tr['+str(trs)+']/td[4]')

        datea2 = datefind2.text
        date2 = str(datea2)
        # print(date2)

        # ekhon ami check korbo

        if (id1 == id2) and (date1 == date2):
            # print(id1)
            # print(id2)
            # print(date1)
            # print(date2)

            sid= driver.find_element_by_xpath(
                '/html/body/table/tbody/tr[2]/td[2]/form/div[2]/table/tbody/tr['+str(trs)+']/td[2]/a')
            claim = sid.text
            claimid = str(claim)

            driver.find_element_by_xpath(
                '/html/body/table/tbody/tr[2]/td[2]/form/div[2]/table/tbody/tr['+str(trs)+']/td[2]/a').click()

            # print(claimid)
            break

        if i == 25:
            i = 0
            std = std+1
            trs = 1
            page = page+1
            # next button e click korbo which is fixed bro
            driver.find_element_by_xpath(
                '/html/body/table/tbody/tr[2]/td[2]/form/div[3]/table/tbody/tr/td/a['+str(page)+']').click()

        # ekhon kon gula iteration hobe seta thik kobo
        i = i+1
        trs = trs+1

    # clicking to upload document tab again
    driver.find_element_by_xpath(
        '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/ul/li[7]/a').click()

    regID = df["Registration Number"].values[index]
    pname = df["Patient Name"].values[index]
    doc1 = df["Doctor Certificate"].values[index]
    doc2 = df["ECHS Card Copy"].values[index]
    doc3 = df["Emergency Letter (By Hospital)"].values[index]
    doc4 = df["Referral Letter"].values[index]
    doc5 = df["Medical Reports"].values[index]
    doc6 = df["Others"].values[index]
    doc7 = df["Delay Condonation Letter"].values[index]
    doc8 = df["Disability Certificate"].values[index]
    doc9 = df["E I R"].values[index]
    doc10 = df["M L C"].values[index]
    doc11 = df["Self Attested Proforma"].values[index]

    DATA_OF_PATIENT = "Data of patient"

    if doc1 == 'Yes':
        loc = os.path.join(config.PROJECT_ROOT, DATA_OF_PATIENT, regID, f"{pname}_Doctor Certificate.pdf")
        # loc = "/home/akash/ProjectSelenium/Data of patient/" + \
        #     regID + "/" + pname+"_"+"Doctor Certificate" + ".pdf"
        print(loc)
        # inputting doctor certificate selection id
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[7]/table[1]/tbody/tr/td[2]/select/option[3]').click()

        # inputting selection
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[7]/table[1]/tbody/tr/td[3]/span/input').send_keys(loc)

        # uploading
        driver.implicitly_wait(10)
        driver.find_element_by_id('uploadButton').click()

    if doc2 == 'Yes':
        loc = os.path.join(config.PROJECT_ROOT, DATA_OF_PATIENT, regID, f"{pname}_ECHS Card Copy.pdf")
        # loc = "/home/akash/ProjectSelenium/Data of patient/" + \
        #     regID + "/" + pname+"_ECHS Card Copy.pdf"
        print(loc)
        # inputting doctor certificate selection id
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[7]/table[1]/tbody/tr/td[2]/select/option[5]').click()

        # inputting selection
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[7]/table[1]/tbody/tr/td[3]/span/input').send_keys(loc)
        
        # uploading
        driver.implicitly_wait(10)
        driver.find_element_by_id('uploadButton').click()

    if doc3 == 'Yes':
        loc = os.path.join(config.PROJECT_ROOT, DATA_OF_PATIENT, regID, f"{pname}_Emergency Letter.pdf")
        # loc = "/home/akash/ProjectSelenium/Data of patient/" + \
        #     regID + "/" + pname+"_Emergency Letter.pdf"
        print(loc)
        # inputting doctor certificate selection id
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[7]/table[1]/tbody/tr/td[2]/select/option[6]').click()

        # inputting selection
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[7]/table[1]/tbody/tr/td[3]/span/input').send_keys(loc)
        
        # uploading
        driver.implicitly_wait(10)
        driver.find_element_by_id('uploadButton').click()
    '''
    if doc4 == 'Yes':
        loc = os.path.join(config.PROJECT_ROOT, DATA_OF_PATIENT, regID, f"{pname}_Referral Letter.pdf")
        # loc = "/home/akash/ProjectSelenium/Data of patient/" + \
        #     regID + "/" + pname+"_Referral Letter.pdf"
        print(loc)
        # inputting doctor certificate selection id
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[7]/table[1]/tbody/tr/td[2]/select/option[10]').click()

        # inputting selection
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[7]/table[1]/tbody/tr/td[3]/span/input').send_keys(loc)

        # uploading
        driver.implicitly_wait(10)
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[7]/table[1]/tbody/tr/td[4]/input').click()
    '''
    '''
    if doc5 == 'Yes':
        loc = os.path.join(config.PROJECT_ROOT, DATA_OF_PATIENT, regID, f"{pname}_Medical Reports.pdf")
        # loc = "/home/akash/ProjectSelenium/Data of patient/" + \
        #     regID + "/" + pname+"_Medical Reports.pdf"
        print(loc)
        # inputting doctor certificate selection id
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[7]/table[1]/tbody/tr/td[2]/select/option[8]').click()

        # inputting selection
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[7]/table[1]/tbody/tr/td[3]/span/input').send_keys(loc)

        # uploading
        driver.implicitly_wait(10)
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[7]/table[1]/tbody/tr/td[4]/input').click()

    
    '''
    

    if doc6 == 'Yes':
        loc = os.path.join(config.PROJECT_ROOT, DATA_OF_PATIENT, regID, f"{pname}_Other.pdf")
        # loc = "/home/akash/ProjectSelenium/Data of patient/" + \
        #     regID + "/" + pname+"_Other.pdf"
        print(loc)
        # inputting doctor certificate selection id
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[7]/table[1]/tbody/tr/td[2]/select/option[9]').click()

        # inputting selection
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[7]/table[1]/tbody/tr/td[3]/span/input').send_keys(loc)
        
        # uploading
        driver.implicitly_wait(10)
        driver.find_element_by_id('uploadButton').click()
    '''
    if doc7 == 'Yes':
        loc = os.path.join(config.PROJECT_ROOT, DATA_OF_PATIENT, regID, f"{pname}_Delay Condonation.pdf")
        # loc = "/home/akash/ProjectSelenium/Data of patient/" + \
        #     regID + "/" + pname+"_Delay Condonation.pdf"
        print(loc)
        # inputting doctor certificate selection id
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[7]/table[1]/tbody/tr/td[2]/select/option[1]').click()

        # inputting selection
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[7]/table[1]/tbody/tr/td[3]/span/input').send_keys(loc)

        # uploading
        driver.implicitly_wait(10)
        driver.find_element_by_id('uploadButton').click()
    if doc8 == 'Yes':
        loc = os.path.join(config.PROJECT_ROOT, DATA_OF_PATIENT, regID, f"{pname}_Disablity Certificate.pdf")
        # loc = "/home/akash/ProjectSelenium/Data of patient/" + \
        #     regID + "/" + pname+"_Disablity Certificate.pdf"
        print(loc)
        # inputting doctor certificate selection id
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[7]/table[1]/tbody/tr/td[2]/select/option[2]').click()

        # inputting selection
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[7]/table[1]/tbody/tr/td[3]/span/input').send_keys(loc)

        # uploading
        driver.implicitly_wait(10)
        driver.find_element_by_id('uploadButton').click()
    if doc9 == 'Yes':
        loc = os.path.join(config.PROJECT_ROOT, DATA_OF_PATIENT, regID, f"{pname}_EIR.pdf")
        # loc = "/home/akash/ProjectSelenium/Data of patient/" + \
        #     regID + "/" + pname+"_EIR.pdf"
        print(loc)
        # inputting doctor certificate selection id
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[7]/table[1]/tbody/tr/td[2]/select/option[4]').click()

        # inputting selection
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[7]/table[1]/tbody/tr/td[3]/span/input').send_keys(loc)

        # uploading
        driver.implicitly_wait(10)
        driver.find_element_by_id('uploadButton').click()
    if doc10 == 'Yes':
        loc = os.path.join(config.PROJECT_ROOT, DATA_OF_PATIENT, regID, f"{pname}_MLC.pdf")
        # loc = "/home/akash/ProjectSelenium/Data of patient/" + \
        #     regID + "/" + pname+"_MLC.pdf"
        print(loc)
        # inputting doctor certificate selection id
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[7]/table[1]/tbody/tr/td[2]/select/option[7]').click()

        # inputting selection
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[7]/table[1]/tbody/tr/td[3]/span/input').send_keys(loc)

        # uploading
        driver.implicitly_wait(10)
        driver.find_element_by_id('uploadButton').click()
    if doc11 == 'Yes':
        loc = os.path.join(config.PROJECT_ROOT, DATA_OF_PATIENT, regID, f"{pname}_Self Attested.pdf")
        # loc = "/home/akash/ProjectSelenium/Data of patient/" + \
        #     regID + "/" + pname+"_Self Attested.pdf"
        print(loc)
        # inputting doctor certificate selection id
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[7]/table[1]/tbody/tr/td[2]/select/option[11]').click()

        # inputting selection
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[7]/table[1]/tbody/tr/td[3]/span/input').send_keys(loc)

        # uploading
        driver.implicitly_wait(10)
        driver.find_element_by_id('uploadButton').click()
            '''

    # digital signature issue>> press close button
    # driver.find_element_by_xpath('/html/body/div[2]/div/p/input').click()
    # print(regID)

    # inputting remarks
    driver.implicitly_wait(10)
    driver.find_element_by_xpath(
        '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[3]/td[2]/textarea').send_keys(df["Remarks"].values[index])


    #Danger::::intimate and go --- restricted it will be only accessed through permission
    #driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[4]/td[2]/input').click()

    now = datetime.now()
    time2 = now.strftime("%H:%M:%S")
    ipnum = df["IP Number"].values[index]
    logs(start_time,time2,claimid,ipnum)


    # uploading documents is successful


def funOfPatientDetails(driver, df, index):
    # inputting adhar uid
    hasText = driver.find_element_by_xpath(
        '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[1]/table/tbody/tr[10]/td[2]/input[1]')
    if len(hasText.text) == 0:
        print('Yes')
        # inputting adhar uid
        driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[1]/table/tbody/tr[10]/td[2]/input[1]').send_keys(
            int(df["Patient's Aadhar/UID card no."].values[index]))

    # inputting address
    hasText = driver.find_element_by_xpath(
        '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[1]/table/tbody/tr[11]/td[2]/input')
    if len(hasText.text) == 0:
        print('Yes')
        # inputting address
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[1]/table/tbody/tr[11]/td[2]/input').send_keys(df["Address"].values[index])

    funOfState(driver, df, index)

    # inputting mobile number
    hasText = driver.find_element_by_xpath(
        '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[1]/table/tbody/tr[16]/td[2]/input')
    if len(hasText.text) == 0:
        print('Yes')

        # inputting mobile number
        driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/form/table[2]/tbody/tr[1]/td/div/div[1]/table/tbody/tr[16]/td[2]/input').send_keys(int(df["Mobile Number"].values[index]))




def funOfPoly(driver, poly):
    if poly == '* Inactive - East Delhi (Preet Vihar)':
        select = Select(driver.find_element_by_id('referredDispensary'))

        select.select_by_visible_text("* Inactive - East Delhi (Preet Vihar)")

    elif poly == '* Inactive - Ghaziabad (Hindon)':
        select = Select(driver.find_element_by_id('referredDispensary'))

        select.select_by_visible_text("* Inactive - Ghaziabad (Hindon)")

    elif poly == '* Inactive - Greater Noida':
        select = Select(driver.find_element_by_id('referredDispensary'))

        select.select_by_visible_text("* Inactive - Greater Noida")

    elif poly == '* Inactive - New Delhi (Lodhi Road)':
        select = Select(driver.find_element_by_id('referredDispensary'))

        select.select_by_visible_text("* Inactive - New Delhi (Lodhi Road)")

    elif poly == '* Inactive - Noida':
        select = Select(driver.find_element_by_id('referredDispensary'))

        select.select_by_visible_text("* Inactive - Noida")

    elif poly == '* Inactive - Timarpur':
        select = Select(driver.find_element_by_id('referredDispensary'))

        select.select_by_visible_text("* Inactive - Timarpur")

    elif poly == 'Delhi Cantt (BHDC)':
        select = Select(driver.find_element_by_id('referredDispensary'))

        select.select_by_visible_text("Delhi Cantt (BHDC)")

    elif poly == 'ECHS Polyclinic - Khanpur':
        select = Select(driver.find_element_by_id('referredDispensary'))

        select.select_by_visible_text("ECHS Polyclinic - Khanpur")

    elif poly == 'Faridabad':
        select = Select(driver.find_element_by_id('referredDispensary'))

        select.select_by_visible_text("Faridabad")

    elif poly == 'Gurgaon':
        select = Select(driver.find_element_by_id('referredDispensary'))

        select.select_by_visible_text("Gurgaon")

    elif poly == 'Gurgaon (Sohana Rd)':
        select = Select(driver.find_element_by_id('referredDispensary'))

        select.select_by_visible_text("Gurgaon (Sohana Rd)")

    elif poly == 'Nuh':
        select = Select(driver.find_element_by_id('referredDispensary'))

        select.select_by_visible_text("Nuh")

    elif poly == 'Palwal':
        select = Select(driver.find_element_by_id('referredDispensary'))

        select.select_by_visible_text("Palwal")

    elif poly == 'RR Polyclinic Army Hospital':
        select = Select(driver.find_element_by_id('referredDispensary'))

        select.select_by_visible_text("RR Polyclinic Army Hospital")

    elif poly == 'Shakurbasti':
        select = Select(driver.find_element_by_id('referredDispensary'))

        select.select_by_visible_text("Shakurbasti")

    elif poly == 'Shakurpur':
        select = Select(driver.find_element_by_id('referredDispensary'))

        select.select_by_visible_text("Shakurpur")


def funOfHour(driver, hr, mins):
    if hr == 0:
        select = Select(driver.find_element_by_name('patientAdmissionHours'))
        select.select_by_visible_text("00")

    elif hr == 1:
        select = Select(driver.find_element_by_name('patientAdmissionHours'))
        select.select_by_visible_text("01")

    elif hr == 2:
        select = Select(driver.find_element_by_name('patientAdmissionHours'))
        select.select_by_visible_text("02")

    elif hr == 3:
        select = Select(driver.find_element_by_name('patientAdmissionHours'))
        select.select_by_visible_text("03")

    elif hr == 4:
        select = Select(driver.find_element_by_name('patientAdmissionHours'))
        select.select_by_visible_text("04")

    elif hr == 5:
        select = Select(driver.find_element_by_name('patientAdmissionHours'))
        select.select_by_visible_text("05")

    elif hr == 6:
        select = Select(driver.find_element_by_name('patientAdmissionHours'))
        select.select_by_visible_text("06")

    elif hr == 7:
        select = Select(driver.find_element_by_name('patientAdmissionHours'))
        select.select_by_visible_text("07")

    elif hr == 8:
        select = Select(driver.find_element_by_name('patientAdmissionHours'))
        select.select_by_visible_text("08")

    elif hr == 9:
        select = Select(driver.find_element_by_name('patientAdmissionHours'))
        select.select_by_visible_text("09")

    elif hr == 10:
        select = Select(driver.find_element_by_name('patientAdmissionHours'))
        select.select_by_visible_text("10")

    elif hr == 11:
        select = Select(driver.find_element_by_name('patientAdmissionHours'))
        select.select_by_visible_text("11")

    elif hr == 12:
        select = Select(driver.find_element_by_name('patientAdmissionHours'))
        select.select_by_visible_text("12")

    elif hr == 13:
        select = Select(driver.find_element_by_name('patientAdmissionHours'))
        select.select_by_visible_text("13")

    elif hr == 14:
        select = Select(driver.find_element_by_name('patientAdmissionHours'))
        select.select_by_visible_text("14")

    elif hr == 15:
        select = Select(driver.find_element_by_name('patientAdmissionHours'))
        select.select_by_visible_text("15")

    elif hr == 16:
        select = Select(driver.find_element_by_name('patientAdmissionHours'))
        select.select_by_visible_text("16")

    elif hr == 17:
        select = Select(driver.find_element_by_name('patientAdmissionHours'))
        select.select_by_visible_text("17")

    elif hr == 18:
        select = Select(driver.find_element_by_name('patientAdmissionHours'))
        select.select_by_visible_text("18")

    elif hr == 19:
        select = Select(driver.find_element_by_name('patientAdmissionHours'))
        select.select_by_visible_text("19")

    elif hr == 20:
        select = Select(driver.find_element_by_name('patientAdmissionHours'))
        select.select_by_visible_text("20")

    elif hr == 21:
        select = Select(driver.find_element_by_name('patientAdmissionHours'))
        select.select_by_visible_text("21")

    elif hr == 22:
        select = Select(driver.find_element_by_name('patientAdmissionHours'))
        select.select_by_visible_text("22")

    elif hr == 23:
        select = Select(driver.find_element_by_name('patientAdmissionHours'))
        select.select_by_visible_text("23")

    # selecting minutes

    if mins == 0:
        select = Select(driver.find_element_by_id('patientAdmissionMins'))
        select.select_by_visible_text("00")

    elif mins == 5:
        select = Select(driver.find_element_by_id('patientAdmissionMins'))
        select.select_by_visible_text("05")

    elif mins == 15:
        select = Select(driver.find_element_by_id('patientAdmissionMins'))
        select.select_by_visible_text("15")

    elif mins == 20:
        select = Select(driver.find_element_by_id('patientAdmissionMins'))
        select.select_by_visible_text("20")

    if mins == 25:
        select = Select(driver.find_element_by_id('patientAdmissionMins'))
        select.select_by_visible_text("25")

    elif mins == 30:
        select = Select(driver.find_element_by_id('patientAdmissionMins'))
        select.select_by_visible_text("30")

    elif mins == 35:
        select = Select(driver.find_element_by_id('patientAdmissionMins'))
        select.select_by_visible_text("35")

    elif mins == 40:
        select = Select(driver.find_element_by_id('patientAdmissionMins'))
        select.select_by_visible_text("40")

    elif mins == 45:
        select = Select(driver.find_element_by_id('patientAdmissionMins'))
        select.select_by_visible_text("45")

    elif mins == 50:
        select = Select(driver.find_element_by_id('patientAdmissionMins'))
        select.select_by_visible_text("50")

    elif mins == 55:
        select = Select(driver.find_element_by_id('patientAdmissionMins'))
        select.select_by_visible_text("55")


def fundOfOPDDate(driver, mn, yr, din):
    # let's tacckle the month---
    if mn == 1:
        select = Select(driver.find_element_by_id('jacsMonths'))
        select.select_by_visible_text("Jan")

    if mn == 2:
        select = Select(driver.find_element_by_id('jacsMonths'))
        select.select_by_visible_text("Feb")

    if mn == 3:
        select = Select(driver.find_element_by_id('jacsMonths'))
        select.select_by_visible_text("Mar")

    if mn == 4:
        select = Select(driver.find_element_by_id('jacsMonths'))
        select.select_by_visible_text("Apr")

    if mn == 5:
        select = Select(driver.find_element_by_id('jacsMonths'))
        select.select_by_visible_text("May")

    if mn == 6:
        select = Select(driver.find_element_by_id('jacsMonths'))
        select.select_by_visible_text("Jun")

    if mn == 7:
        select = Select(driver.find_element_by_id('jacsMonths'))
        select.select_by_visible_text("Jul")

    if mn == 8:
        select = Select(driver.find_element_by_id('jacsMonths'))
        select.select_by_visible_text("Aug")

    if mn == 9:
        select = Select(driver.find_element_by_id('jacsMonths'))
        select.select_by_visible_text("Sep")

    if mn == 10:
        select = Select(driver.find_element_by_id('jacsMonths'))
        select.select_by_visible_text("Oct")

    if mn == 11:
        select = Select(driver.find_element_by_id('jacsMonths'))
        select.select_by_visible_text("Nov")

    if mn == 12:
        select = Select(driver.find_element_by_id('jacsMonths'))
        select.select_by_visible_text("Dec")

    year = 1907

    while (year <= 2026):
        if yr == year:
            select = Select(driver.find_element_by_id('jacsYears'))
            select.select_by_visible_text(str(yr))
            break
        year = year+1

    # let's tackle teh din
    index = 2
    while(index <= 32):
        din2 = driver.find_element_by_id('jacsCell_'+str(index))
        d = din2.text
        # print(d)
        if d == str(din):
            driver.find_element_by_id('jacsCell_'+str(index)).click()
            break
        index = index+1


def funOfEDDDate(driver, edin, emn, eyr):
    # let's tacckle the month---
    if emn == 1:
        select = Select(driver.find_element_by_id('jacsMonths'))
        select.select_by_visible_text("Jan")

    if emn == 2:
        select = Select(driver.find_element_by_id('jacsMonths'))
        select.select_by_visible_text("Feb")

    if emn == 3:
        select = Select(driver.find_element_by_id('jacsMonths'))
        select.select_by_visible_text("Mar")

    if emn == 4:
        select = Select(driver.find_element_by_id('jacsMonths'))
        select.select_by_visible_text("Apr")

    if emn == 5:
        select = Select(driver.find_element_by_id('jacsMonths'))
        select.select_by_visible_text("May")

    if emn == 6:
        select = Select(driver.find_element_by_id('jacsMonths'))
        select.select_by_visible_text("Jun")

    if emn == 7:
        select = Select(driver.find_element_by_id('jacsMonths'))
        select.select_by_visible_text("Jul")

    if emn == 8:
        select = Select(driver.find_element_by_id('jacsMonths'))
        select.select_by_visible_text("Aug")

    if emn == 9:
        select = Select(driver.find_element_by_id('jacsMonths'))
        select.select_by_visible_text("Sep")

    if emn == 10:
        select = Select(driver.find_element_by_id('jacsMonths'))
        select.select_by_visible_text("Oct")

    if emn == 11:
        select = Select(driver.find_element_by_id('jacsMonths'))
        select.select_by_visible_text("Nov")

    if emn == 12:
        select = Select(driver.find_element_by_id('jacsMonths'))
        select.select_by_visible_text("Dec")

    year = 1907

    while (year <= 2026):
        if eyr == year:
            select = Select(driver.find_element_by_id('jacsYears'))
            select.select_by_visible_text(str(eyr))
            break
        else:
            print(eyr)
            # print(year)
            # print("sorry")
        year = year+1

    # let's tackle teh din
    index = 2
    while(index <= 32):
        din2 = driver.find_element_by_id('jacsCell_'+str(index))
        d = din2.text
        # print(d)
        if d == str(edin):
            
            driver.find_element_by_id('jacsCell_'+str(index)).click()
            break
        else:
            print(d)
            # print(edin)
            # print("sorry")
        index = index+1


def funOfState(driver, df, index):
    # selecting state
    # dropdown7-state
    state = df["State"].values[index]

    if state == 'Andaman and Nicobar Islands':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Andaman and Nicobar Islands")

    elif state == 'Andhra Pradesh':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Andhra Pradesh")

    elif state == 'Arunachal Pradesh':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Arunachal Pradesh")

    elif state == 'Assam':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Assam")

    elif state == 'Bihar':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Bihar")

    elif state == 'Chandigarh':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Chandigarh")

    elif state == 'Chhattisgarh':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Chhattisgarh")

    elif state == 'Dadra and Nagar Haveli':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Dadra and Nagar Haveli")

    elif state == 'Daman and Diu':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Daman and Diu")

    elif state == 'Delhi':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Delhi")

    elif state == 'Goa':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Goa")

    elif state == 'Gujarat':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Gujarat")

    elif state == 'Haryana':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Haryana")

    elif state == 'Himachal Pradesh':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Himachal Pradesh")

    elif state == 'Jammu and Kashmir':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Jammu and Kashmir")

    elif state == 'Jharkhand':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Jharkhand")

    elif state == 'Karnataka':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Karnataka")

    elif state == 'Kerala':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Kerala")

    elif state == 'Lakshadweep':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Lakshadweep")

    elif state == 'Madhya Pradesh':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Madhya Pradesh")

    elif state == 'Maharashtra':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Maharashtra")

    elif state == 'Manipur':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Manipur")

    elif state == 'Meghalaya':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Meghalaya")

    elif state == 'Mizoram':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Mizoram")

    elif state == 'NA':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("NA")

    elif state == 'Nagaland':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Nagaland")

    elif state == 'Nepal':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Nepal")

    elif state == 'Orissa':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Orissa")

    elif state == 'Puducherry':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Puducherry")

    elif state == 'Punjab':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Punjab")

    elif state == 'Rajasthan':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Rajasthan")

    elif state == 'Sikkim':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Sikkim")

    elif state == 'Tamil Nadu':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Tamil Nadu")

    elif state == 'Telengana':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Telengana")

    elif state == 'Tripura':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Tripura")

    elif state == 'Uttar Pradesh':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Uttar Pradesh")

    elif state == 'Uttarakhand':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("Uttarakhand")

    elif state == 'West Bengal':
        select = Select(driver.find_element_by_id('patientState'))

        select.select_by_visible_text("West Bengal")



# Driver code
def main():
    driver = driver_init()

    #time generator
    time1 = datetime.now().strftime("%H:%M:%S")

    # xls sheet read
    file = os.path.join(config.PROJECT_ROOT, "Patient Details Form.csv")
    df = pd.read_csv(file)


    # single_run(driver, df, time1, 1)

    continuous_run(driver, df, time1)



def single_run(driver, df, time1, index):
    loginPage(driver)
    secondPage(driver, df, index)
    PatientDetails(driver, df, index)
    admissionFill(driver, df, index)
    patientHistory(driver, df, index)
    clinicFind(driver, df, index)
    diagnose(driver, df, index)
    proposeTreat(driver, df, index)
    upDoc(driver, df, time1, index)

def continuous_run(driver, df, time1):
    loginPage(driver)
    for index in df.index:
        secondPage(driver, df, index)
        PatientDetails(driver, df, index)
        admissionFill(driver, df, index)
        patientHistory(driver, df, index)
        clinicFind(driver, df, index)
        diagnose(driver, df, index)
        proposeTreat(driver, df, index)
        upDoc(driver, df, time1, index)

if __name__ == "__main__":
    main()
import pandas as pd
import bs4
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome(executable_path=r"/Users/chesterpoon/chromedriver")
browser.get('https://www.linkedin.com/')

log_name = browser.find_element_by_id('login-email')
log_name.send_keys('username@email.com')
log_pass = browser.find_element_by_id('login-password')
log_pass.send_keys('password')
login_but = browser.find_element_by_id('login-submit')
login_but.click()

jobs_link = browser.find_element_by_id('jobs-tab-icon')
jobs_link.click()

while True:
    try:
        search_jobs = browser.find_element_by_css_selector('input[id*=jobs-search-box-keyword-id-ember]')
    except:
        continue
    break

search_jobs = browser.find_element_by_css_selector('input[id*=jobs-search-box-keyword-id-ember]')
search_jobs.send_keys('data scientist')
search_go = browser.find_element_by_css_selector(
    'button.jobs-search-box__submit-button.button-secondary-large-inverse')
search_go.click()

skill_list = []
title_list = []
industry_list = []
job_id = []

for p in range(2,42):
    def pg_dwn():
        while True:
            try:
                browser.find_element_by_css_selector(
                    'div[class*=jobs-search-results--is-two-pane]').send_keys(Keys.PAGE_DOWN)
            except:
                continue
            break

    for i in range(25):
        pg_dwn()

    url = browser.current_url
    source = browser.page_source
    html = bs4.BeautifulSoup(source, "lxml")

    while True:
        try:
            job = browser.find_elements_by_class_name('job-card-search__title-line')
            jtitle = html.find_all(
                attrs={"class": "job-card-search__title lt-line-clamp lt-line-clamp--multi-line ember-view"})
        except:
            continue
        break

    for i in range(len(job)-1):
        job[i].click()
        time.sleep(2.25)
        url = browser.current_url
        source = browser.page_source
        html = bs4.BeautifulSoup(source, "lxml")
        skills = html.find_all(attrs={"class": "jobs-ppc-criteria__value t-14 t-black t-normal ml2 block"})
        industry = html.find_all(attrs={"class": "jobs-box__list-item jobs-description-details__list-item"})
        j_id = random.choice(string.ascii_lowercase) + str(random.randrange(10000))

        for j in range(len(skills)):
            s = skills[j].getText()
            t = jtitle[i].getText()
            ind = industry[0].getText()
            skill_list.append(s)
            title_list.append(t)
            industry_list.append(ind)
            job_id.append(j_id)

    if p == 41:
        print("Last page complete")
        break

    print("Starting page " + str(p))
    page = browser.find_element_by_xpath('//button[text()="' + str(p) +'"]')
    page.click()
    time.sleep(2)

skillsdf = pd.DataFrame(
    {'job_id': job_id,
     'skills': skill_list,
     'title': title_list,
     "industry": industry_list})
skillsdf.to_csv('skills.csv', index=False)

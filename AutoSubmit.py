import time


from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys


def SelectBox(_xpath, _select):
    driver.find_element_by_xpath(_xpath).send_keys(Keys.ENTER)

    time.sleep(0.2)
    driver.find_element_by_link_text(_select).send_keys(Keys.ENTER)
    time.sleep(2)

def getMajorName(dom):
    return  dom.get('value')


class_infor = []
table_header = []


#------------- User Info -----------
student_id = '201524532'
student_pw = 'wlwhsvkdnj1!'
pnu_url = 'https://e-onestop.pusan.ac.kr/common/login'
samsung_id = 'koogk7@gmail.com'
samsung_pw = '960115!a'
samsung_url = 'http://www.samsungcareers.com/main.html'

#크롬 드라이버의 위치를 지정
driver = webdriver.Chrome('./util/chromedriver')

driver.implicitly_wait(5)

driver.get(pnu_url)

#-------------PNU OneStop 성적 Parsing-------------------

#id, student_pw 입력
driver.find_element_by_id("id").send_keys(student_id)
driver.find_element_by_id("pw").send_keys(student_pw)


#Login 버튼 클릭
driver.find_element_by_xpath('//*[@id="wrapper"]/section/div/div[2]/div[2]/form/footer/button').click()



#전체성적 조회 버튼 클릭
driver.find_element_by_xpath('//*[@id="topMain"]/li[4]/a/span').click()
driver.find_element_by_xpath('//*[@id="topMain"]/li[4]/ul/li[2]/a').click()
driver.find_element_by_xpath('//*[@id="topMain"]/li[4]/ul/li[2]/ul/li[2]').click()

time.sleep(1)

#전체성적 페이지 가져옴
html = driver.page_source # 페이지의 elements모두 가져오기
soup = BeautifulSoup(html, 'html.parser') # BeautifulSoup사용하기


#header 가져오기
html_th = soup.select('thead > tr > td')

for v in html_th :
    table_header.append(v.get_text())
print(table_header)

#data 가져오기
html_rows = soup.select('table#tb1 > tbody > tr')
for v in html_rows:
    row = v.select('td')
    print(row)
    print(len(row))
    if len(row) == 1:
        break
    if row[1]['class'][0] != 'table_box_background':
        continue

    _year = row[0].get_text()
    semester = row[1].get_text()
    subject_cate = row[2].get_text()
    subject_name = row[3].get_text()
    credit = row[4].get_text()
    grade = row[5].get_text()
    temp = {
        table_header[0]: _year,
        table_header[1]: semester,
        table_header[2]: subject_cate,
        table_header[3]: subject_name,
        table_header[4]: credit,
        table_header[5]: grade
    }
    class_infor.append(temp)

print(class_infor)

#-------------Samsung -------------------
driver.get(samsung_url)


#로그인화면 이동
# driver.find_element_by_xpath('//*[@id="login"]/a[1]').click()
# 클릭이 되지 않을 때 아래와 같이 Enter를 넣어주면 해결이 된다.
driver.find_element_by_xpath('//*[@id="login"]/a[1]').send_keys(Keys.ENTER)

#로그인
driver.find_element_by_xpath('//*[@id="email"]').send_keys(samsung_id)
driver.find_element_by_xpath('//*[@id="password"]').send_keys(samsung_pw)
driver.find_element_by_xpath('//*[@id="budiv_mySheet_comLogin"]/a').send_keys(Keys.ENTER)

#팝업닫기
_alert = Alert(driver)
_alert.accept()

driver.find_element_by_xpath('//*[@id="cont"]/div[1]/ul/div/dl/dd[1]/p/span/a').send_keys(Keys.ENTER)

driver.find_element_by_xpath('//*[@id="masTable1"]/tr/td[3]/a').send_keys(Keys.ENTER)
_alert.accept()

driver.find_element_by_xpath('//*[@id="cont"]/table[1]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div[2]/ul/li[3]/a').send_keys(Keys.ENTER)
_alert.accept()

#정보입력

time.sleep(3)
html = driver.page_source # 페이지의 elements모두 가져오기
soup = BeautifulSoup(html, 'html.parser') # BeautifulSoup사용하기


#이전의 입력된 과목들 체크
curri_majors = soup.select('#majdetTable .RESUME_FORM_4[name=majcurrinm]')
curri_majors = list(map(getMajorName, curri_majors))

print(curri_majors)

major_bools = [True for i in range(0,len(curri_majors))]


already_major = {
 curri_majors:  major_bool for curri_majors, major_bool in zip(curri_majors, major_bools)
}

print(already_major)


SelectBox('//*[@id="tmp_schlcarrcdId"]', '학사')
SelectBox('//*[@id="tmp_majcdId"]', '정보컴퓨터공학(부산대)')
SelectBox('//*[@id="tmp_retakeynId"]', 'N(1회수강)')
SelectBox('//*[@id="abeektgtynId"]', '비대상')
driver.find_element_by_xpath('//*[@id="majcntTable"]/thead/tr[2]/td[6]/input').send_keys(str(len(class_infor)))
cnt = 0
for item in class_infor:
    if cnt == 10 :
        _alert.accept()
        driver.find_element_by_xpath('//*[@id="budiv_mySheet_Save"]/a').send_keys(Keys.ENTER)
        cnt = 0
        _alert.accept()
        _alert.accept()

    t_year = item['년도']
    t_sem = item['학기']
    t_credit = item['학점'].replace('.00','')
    t_grade = item['성적등급'].replace('0','')
    t_grade = t_grade.replace(' ','')
    t_name = item['교과목명']
    t_cate = item['교과구분']

    if t_name in already_major:
        print(t_name + " 중복")
        continue

    if t_grade == 'U':
        t_grade = 'FAIL'
    if t_grade == 'S':
        t_grade = 'PASS'

    if (t_cate == '교양선택') | (t_cate == '교양필수') | (t_cate == '일반선택'):
        t_cate = '교양기타'
    if (t_cate == '전공기초') | (t_cate == '전공선택') | (t_cate == '전공필수') | (t_cate == '심화전공'):
        t_cate = '전공'
    if (t_sem == '겨울') | (t_sem == '여름'):
        t_sem = t_sem + "계절"

    print("------------------%s---------------" %cnt)
    print(t_name)
    print(t_cate)
    print(t_grade)
    print(t_credit)

    SelectBox('//*[@id="tmp_majtypecdId"]', t_cate)
    SelectBox('//*[@id="tmp_regyrId"]', t_year)
    SelectBox('//*[@id="tmp_semstId"]', t_sem)

    if int(t_credit) > 10:
        SelectBox('//*[@id="tmp_obtptId"]', '기타')
        driver.find_element_by_xpath('//*[@id="tmp_obtptetc"]').send_keys(t_credit)
    else:
        t_credit = str(t_credit)+'학점'
        SelectBox('//*[@id="tmp_obtptId"]', t_credit)

    SelectBox('//*[@id="tmp_obtpovId"]', t_grade)

    driver.find_element_by_xpath('//*[@id="tmp_majcurrinm"]').send_keys(t_name)
    driver.find_element_by_xpath('//*[@id="budiv_mySheet_AddMajdet"]/a').send_keys(Keys.ENTER)
    cnt +=1


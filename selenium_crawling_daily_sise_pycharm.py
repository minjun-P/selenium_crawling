from pprint import pprint


def choochool(result_list, table, column_set=False):
    # 테이블에서 행 추출
    rows = table.find_elements_by_css_selector('tr')
    for row in rows:
        # 내용 없는 행 제거
        if len(row.text.strip()) > 0:

            new_list = row.text.split(' ')

            # 왜 try except을 쓰는가? elem이 있는 것도 있고 없는 것도 있음.
            # 그러니 없는 친구는 걍 무시하고 싶은데,
            # 조건문을 달기보단 오류가 뜨게 만들고 무시하는게 효율적임

            try:
                row.find_element_by_css_selector('td:nth-child(3) img').get_attribute('alt') == '하락'
                new_list[2] = '-' + new_list[2]
            except:
                pass
            '''해당 row 변수에 있던 걸 list로 옮겨옴'''

            '''열제목이 중복 수집되는 걸 방지하기 위함, 함수 인수에 bool 변수 추가'''
            if not column_set:
                if row.text[0] == '날':
                    pass
                else:
                    result_list.append(new_list)
            else:
                result_list.append(new_list)

    return result_list
# reuslt list에 각각의 행이 변환된 new list를 list화 해서 연결시켜 담음


def main_crawling():
    # 시간 측정
    start = time.time()
    # 페이지 이동
    last_page = driver.find_element_by_css_selector('td.pgRR > a').get_attribute('href').split('=')[-1]
    # 빈 리스트 만들기
    result_list = []
    progress = 10
    for i in range(1, int(last_page) + 1):
        # 버튼 선택하기 및 클릭하기
        page_button_list = driver.find_element_by_css_selector('tbody:nth-child(2)')
        page_button = page_button_list.find_element_by_link_text('{}'.format(i))
        page_button.click()
        # 데이터 뽑을 테이블 요소 가져오기
        table = driver.find_element_by_css_selector('tbody')
        # 리스트에 테이블 데이터 담기 - 리스트 요소당 한 행
        if i == 1:
            result_list = choochool(result_list, table, True)
        else:
            result_list = choochool(result_list, table)

        if (i / int(last_page)) >= progress / 100:
            print(str(round(i / int(last_page) * 100)) + '% 진행 / 경과시간 : ' + str(time.time() - start))
            progress += 10
        # 10 단위로 다음 페이지로 넘어가니깐 아래 조건문 설정
        if i % 10 == 0:
            # 셀리늄 오류 방지 위해서 다시 요소 크롤링
            page_button_list = driver.find_element_by_css_selector('tbody:nth-child(2)')
            page_button = page_button_list.find_element_by_link_text('다음')
            page_button.click()

    return result_list

from selenium import webdriver
import pandas as pd
import time
#시간 재기
start = time.time()
#코드 입력 및 url 설정
url = 'https://finance.naver.com/item/sise.nhn?code='
code = input('코드? ')
final_url = url+code
#크롬 동작 및 url 이동
driver = webdriver.Chrome('chromedriver')
driver.get(final_url)
#iframe 내부로 이동
daily_table = driver.find_element_by_css_selector('#content > div.section.inner_sub > iframe:nth-child(4)')
driver.switch_to.frame(daily_table)

result = main_crawling()
print(str(time.time() - start) +'만큼 소요됐습니다')
df = pd.DataFrame(result[1:],columns=result[0])
df = df.set_index('날짜')

pprint(df)



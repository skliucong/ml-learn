# coding = utf-8
from time import sleep
from selenium import webdriver
import json

def get_news(topicword):
    page=0
    items=0
    browser = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
    browser.get("http://search.people.com.cn/cnpeople/news/noNewsResult.jsp")
    browser.find_element_by_id("keyword").send_keys(topicword)
    browser.find_element_by_class_name("tt03").find_element_by_xpath("//table/tbody/tr/td[2]/img").click()

    f = open('success_'+topicword+'_movies.csv', 'w')
    error_f = open('error_topicword_movies.csv', 'w')


    for j in range(100):
        try:
            ullis = browser.find_element_by_class_name("w800").find_elements_by_xpath("ul")
        except:
            sleep(2)
            browser = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")

            browser.get("http://search.people.com.cn/cnpeople/news/noNewsResult.jsp")
            browser.find_element_by_id("keyword").send_keys(topicword)
            browser.find_element_by_class_name("tt03").find_element_by_xpath("//table/tbody/tr/td[2]/img").click()
            for j in range(page):
                sleep(1)
                browser.find_element_by_class_name("show_nav_bar").find_element_by_xpath(".//a[last()]").click()
            ullis = browser.find_element_by_class_name("w800").find_elements_by_xpath("ul")


        for i in range(len(ullis)):
                link=ullis[i].find_element_by_xpath("li[1]/b/a").get_attribute('href')
                text=ullis[i].find_element_by_xpath("li[1]/b/a").text


                js = 'window.open("' + link + '")'

                browser.set_page_load_timeout(30)

                browser.execute_script(js)
                browser.switch_to_window(browser.window_handles[1])



                try:
                    neirong = browser.find_element_by_xpath('//div[@class="box_con"]').text
                except:
                    try:
                        neirong = browser.find_element_by_xpath('//div[@class="text_c"]').text
                    except:
                        try:
                            neirong= browser.find_element_by_xpath('//div[@class="text_con"]').text
                        except:
                            try:
                                neirong = browser.find_element_by_xpath('//div[@class="text clear"]').text
                            except:
                                try:
                                    neirong = browser.find_element_by_xpath('//div[@class="articleCont"]').text
                                except:
                                    print("error!!")
                                    neirong=None

                browser.close()
                browser.switch_to_window(browser.window_handles[0])
                sleep(0.5)
                print("#####################"+str(items)+"#######################")

                if neirong!=None:
                    neirong=neirong.replace("\n","").replace(" ","")
                    print(link,text,neirong)
                    data_json = json.dumps({'biaoti':text,'pageNum':page,'IDNum':items,'link':link,'neirong':neirong})
                    f.write(data_json+'\n')
                    items=items+1


        browser.find_element_by_class_name("show_nav_bar").find_element_by_xpath(".//a[last()]").click()
        page=page+1

    f.close()
    error_f.close()

if __name__ == '__main__':
    topicword_lis=["富强","民主","文明","和谐","自由","平等","公正","法治","爱国","敬业","诚信","友善"]
    for item in topicword_lis:
        get_news(item)
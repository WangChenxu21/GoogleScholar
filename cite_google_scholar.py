from time import sleep
from urllib import parse

from selenium import webdriver


def cited_by_author(paper, author):
    """查找有无特定作者引用特定文章

    Args:
        paper: 待查找的文章列表
        author: 候选的作者列表
    """
    # 搜索的主页面
    strto_pn = parse.quote("{}".format(paper))
    url = gg_search_url + strto_pn
    browser.get(url)
    
    # 被引用页面
    element = browser.find_element_by_css_selector("[class='gs_r gs_or gs_scl']")
    element = element.find_element_by_css_selector("[class='gs_ri']")
    element = element.find_element_by_css_selector("[class='gs_fl']")
    try:
        element = element.find_element_by_partial_link_text("被引用次数")
        element.click()
    except:
        print('0 cites!')
        return
    
    element = browser.find_element_by_id("gs_res_ccl_top")
    element = element.find_element_by_id("gs_rt_hdr_cites")
    element = element.find_element_by_id("gs_scipsc")
    element = element.find_element_by_css_selector("[class='gs_chk']")
    element.click()

    element = browser.find_element_by_id("gs_hdr")
    element = element.find_element_by_id("gs_hdr_md")
    element = element.find_element_by_id("gs_hdr_frm")
    element.find_element_by_css_selector("[class='gs_in_txt gs_in_ac']").clear()
    element.find_element_by_css_selector("[class='gs_in_txt gs_in_ac']").send_keys('{}'.format(author))
    element.find_element_by_id("gs_hdr_tsb").click()
        
    # paper urls
    urls = []
    page = 1
    
    while 1:
        for idx in range((page-1)*10, page*10):
            try:
                element = browser.find_element_by_css_selector("[class='gs_r gs_or gs_scl']")
                element = element.find_element_by_css_selector("[class='gs_rt']")
                element = element.find_elements_by_xpath("//*[@data-rp={}]".format(idx))[0]
                id = element.get_attribute('data-cid')
                element = element.find_element_by_id(id)
                url = element.get_attribute('href')
                urls.append(url)
                print('url: {}'.format(url, url))
            except:
                break
    
        # 有后面的页
        try:
            element = browser.find_element_by_id("gs_res_ccl_bot")
            element = element.find_element_by_id("gs_n")
            element = element.find_element_by_partial_link_text('下一页')
            element.click()
            print('下一页')
            page += 1
        except:
            break


if __name__ == "__main__":
    author_list = ["author:Qian author:Du", "author:JA author:Benediktsson"]

    paper_list = []
    with open("paper_list.txt", encoding="utf-8") as f:
        datas = f.readlines()
    for data in datas:
        paper_name = data.split('.')[1]
        paper_name = paper_name.split(',')[0]
        paper_list.append(paper_name)

    # init
    driver_path = r"C:/Program Files (x86)/Google/Chrome/Application/chromedriver"
    option_path = r"C:/Users/WANGCHENXU/AppData/Local/Google/Chrome/User Data/"
    gg_search_url = r"https://scholar.google.com/scholar?hl=zh-CN&as_sdt=0%2C5&inst=1597255436240989024&q="

    option = webdriver.ChromeOptions()
    browser = webdriver.Chrome(executable_path = driver_path, options = option)
    browser.set_window_size(800, 800)

    # start search
    for i, paper in enumerate(paper_list):
        print('paper_name: {}'.format(paper))
        for author in author_list:
            print('author_name: {}'.format(author))
            sleep(1)
            cited_by_author(paper, author)

        sleep(10)
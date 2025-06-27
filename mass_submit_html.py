from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchWindowException, WebDriverException
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import random
import os
from query_excel_info import load_source_data
from query_excel_info import set_dest_data
def human_delay(min=0.5, max=2.5):
    time.sleep(random.uniform(min, max))

def handle_know_button(browser):
    #处理知道了弹窗按钮
    try:
        # 定义按钮定位器（使用span文本定位）
        button_locator = (By.XPATH, "//button[.//span[text()='我知道了']]")
        
        # 使用短时间等待按钮出现（不抛出异常）
        button = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located(button_locator)
        )
        # 尝试标准点击
        move_click(browser, button)
    except TimeoutException:
    # 等待超时表示按钮不存在
        pass

def focus_element(browser, focus_element):
    # 确保输入框可见（滚动到视图）
    is_focused = browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", focus_element)
    human_delay()  

    if not is_focused:
        # 如果仍未获得焦点,使用JavaScript聚焦
        browser.execute_script("arguments[0].focus();", focus_element)
        human_delay()  
        is_focused = browser.execute_script("return document.activeElement === arguments[0]", focus_element)
        print('JavaScript聚焦')
    
    print(f"JS聚焦后是否获得焦点: {is_focused}")  

def input_element(browser, company_name):
    #输入企业名称
    human_delay()  
    input_xpath = "//input[@class='el-input__inner' and @placeholder='请输入企业名称']"

    input_elements = WebDriverWait(browser, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, input_xpath))
                )     

    input_element = input_elements[1]  # 索引0是第一个按钮，1是第二个
    move_click(browser, input_element)
    input_element.send_keys(company_name)

def select_company(browser, company_name):
    #选中第一行
    human_delay()  
    radio_xpath = f"//a[contains(text(), '{company_name}')]/ancestor::tr"
    radio_row = browser.find_element(By.XPATH, radio_xpath)
    radio_btn = radio_row.find_element(By.CSS_SELECTOR, "input[type='radio']")
    browser.execute_script("arguments[0].click();", radio_btn)

    human_delay()  
    select_xpath = "//a[contains(text(), '选择') and @class = 'btn']"
    select_btn = browser.find_element(By.XPATH, select_xpath)
    move_click(browser, select_btn)

def click_query_btn(browser):
    # 定位查询按钮
    button_xpath = "//button[.//span[text()='查询 ']]"
    buttons = WebDriverWait(browser, 15).until(
        EC.presence_of_all_elements_located((By.XPATH, button_xpath))
        )
    
    target_button = buttons[1]  # 索引0是第一个按钮，1是第二个
    move_click(browser, target_button)


def click_nowhere(browser, inspection_img, connetc_img):
    #选择查无下落按钮
    human_delay()  
    element_xpath = "//label[contains(@class, 'el-radio') \
        and .//span[@class='el-radio__label' \
            and contains(text(), '查无下落')]]"
    radio_row = browser.find_element(By.XPATH, element_xpath)
    radio_row.click()

    #选择日期
    element_xpath = "//input[@placeholder='请选择日期' \
        and @class='el-input__inner']"
    radio_row = browser.find_element(By.XPATH, element_xpath)
    radio_row.click()
    human_delay()  
    move_scroll(browser)

    #选择今天
    element_xpath = "//td[@class = 'available today']"
    today_btn = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, element_xpath))
        )
    today_btn.click()
    human_delay()  

    #输入检查情况
    element_xpath = "//span[@contenteditable='true' \
            and contains(@class, 'my-span-input-class') \
            and contains(@class, 'span-fact-reason-input') \
            and @placeholder='请输入，1000字以内']"
    input_span = browser.find_element(By.XPATH, element_xpath)
    input_span.click()
    human_delay()  
    input_span.send_keys('工作人员经现场核查未找到该公司，通过登记的住所无法取得联系')

    #上传检查照片
    upload_image(browser, '现场照片：', inspection_img)

    #上传联系记录
    upload_image(browser, '联系记录：', connetc_img)


def upload_image(browser, label_text, image_path):
    """上传图片到指定区域"""
    try:
        # 定位标签元素
        label_xpath = f"//label[contains(@class, 'el-form-item__label') and contains(text(), '{label_text}')]"
        label = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, label_xpath))
        )
        
        # 定位父容器
        container = label.find_element(By.XPATH, 
            "./following-sibling::div[@class='el-form-item__content']")
        
        # 定位上传按钮区域
        upload_div = container.find_element(By.XPATH, 
            ".//div[contains(@class, 'upload-file') and contains(@class, 'align-center')]")
        
        # 定位隐藏的文件输入框
        file_input = upload_div.find_element(By.XPATH, 
            ".//input[@type='file' and @name='file' and @accept='.png,.pdf,.jpg']")
        

        # 上传文件
        file_input.send_keys(image_path)
        #print(f"✅ {label_text}上传成功: {os.path.basename(image_path)}")       
        human_delay()
        
    except Exception as e:
        print(f"❌ {label_text}上传失败: {str(e)}")

def undetected_chromedriver():
    # 配置Edge选项 - 正确方式
    edge_options = Options()

    # 添加参数的正确方法
    arguments = [
        "--disable-blink-features=AutomationControlled",
        "--disable-infobars",
        "--disable-popup-blocking",
        "--disable-extensions",
        "--disable-default-apps",
        "--disable-web-security",
        "--disable-dev-shm-usage",
        "--no-sandbox",
        "--disable-gpu",
        "--disable-software-rasterizer",
        "--disable-logging",
        "--log-level=3",
        "start-maximized",
        "--window-size=1920,1080"
    ]

    for arg in arguments:
        edge_options.add_argument(arg)

    # 随机化用户代理
    user_agents = [
        # 添加多个常见的Edge用户代理
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69"
    ]
    selected_ua = random.choice(user_agents)
    edge_options.add_argument(f"user-agent={selected_ua}")

    # 禁用自动化标志
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    edge_options.add_experimental_option('useAutomationExtension', False)

    # 创建Edge驱动服务
    executable_path='D:\\python\\Python37\\Scripts\\msedgedriver.exe'
    service = Service(executable_path)

    # 初始化浏览器
    driver = webdriver.Edge(service=service, options=edge_options)

    # 执行CDP命令覆盖WebDriver属性
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3]
        });
        Object.defineProperty(navigator, 'languages', {
            get: () => ['zh-CN', 'zh', 'en']
        });
        window.chrome = {
            runtime: {},
            app: { isInstalled: false }
        };
        """
    })

    # 随机化浏览器指纹
    driver.execute_cdp_cmd("Emulation.setUserAgentOverride", {
        "userAgent": selected_ua,
        "platform": "Win32",
        "acceptLanguage": "zh-CN,zh;q=0.9,en;q=0.8",
        "userAgentMetadata": {
            "brands": [
                {"brand": "Not A;Brand", "version": "99"},
                {"brand": "Chromium", "version": "116"},
                {"brand": "Microsoft Edge", "version": "116"}
            ],
            "fullVersion": "116.0.1938.69",
            "platform": "Windows",
            "platformVersion": "10.0.0",
            "architecture": "x86",
            "model": "",
            "mobile": False
        }
    })

    # 设置其他指纹参数
    driver.execute_cdp_cmd("Emulation.setScriptExecutionDisabled", {"value": False})
    driver.execute_cdp_cmd("Emulation.setTouchEmulationEnabled", {"enabled": False})
    driver.execute_cdp_cmd("Emulation.setEmitTouchEventsForMouse", {"enabled": False})
    return driver

def move_click(browser, element):
    ## 模拟人类操作：移动鼠标到按钮，稍作停留后点击
    ActionChains(browser).move_to_element(element).pause(
            random.uniform(0.3, 1.0)).click().perform()

def move_scroll(browser):
    # 模拟按下向下箭头键的次数
    action_chains = ActionChains(browser)
    press_times = 10
    for i in range(press_times):
        action_chains.send_keys("\ue015").perform()  # "\ue015"是向下箭头键的编码
        time.sleep(0.1)
    human_delay() 

def click_submit(browser):
    #点击提交按钮，并判断是否提交成功
    element_xpath = "//a[@class = 'btn submit' \
        and text()= '提交审批']"
    radio_row = browser.find_element(By.XPATH, element_xpath)
    move_click(browser, radio_row)

    try:
        # 等待弹窗标题出现
        element_xpath = "//div[contains(@class, 'el-dialog__header')] \
                //span[contains(@class, 'title') and text()='提交审批']"
        dialog_element = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH,element_xpath))
            )
        
        #点击同意按钮
        element_xpath = "//button[contains(@class, 'el-button') and .//span[text()='同意']]"
        agree_btn = browser.find_element(By.XPATH, element_xpath)        
        move_click(browser, agree_btn)

        #勾选领导
        element_xpath = "//label[contains(@class, 'el-checkbox') and " \
        ".//span[@class='el-checkbox__label' and contains(text(), '任建武')]]"
        check_box = browser.find_element(By.XPATH, element_xpath) 
        move_click(browser, check_box)

        #点击提交
        element_xpath = "//div[@class='el-dialog__footer'] " \
        "//a[@class='btn submit' and text()='提交']"
        check_box = browser.find_element(By.XPATH, element_xpath) 
        move_click(browser, check_box)

        #检测提交结果
        if check_duplicate_record_error(browser):
            return '提交成功'
        else:
            return '已有列异记录，提交失败'

    except:
        #没出现，则跳过
        return '没有出现审批按钮'


def check_duplicate_record_error(browser, timeout=5):
    """
    检测是否存在重复记录错误消息
    :param driver: WebDriver实例
    :param timeout: 检测超时时间（秒）
    :return: 如果检测到错误消息返回True，否则返回False
    """
    try:
        # 构建错误消息的XPath定位器
        error_xpath = (
            "//div[contains(@class, 'el-message--error')]"
            "//p[@class='el-message__content' and contains(text(), '该企业已经存在一条因查无下落列异在列的记录，无法重复列入')]"
        )
        
        # 显式等待错误消息出现
        error_message = WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located((By.XPATH, error_xpath)))
        
        # 如果找到错误消息
        if error_message.is_displayed():
            print("⚠️ 检测到重复记录错误消息:", error_message.text)
            return False
    except Exception:
        # 超时或其他异常表示未找到错误消息
        return True

def click_cancle(browser):
    element_xpath = "//a[contains(@class ,'btn cancel') \
        and text()= '取消']"
    cancel_btn = browser.find_element(By.XPATH, element_xpath)
    move_click(browser, cancel_btn)

def process_all_list(browser):
    #打开文件，把所有名单进行提交，最后将结果保存至文件
    report_dir = 'D:\\瞿溪市监所\\信用监管\\年报\\'
    filename = report_dir + '年报分类名单管理导出-2025年06月26日未年报企业 测试.xls'
    user_info_map = load_source_data(filename, '企业名称', ['法定代表人联系电话', '提交情况'])
    #上传检查照片
    inspection_img = report_dir +'列异现场检查照片\\力西特 潘骏.jpg'    

    #上传联系记录
    connetc_dir = report_dir + '列异电话照片\\'    

    icount = 1
    for key_com in user_info_map:        
        company_name = key_com
        telephone_num = user_info_map[key_com][0]   
        connetc_img = connetc_dir + str(telephone_num) + '.jpg' 
        #首先检测电话照片有了没有，没有的直接跳过
        if not os.path.isfile(connetc_img):
            #文件不存在则跳过
            user_info_map[key_com][1] = '没有电话照片'
            continue

        #点击新增申请按钮
        time.sleep(2)
        button_xpath = "//button[.//span[text()='新增列入申请']]"
        button = WebDriverWait(browser, 30).until(
                EC.element_to_be_clickable((By.XPATH, button_xpath))
            )
        move_click(browser, button)

        #处理我知道了按钮
        time.sleep(2)
        handle_know_button(browser)

        #点击+号按钮
        time.sleep(2)
        button_xpath = "i.svg-icon-mt-plus"
        button = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, button_xpath))
                    )
        move_click(browser, button)

        #输入企业名称    
        input_element(browser, company_name)

        #点击查询按钮
        click_query_btn(browser)

        #勾选查询结果，点击选择
        select_company(browser, company_name)

        #勾选查无下落按钮，输入检查情况， 上传照片
        click_nowhere(browser, inspection_img, connetc_img)
            
        #提交按钮
        result = click_submit(browser)
        print(f'处理第{icount}个：{company_name}处理完成，处理结果：'+ result)
        user_info_map[key_com][1] = result
        
        icount += 1
        
    
    #记录提交结果   
    set_dest_data(filename, user_info_map, ['X','Y'],['联系方式','提交情况'], 2)

            
browser = undetected_chromedriver()
browser.maximize_window()
browser.get('https://portal.zjamr.zj.gov.cn/wsite-frontend/#/platform/swxt')
browser.implicitly_wait(10)  

try:
    success_element = WebDriverWait(browser, 3000).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'item') and .//div[text()='浙企信用']]")
                                        )
        )

    # 记录当前窗口信息
    main_window_handle = browser.current_window_handle  # 当前主窗口句柄
    window_count = len(browser.window_handles) # 当前窗口数量

    time.sleep(5)  
    # 执行点击操作
    move_click(browser, success_element)

    #等待新标签页出现（最多等待15秒）
    WebDriverWait(browser, 30).until(
            lambda d: len(d.window_handles) > window_count
        )

    #获取所有窗口句柄并切换到新标签页
    window_handles = browser.window_handles
    print(browser.window_handles)

    new_window_handle = None

    # 查找新出现的窗口句柄
    for handle in window_handles:
        if handle != main_window_handle:
            new_window_handle = handle
            break

    if new_window_handle:
        try:
            browser.switch_to.window(new_window_handle)
            print(f"已切换到新标签页: {new_window_handle}")
            print(f"新页面标题: {browser.title}")
            print(f"新页面URL: {browser.current_url}")
        except NoSuchWindowException:
            print("错误：新标签页已关闭或不可访问")
            raise
    else:
        print("错误：未找到新窗口句柄")
        raise RuntimeError("未找到新窗口句柄")
    
    time.sleep(5) 
    browser.get('https://xyjg.zjamr.zj.gov.cn:8082/f1/dishonest-list/business-anomaly/inclusion-application')
    
    process_all_list(browser)

except Exception as e:
    print(f"等待登录成功时出错: {e}")
    print(e)

#重要提醒：1.在使用本脚本前，首先首先首先！！！编辑好名为“12306.json”的文件，否则无法运行！！json文件中名称的具体含义可见本程序35-37行代码
#        2.下载浏览器驱动，将驱动放在python.exe所在的根目录下
#（必看）  3.提前找到想乘坐的车次预定按钮css信息，填到187和195行代码！！！！
#        4.第一次使用需要扫码登录，之后会生成一个名为"12306cookies.pkl"的文件，之后短时间内购票就不需要再进行登录操作（①若需要重新登录，删掉此文件即可；②长时间未登录，也需要删掉此文件重新登陆）
#        5.52行进行定时设置，设置时间最好提前10秒
#        6.无选座功能
import time
import requests
from prettytable import PrettyTable
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.common import exceptions
import pickle
import os
import datetime
import sys
def stop():
    sys.exit()

def wait_until(target_time_str):
    """精确等待到指定时间"""
    target_time = datetime.datetime.strptime(target_time_str, '%Y-%m-%d %H:%M:%S')

    # 提前10秒开始准备
    prep_time = target_time - datetime.timedelta(seconds=10)

    # 等待到准备时间
    print("等待到准备时间...")
    while datetime.datetime.now() < prep_time:
        current = datetime.datetime.now()
        print(f'\r当前时间：{current.strftime("%Y-%m-%d %H:%M:%S")}', end="", flush=True)
        time.sleep(0.1)

    print("\n开始浏览器初始化...")
    # 初始化浏览器和其他准备工作

    # 精确等待到目标时间
    print("精确等待到抢票时间...")
    while datetime.datetime.now() < target_time:
        # 使用更短的时间间隔提高精度
        time.sleep(0.001)

    print("执行抢票操作！")


# 使用
dingshi = '2025-09-20 11:44:52'
wait_until(dingshi)

#加载乘客信息（请在json文件中设置好个人出行信息）
info_user=open('12306.json', encoding='utf-8').read()
user_data=json.loads(info_user)
FP=user_data['FP']#出发城市
TP=user_data['TP']#目的城市
DATE=user_data['DATE']#出发日期（XXXX-XX-XX）
while 1:
    # choice=2
    choice=int(input('查票请扣1，购票请扣2，退出请扣3：'))
    if choice==1 or choice==2:
        if choice==1:
            print('---------------------查票功能---------------------')
            #读取12306上对应的城市编号文件city.json
            f=open('city.json',encoding='utf-8').read()
            city_data=json.loads(f)
            #输入信息对应的12306标头网址
            url=f'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={DATE}&leftTicketDTO.from_station={city_data[FP]}&leftTicketDTO.to_station={city_data[TP]}&purpose_codes=ADULT'
            #输入对应的浏览器客户操作
            headers={
            'cookie':'_uab_collina=172974753653822536335524; JSESSIONID=107E2E807B6B2E47E570F6D92E176D74; tk=hys9TBdhbV_BubNoqLwmSIfZDCsMjL25eBf92K00Gchsyj_j-fi1Zwkow1w0; BIGipServerotn=1389953290.50210.0000; BIGipServerpassport=770179338.50215.0000; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; route=c5c62a339e7744272a54643b3be5bf64; _jc_save_fromStation=%u5A01%u6D77%u5317%2CWHK; _jc_save_toStation=%u5FB7%u5DDE%u4E1C%2CDIP; _jc_save_toDate=2024-10-24; _jc_save_wfdc_flag=dc; uKey=d6ace43cc44f77789975a7f82eea011eacefea10ee1c07b0cf02c44475ecccd2f3b0af07861ba353edec8de7b01b7550; _jc_save_fromDate=2024-10-29',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
            }
            #扒取信息
            response=requests.get(url=url,headers=headers)
            json_data=response.json()
            # print(json_data)
            tb=PrettyTable()
            tb.field_names=[
                '序号',
                '车次',
                '出发时间',
                '到达时间',
                '耗时',
                '特等座',
                '一等',
                '二等',
                '软卧',
                '硬卧',
                '硬座',
                '无座'
            ]
            page=0
            #扒取信息中的有用信息
            result=json_data['data']['result']
            for i in result:
                index=i.split('|')
                # page=0
                # for j in index:
                #     print(page,"***",j)
                #     page+=1
                # break
                num=index[3]#车次
                leave_time = index[8]  # 出发时间
                arrive_time = index[9]  # 到达时间
                cost_time = index[10]  # 耗时
                topGrade=index[32]#商务
                first_class = index[31]#一等座
                second_class = index[30]#二等座
                hard_sleeper = index[28]#硬卧
                hard_seat = index[29]#硬座
                no_seat = index[26]#无座
                soft_sleeper = index[23]#软卧
                # dict={
                #     '车次':num,
                #     '出发时间': leave_time,
                #     '到达时间': arrive_time,
                #     '耗时': cost_time,
                #     '特等座': topGrade,
                #     '一等': first_class,
                #     '二等': second_class,
                #     '软卧': soft_sleeper,
                #     '硬卧': hard_sleeper,
                #     '硬座': hard_seat,
                #     '无座': no_seat
                # }
                tb.add_row([
                page,
                num,
                leave_time,
                arrive_time,
                cost_time,
                topGrade,
                first_class,
                second_class,
                soft_sleeper,
                hard_sleeper,
                hard_seat,
                no_seat
                ])
                page+=1
            print(tb)

        if choice==2:
            print('---------------------购票功能---------------------')
            zhuye12306_url='https://www.12306.cn/index/index.html'
            target_url='https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc'

            class Log:
                def __init__(self):
                    self.status = 0
                    self.login_method = 1
                    # === 添加浏览器优化配置 ===
                    self.options = webdriver.ChromeOptions() #设置浏览器启动参数
                    self.options.add_experimental_option('detach', True) #保持浏览器窗口在结束之后不关闭
                    self.options.add_experimental_option('excludeSwitches', ['enable-automation']) #隐藏"Chrome正受到自动测试软件的控制"提示，降低被网站检测为自动化的风险
                    self.options.add_argument('--disable-blink-features=AutomationControlled')#禁用 Blink 引擎的自动化控制特征，进一步隐藏自动化痕迹，避免被反爬虫机制检测
                    self.options.add_argument('--no-sandbox')#禁用沙盒模式。提升性能但降低安全性
                    self.options.add_argument('--disable-dev-shm-usage')
                    self.options.add_argument('--disable-gpu')#禁用 GPU 硬件加速,避免GPU相关硬件错误.
                    self.options.add_argument('--disable-extensions')#禁用所有浏览器扩展插件,减少内存占用
                    self.options.add_argument('--disable-images')  # 禁用图片加载

                    # 网络请求优化 - 禁用图片和CSS
                    self.options.add_experimental_option("prefs", {
                        #"profile.default_content_setting_values.images": 2,  # 禁用图片
                        #"profile.managed_default_content_settings.stylesheets": 2,  # 禁用CSS
                        "profile.managed_default_content_settings.javascript": 1,  # 保持JS启用
                        "profile.managed_default_content_settings.flash": 2  # 禁用Flash
                    })

                    self.driver = webdriver.Chrome(options=self.options)

                def button(self):
                    try:
                        self.driver.find_element(By.ID, 'link_for_ticket')
                        return True
                    except exceptions.NoSuchElementException:
                        return False

                def set_cookies(self):
                    self.driver.get(zhuye12306_url)
                    self.driver.find_element(By.ID,'J-btn-login').click()
                    print('###请扫码登录###')
                    while not self.button():
                        time.sleep(1)
                    print('###扫码成功###')
                    pickle.dump(self.driver.get_cookies(), open('12306cookies.pkl', 'wb'))
                    print('cookie保存成功')
                    self.driver.get(target_url)

                def get_cookie(self):
                    cookies = pickle.load(open('12306cookies.pkl', 'rb'))
                    for cookie in cookies:
                        cookie_dict = {
                            'domain': '.12306.cn',
                            'name': cookie.get('name'),
                            'value': cookie.get('value')
                        }
                        self.driver.add_cookie(cookie_dict)
                    print('载入cookie')


                def login(self):
                    if self.login_method == 0:
                        self.driver.get(zhuye12306_url)
                        print('开始登录')
                    elif self.login_method == 1:
                        if not os.path.exists('12306cookies.pkl'):
                            self.set_cookies()
                        else:
                            self.driver.get(target_url)
                            self.get_cookie()

                @property
                def goupiao(self):
                    self.driver.maximize_window()

                    from_input = self.driver.find_element(By.ID, 'fromStationText')
                    from_input.click()
                    from_input.clear()
                    from_input.send_keys(Keys.CONTROL + "a")
                    from_input.send_keys(Keys.DELETE)
                    from_input.send_keys(FP)


                    from_input.send_keys(Keys.ENTER)  # 确认选择

                    to_input = self.driver.find_element(By.ID, 'toStationText')
                    to_input.click()
                    to_input.clear()
                    to_input.send_keys(Keys.CONTROL + "a")
                    to_input.send_keys(Keys.DELETE)
                    to_input.send_keys(TP)

                    time.sleep(0.1)  # 极短等待确保下拉列表出现
                    # 按下两次向下箭头选择"广州"（跳过"广州北"）
                    from_input.send_keys(Keys.ARROW_DOWN)  # 第一次：从"广州北"跳到下一个
                    from_input.send_keys(Keys.ARROW_DOWN)  # 第二次：确保选择到"广州"
                    to_input.send_keys(Keys.ENTER)



                    # 输入出发日期
                    self.driver.find_element(By.ID, 'train_date').click()
                    self.driver.find_element(By.ID, 'train_date').clear()
                    self.driver.find_element(By.ID, 'train_date').send_keys(DATE)
                    self.driver.find_element(By.ID, 'train_date').send_keys(Keys.ENTER)


                    def click_query_button():
                        # 先点击一次查询按钮 - 使用更可靠的定位方式
                        try:
                            query_button = WebDriverWait(self.driver, 1).until(
                                EC.element_to_be_clickable((By.ID, 'query_ticket'))
                            )
                            self.driver.execute_script("arguments[0].click();", query_button)
                            time.sleep(0.1)
                        except Exception as e:
                            print(f"点击查询按钮失败: {str(e)}")
                            # 备用方案：尝试通过CSS选择器定位
                            try:
                                query_button = WebDriverWait(self.driver, 0.5).until(
                                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a#query_ticket.btn92s'))
                                )
                                self.driver.execute_script("arguments[0].click();", query_button)
                                time.sleep(0.1)
                            except Exception as e2:
                                print(f"备用方案也失败: {str(e2)}")
                                return False

                    # 等待查询结果加载
                    try:
                        WebDriverWait(self.driver, 3).until(
                            EC.presence_of_element_located((By.ID, 'queryLeftTable'))
                        )
                        print("查询结果已加载")
                    except TimeoutException:
                        print("查询结果加载超时")
                        return False

                    target_train = "G8476"
                    max_retries = 200
                    retry_count = 0.1
                    found_target = False

                    while retry_count < max_retries and not found_target:
                        try:
                            # 点击五华筛选 - 直接通过ID定位（改为出发站）
                            from_station_filter = WebDriverWait(self.driver, 0.5).until(
                                EC.element_to_be_clickable((By.ID, 'cc_from_station_五华'))
                            )
                            self.driver.execute_script("arguments[0].click();", from_station_filter)
                            time.sleep(0.2)

                            # 点击广州筛选 - 直接通过ID定位（改为到达站）
                            to_station_filter = WebDriverWait(self.driver, 0.5).until(
                                EC.element_to_be_clickable((By.ID, 'cc_to_station_广州'))
                            )
                            self.driver.execute_script("arguments[0].click();", to_station_filter)
                            time.sleep(0.2)

                            # 再次点击查询按钮应用筛选
                            self.driver.find_element(By.ID, 'query_ticket').click()
                            time.sleep(0.01)

                            # 查找G8476车次 分清精准匹配和模糊匹配异常重要!!!
                            train_xpath = f"//tr[contains(@id, 'ticket_') and contains(@id, '{target_train}')]//a[contains(text(), '{target_train}')]"
                            train_element = WebDriverWait(self.driver, 0.5).until(
                                EC.presence_of_element_located((By.XPATH, train_xpath))
                            )

                            # 验证车次信息
                            row = train_element.find_element(By.XPATH, "./ancestor::tr[1]")
                            station_info = row.find_element(By.CLASS_NAME, "cdz").text

                            if "广州" in station_info and "五华" in station_info:
                                print(f"找到目标车次: {target_train}, 区间: {station_info}")
                                found_target = True

                                # ⚡ 直接点击该车次行的预订按钮
                                try:
                                    # 使用更精确的定位和更短的等待时间
                                    book_btn = WebDriverWait(row, 0.5).until(
                                        EC.element_to_be_clickable(
                                            (By.XPATH, ".//a[contains(@class,'btn72') and contains(text(),'预订')]"))
                                    )
                                    # 立即点击，不要等待
                                    self.driver.execute_script("arguments[0].click();", book_btn)
                                    print("预订按钮点击成功")
                                    book_btn_found = True

                                except Exception as e:
                                    print(f"直接点击预订按钮失败: {str(e)}")
                                    #  fallback to original method
                                    start_time = time.time()
                                    timeout = 20  # 最多等待20秒
                                    book_btn_found = False

                                    while time.time() - start_time < timeout and not book_btn_found:
                                        try:
                                            # 先点击查询按钮刷新
                                            self.driver.find_element(By.ID, 'query_ticket').click()
                                            time.sleep(0.04)

                                            # 尝试查找预订按钮
                                            book_btn = WebDriverWait(self.driver, 0.3).until(
                                                EC.element_to_be_clickable((By.CLASS_NAME, "btn72"))
                                            )
                                            book_btn.click()
                                            print("预订按钮点击成功")
                                            book_btn_found = True
                                            break

                                        except Exception as e:
                                            # 预订按钮还没出现，继续循环
                                            print(f"刷新查询，等待预订按钮...")
                                            time.sleep(0.12)  # 稍微等待一下再继续

                        except Exception as e:
                            print(f"尝试 {retry_count + 1} 失败: {str(e)}")
                            retry_count += 1
                            # 每次重试前重新点击查询按钮
                            self.driver.find_element(By.ID, 'query_ticket').click()
                            time.sleep(0.1)

                    if not found_target:
                        print("达到最大重试次数，未能找到广州→五华的G8476车次")
                        return False

                    # ⚡ 极速锁单操作
                    try:
                        # 等待页面跳转到乘车人选择页面
                        WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.ID, 'normalPassenger_0'))
                        )

                        # 选择乘车人
                        self.driver.execute_script("document.getElementById('normalPassenger_0').click();")
                        time.sleep(0.03)

                        print("乘车人选择完成，准备提交订单（锁单）")

                        # 减少等待时间，使用更激进的策略
                        submit_btn = WebDriverWait(self.driver, 2).until(
                            EC.presence_of_element_located((By.ID, 'submitOrder_id'))
                        )
                        # 直接JavaScript点击，避免UI阻塞
                        self.driver.execute_script("document.getElementById('submitOrder_id').click();")
                        # 确保按钮在视图中
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                            submit_btn
                        )


                        # 使用JavaScript点击避免元素拦截
                        self.driver.execute_script("arguments[0].click();", submit_btn)

                        print("✅ 订单提交成功")

                        # ⚡ 极速锁单操作
                        try:
                            # 提交订单
                            submit_btn = WebDriverWait(self.driver, 1).until(
                                EC.presence_of_element_located((By.ID, 'submitOrder_id'))
                            )
                            self.driver.execute_script("arguments[0].click();", submit_btn)
                            print("✅ 订单提交成功")

                            time.sleep(0.03)

                            # 第一步：尝试关闭警告对话框（直接内联实现）
                            try:
                                warning_btn = WebDriverWait(self.driver, 0.3).until(
                                    EC.presence_of_element_located((By.ID, 'qd_closeDefaultWarningWindowDialog_id'))
                                )

                                # 执行警告按钮的javascript代码
                                self.driver.execute_script("""
                                    var btn = document.getElementById('qd_closeDefaultWarningWindowDialog_id');
                                    if (btn && btn.href) {
                                        var jsCode = btn.href.replace('javascript:', '').trim();
                                        if (jsCode) {
                                            eval(jsCode);
                                        } else {
                                            btn.click();
                                        }
                                    }
                                """)

                                print("✅ 警告对话框已关闭")
                                time.sleep(0.08)  # 等待对话框关闭

                            except Exception as e:
                                # 没有警告对话框是正常情况
                                pass

                            # 第二步：点击最终确认按钮
                            try:
                                confirm_btn = WebDriverWait(self.driver, 1).until(
                                    EC.element_to_be_clickable((By.ID, 'qr_submit_id'))
                                )

                                # 极速点击组合
                                self.driver.execute_script("arguments[0].click();", confirm_btn)
                                confirm_btn.click()

                                # 额外保障：直接DOM操作
                                self.driver.execute_script("document.getElementById('qr_submit_id').click();")

                                print("✅ 最终确认完成")
                                return True

                            except Exception as e:
                                print(f"❌ 最终确认失败: {str(e)}")
                                return False

                        except Exception as e:
                            return False

                    except Exception as e:
                        print(f"❌ 提交订单失败: {str(e)}")
                        return False
                def enter_ticket(self):
                    print('打开浏览器，进入12306官网')
                    self.login()
                    self.driver.refresh()
                    self.status = 2
                    print('登录成功，开始购票')
                    self.goupiao


            train = Log()
            train.enter_ticket()
            break
    if choice == 3:
        print('已退出')
        break


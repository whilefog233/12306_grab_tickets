# 极速输入站点信息（精准选择广州）
""""""

                    from_input = self.driver.find_element(By.ID, 'fromStationText')
                    from_input.click()
                    from_input.clear()
                    from_input.send_keys(Keys.CONTROL + "a")
                    from_input.send_keys(Keys.DELETE)
                    from_input.send_keys(FP)
                    time.sleep(0.1)  # 极短等待确保下拉列表出现

                    # 按下两次向下箭头选择"广州"（跳过"广州北"）
                    from_input.send_keys(Keys.ARROW_DOWN)  # 第一次：从"广州北"跳到下一个
                    from_input.send_keys(Keys.ARROW_DOWN)  # 第二次：确保选择到"广州"
                    from_input.send_keys(Keys.ENTER)  # 确认选择

                    to_input = self.driver.find_element(By.ID, 'toStationText')
                    to_input.click()
                    to_input.clear()
                    to_input.send_keys(Keys.CONTROL + "a")
                    to_input.send_keys(Keys.DELETE)
                    to_input.send_keys(TP)
                    to_input.send_keys(Keys.ENTER)
                    # 输入出发日期
                    self.driver.find_element(By.ID, 'train_date').click()
                    self.driver.find_element(By.ID, 'train_date').clear()
                    self.driver.find_element(By.ID, 'train_date').send_keys(DATE)
                    self.driver.find_element(By.ID, 'train_date').send_keys(Keys.ENTER)
""""""

try:
    # 等待页面跳转到乘车人选择页面
    WebDriverWait(self.driver, 5).until(
        EC.url_contains("confirmPassenger")
    )
    time.sleep(0.1)

    # 尝试多次选择乘车人
    for attempt in range(3):  # 尝试3次
        try:
            passenger_checkbox = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.ID, 'normalPassenger_0'))
            )
            self.driver.execute_script("arguments[0].click();", passenger_checkbox)
            time.sleep(0.1)

            # 验证是否选中
            if passenger_checkbox.is_selected():
                print("乘车人选择成功")
                break
            else:
                print(f"第{attempt + 1}次选择失败，重试...")

        except Exception as e:
            print(f"第{attempt + 1}次尝试失败: {str(e)}")
            if attempt == 2:  # 最后一次尝试失败则抛出异常
                raise e



# 修改这里：持续点击查询直到预订按钮出现
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
                                        time.sleep(0.5)  # 稍微等待一下再继续

            # 点击广州东筛选 - 直接通过ID定位
        from_station_filter = WebDriverWait(self.driver, 0.5).until(
            EC.element_to_be_clickable((By.ID, 'cc_from_station_广州'))
        )
        self.driver.execute_script("arguments[0].click();", from_station_filter)
        time.sleep(0.2)

        # 点击五华筛选 - 直接通过ID定位
        to_station_filter = WebDriverWait(self.driver, 0.5).until(
            EC.element_to_be_clickable((By.ID, 'cc_to_station_五华'))
        )
        self.driver.execute_script("arguments[0].click();", to_station_filter)
        time.sleep(0.2)

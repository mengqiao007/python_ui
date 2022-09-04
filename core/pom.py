from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    #定义属性，>元素


    def __init__(self,driver:WebDriver):
        self.driver = driver
        #显示等待
        self.wait = WebDriverWait(driver,10)

        #检查元素，获取属性定位到元素，设置成属性
        self.check_element()

    def check_element(self):
        """
        把属性中的字符串变成元素
        检查是否有元素丢失
        :return:
        """
        for attr in dir(self):
            #判断是否是元素属性
            if attr.startswith("ele_"):
                #获取属性
                loc = getattr(self,attr)
                #定位到元素
                el =self.find_element(By.XPATH,loc)
                #设置属性
                setattr(self,attr,el)

    def find_element(self,*args):
        """
        封装元素定位方法，自动使用显示等待
        """
        el = self.wait.until(lambda  _:self.driver.find_element(*args))
        return el


    def input(self,ele:WebElement,content=None):
        """
        封装input方法
        """
        #等待元素出现
        self.wait.until(lambda _:ele.is_enabled())
        ele.clear()
        #输入内容
        if content is not None:
            ele.send_keys(content)


    def click(self,ele:WebElement):
        """
        封装点击方法
        :return:
        """
        self.wait.until(lambda _: ele.is_enabled())
        ele.click()

    def get_message(self):
        message = self.find_element(By.XPATH,'//span[@class="right-header--text-username--cblIQLq"]').text
        return message

class LoginPage(BasePage):
    ele_input_account = '//*[@id="account"]'
    ele_input_password = '//*[@id="password"]'
    ele_button_submit = '//*[@id="ice-container"]/div/form/button'

    def login(self,username,password):
        self.input(self.ele_input_account,username)
        self.input(self.ele_input_password,password)
        self.click(self.ele_button_submit)



from core import pom
def test_login(driver):
    driver.get('https://mp-console-dev.ab-inbev.cn/login')
    page = pom.LoginPage(driver)

    page.login('78170019','Z7b!0lc!Tn')

    message = page.get_message()

    assert message == '78170019'


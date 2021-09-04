

class Paths():
    def __init__(self):
        tmp = None

        # GENERAL # 

        self.error_loop = "Error in loop_body: {}"


        # BEST BUY #

        self.BEST_BUY_PDP_URL = "https://api.bestbuy.com/click/5592e2b895800000/{sku}/pdp"
        self.BEST_BUY_CART_URL = "https://api.bestbuy.com/click/5592e2b895800000/{sku}/cart"
        self.BEST_BUY_PDP_URL = "https://api.bestbuy.com/click/5592e2b895800000/{sku}/pdp"
        self.BEST_BUY_CART_URL = "https://api.bestbuy.com/click/5592e2b895800000/{sku}/cart"
        self.BEST_BUY_ADD_TO_CART_API_URL = "https://www.bestbuy.com/cart/api/v1/addToCart"
        self.BEST_BUY_CHECKOUT_URL = "https://www.bestbuy.com/checkout/c/orders/{order_id}/"
        self.DEFAULT_HEADERS = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
            "origin": "https://www.bestbuy.com",
        }
        self.signin  = "https://www.bestbuy.com/identity/global/signin"
        self.submit_login = "/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div[4]/button"
        self.pw_field = '//*[@id="fld-p1"]'
        self.select_country = '/html/body/div[2]/div/div/div/div[1]/div[2]/a[2]'
        self.close_deals_popup = "//*[@id=\"widgets-view-email-modal-mount\"]/div/div/div[1]/div/div/div/div/button"


        # NEWEGG #

        self.nav_title = 'nav-complex-title'
        self.ne_dropdown = "//*[@value='96']/option[text()='96']"
        self.signin_button = "//*[contains(text(), 'Sign in / Register')]"
        self.close_popup = "popup-close"
        self.sign_email = "labeled-input-signEmail"
        self.input_pw = "labeled-input-password"
        self.human = """//*[contains(text(), 'Are you a human?')]"""
        self.captcha = "/html/body/div[1]/div[2]/p[5]/a"
        self.two_factor = """//*[@id="app"]/div/div[2]/div[2]/div/div/div[3]/form/div/div[3]/div/input[1]"""
        self.tfa_value = """//*[@id="app"]/div/div[2]/div[2]/div/div/div[3]/form/div/div[3]/div/input[6]"""

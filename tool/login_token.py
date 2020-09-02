import re
import urllib

import requests

from common import read_config

rd = read_config.ReadConfig( )

class TokenApp:
    def __init__(self, tenantcode, environment, username, password):
        self.tenantcode = tenantcode
        self.environment = environment
        self.userName = username
        self.password = password
        self.url_name_option = self.environment + "_" + self.tenantcode + "_" + "url"


    def get_token(self):
        url_info = rd.read_url_config(self.url_name_option)
        inner_login_url = url_info.get('inner_login_url')
        host = url_info.get('host')
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Host":"{host}".format(host=host),
            "Connection": "keep-alive",
        }
        data ={
            "tenantCode": "{tenantcode}".format(tenantcode=self.tenantcode),
            "userName" : "{userName}".format(userName=self.userName),
            "password" : "{password}".format(password=self.password),
            "code" : "",
        }
        url = "{url}".format(url=inner_login_url)
        session = requests.session()
        req = session.post(url=url, data=data, headers=header, allow_redirects=False, verify=False)
        print(req)
        if req.status_code == 302:
            flag = 'success'
            token = req.headers["location"]
            p = re.compile(r'sid=(.*?)&')
            token = re.search(p, token).group(1)
        else:
            flag = 'fail'
            token = ''
        result = [flag, token]
        # print(result)
        return result

    def login_app_url(self):
        result = self.get_token()
        if result[0] == "success":
            flag = "success"
            token = result[1]
            url_info = rd.read_url_config(self.url_name_option)
            url = '{app_url}?sid={token}&o={tenantcode}'\
                .format(app_url=url_info.get('app_url'), token=token, tenantcode=self.tenantcode)
        elif result[0] ==  'fail':
            flag =  'fail'
            url = ''
        result = [flag, url]
        print(result)
        return result


if __name__ == "__main__":
    s = TokenApp("yuexiu", "beta", "sytest", "cz@123456")
    s.login_app_url()


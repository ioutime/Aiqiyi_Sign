'''
@FILE    :   action.py
@DSEC    :   爱奇艺会员打卡
@AUTHOR  :   ioutime
@DATE    :   2021/07/11  00:56:17
@VERSION :   1.0
'''
import requests
import argparse
import execjs

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("phone", help="Your Phone Number.")
    parser.add_argument("password", help="The plaint text or MD5 value of the password.")
    args = parser.parse_args()

    return {
        "phone": args.phone,
        "password": args.password,
    }

#加密密码    
def encry(password):
    with open('encryption.js', encoding='utf-8') as f:
        aiqiyi = f.read()
    js = execjs.compile(aiqiyi)
    password = js.call('rsaFun', password)
    return password

#login
def login(infos,phone,password):
        url = 'https://passport.iqiyi.com/apis/reglogin/login.action'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',

            'Connection': 'keep-alive',

            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'

        }
        formData ={
            'email': phone,
            'fromSDK': '1',
            'sdk_version': '1.0.0',
            'passwd': password,
            'agenttype': '1',
            '__NEW': '1',
            'checkExist': '1',
            'lang': '',
            'ptid': '01010021010000000000',
            'nr': '2',
            'verifyPhone':'1',
            'area_code': '86',
            'dfp': 'a108aecd4300a148ee94184b13e3289476ec969d7ab9536cc924fc76966f26f788',
        }
        try:
            r = requests.Session()
            res = r.post(url,headers=headers,data=formData)      
            if res.status_code == 200:
                html = res.json()
                msg = html.get('msg')
                if(msg == '帐号或密码错误'):
                    print(msg)
                    return
                data = html.get('data')
                nickname = data.get('nickname')
                print('='*40)
                print(nickname+'----->登录成功')
                #获取cookie值,转成字典格式
                cookies_dict = requests.utils.dict_from_cookiejar(r.cookies)
                #签到
                #退出
                logout(nickname,cookies_dict)
            else:
                print('登录失败')
                return
        except:
            print('false')

#logout
def logout(nickname,cookies):
        logout_url = 'https://passport.iqiyi.com/apis/user/logout.action'
        logout_headers = {
            'Accept': '*/*',

            'Connection': 'keep-alive',

            # 'Cookie': cookies,

            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
        }
        logout_fromdata = {
            'agenttype': '1',
            'fromSDK': '1',
            'noredirect': '1',
            'ptid': '01010021010000000000',
            'sdk_version': '1.0.0',
        }
        res = requests.post(url=logout_url,headers=logout_headers,cookies = cookies,data=logout_fromdata)
        if res.status_code == 200:
            print(nickname+'----->注销成功!')
            print('='*40)
        else:
            print('注销失败')


def main(infos):
    phone = infos["phone"]
    password = infos["password"]
    # Run tasks
    if not password:
        return
    else:
        login(infos,phone,encry(password))

if __name__=="__main__":
    main(get_args())


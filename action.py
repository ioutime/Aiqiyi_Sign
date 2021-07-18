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
import re
from http import cookiejar

# 创建一个session,作用会自动保存cookie
Session = requests.session()

#推送信息
def push_info(infos,msg):
    token = infos["token"]
    if not token:
        return
    else: 
        url = "http://www.pushplus.plus/send?token="+token+"&title=爱奇艺打卡&content="+msg+"&template=html"
        try:
            requests.get(url=url)
        except Exception as e:
            print('推送失败')
            print(e)
#参数
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("phone", help="Your Phone Number.")
    parser.add_argument("password", help="The plaint text or MD5 value of the password.")
    parser.add_argument("-t", dest="token", help="pushplus的token值")
    args = parser.parse_args()

    return {
        "phone": args.phone,
        "password": args.password,
        "token" : args.token
    }

#加密密码    
def encry(password):
    with open('encryption.txt', encoding='utf-8') as f:
        aiqiyi = f.read()
    js = execjs.compile(aiqiyi)
    password = js.call('rsaFun', password)
    return password

#login
def login(infos,phone,password):
        url = 'https://passport.iqiyi.com/apis/reglogin/login.action'
        headers = {
            
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70'

        }
        formData ={
            'email': phone,
            'fromSDK': '1',
            'passwd': password,
            'agenttype': '1',
            '__NEW': '1',
            'checkExist': '1',
            'lang': '',
            'ptid': '01010021010000000000',
            'nr': '2',
            'verifyPhone':'1',
            'area_code': '86',
            'dfp': 'a0dd3024dbad184f509b5c7fc18110921d4bf7f60ebbc462dd8b5e2d17f7b9281d',
        }
        res = Session.post(url,headers=headers,data=formData)      
        if res.status_code == 200:
            html = res.json()
            msg = html.get('msg')
            if(msg == '帐号或密码错误'):
                print(msg)
                push_info(infos,msg)
                return
            if(msg == '安全校验不通过'):
                print(msg)
                msg = msg + "\n可能是运行次数太多了，也可能是dfp变化了"
                push_info(infos,msg)
                return
            data = html.get('data')
            nickname = data.get('nickname')
            print('='*40)
            print(nickname+'----->登录成功')
            #获取cookie值,转成字典格式
            cookies_dict = requests.utils.dict_from_cookiejar(Session.cookies)
            #签到
            msg0  = member_sign(cookies_dict)
            #获取用户信息
            msg1 = get_info(cookies_dict)
            #输出信息
            msg = msg0 + msg1
            print(msg)
            #退出
            logout(nickname,cookies_dict)
            #推送消息
            push_info(infos,msg)
        else:
            print('登录失败')
            push_info(infos,'登录失败')
            return

#logout
def logout(nickname,cookies):
        logout_url = 'https://passport.iqiyi.com/apis/user/logout.action'
        logout_headers = {
            'Accept': '*/*',

            'Connection': 'keep-alive',

            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70',
        }
        logout_fromdata = {
            'agenttype': '1',
            'fromSDK': '1',
            'noredirect': '1',
            'ptid': '01010021010000000000',
            'sdk_version': '1.0.0',
        }
        res = requests.post(url=logout_url,headers=logout_headers,data=logout_fromdata)#cookies = cookies,
        if res.status_code == 200:
            print(nickname+'----->注销成功!')
            print('='*40)
        else:
            print('注销失败')

#sign
def member_sign(cookies_dict):
    P00001 = cookies_dict.get('P00001')
    login = Session.get('https://static.iqiyi.com/js/qiyiV2/20201023105821/common/common.js').text
    regex1=re.compile("platform:\"(.*?)\"")
    platform=regex1.findall(login)
    url='https://tc.vip.iqiyi.com/taskCenter/task/userSign?P00001='+P00001+'&platform='+platform[0] + '&lang=zh_CN&app_lm=cn&deviceID=pcw-pc&version=v2'
    try:
        sign=Session.get(url)
        strr = sign.json()
        try:
            sign_msg = strr.get('msg')
        except:
            print('未签')
        str2 = strr.get('data')
        continueSignDaysSum = str2.get('continueSignDaysSum')
        rewardDay = 7 if continueSignDaysSum%28<=7 else (14 if continueSignDaysSum%28<=14 else 28)
        rouund_day = 28 if continueSignDaysSum%28 == 0 else continueSignDaysSum%28
        growth = str2.get('acquireGiftList')[0]
        msg = f"{sign_msg}\n{growth}\n连续签到：{continueSignDaysSum}天\n签到周期：{rouund_day}天/{rewardDay}天\n"
        # print(msg)
    except Exception as e:
        msg = e
        # print(e)
    return msg

#获取用户信息
def get_info(cookies_dict):
    P00001 = cookies_dict.get('P00001')
    url = 'http://serv.vip.iqiyi.com/vipgrowth/query.action'
    params = {
        "P00001": P00001,
        }
    res = Session.get(url, params=params)
    if res.json()["code"] == "A00000":
        try:
            res_data = res.json()["data"]
            #VIP等级
            level = res_data["level"]
            #升级需要成长值
            distance = res_data["distance"]
            #VIP到期时间
            deadline = res_data["deadline"]
            msg = f"VIP等级：{level}\n升级需成长值：{distance}\nVIP到期时间:{deadline}"
            # print(msg)
        except:
            msg = res.json()
    else:
        msg = res.json()
        # print(msg)
    return msg

#主函数
def main(infos):
    '''
    爱奇艺会员打卡,实现手机号登录自动获取cookie
    '''
    phone = infos["phone"]
    password = infos["password"]
    # Run tasks
    if not password:
        return
    else:
        login(infos,phone,encry(password))

if __name__=="__main__":
    main(get_args())


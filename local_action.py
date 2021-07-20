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

cookie = '''cookie值'''

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
    parser.add_argument("-t", dest="token", help="pushplus的token值")
    args = parser.parse_args()

    return {
        "token" : args.token,
    }



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
    res = requests.get(url, params=params)
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
        print(msg)
    return msg

#转换获取的COOKIE
def transform(infos):
    cookies = cookie.replace(' ','')
    dct = {}
    lst = cookies.split(';')
    for i in lst:
        name = i.split('=')[0]
        value = i.split('=')[1]
        dct[name] = value
    #签到
    msg0  = member_sign(dct)
    #获取用户信息
    # msg1 = get_info(dct)
    # #输出信息
    # msg = msg0 + msg1
    print(msg0)
    #推送消息
    push_info(infos,msg0)
    return

#主函数
def main(infos):
    '''
    爱奇艺会员打卡,本地代码执行
    '''
    transform(infos)

if __name__=="__main__":
    main(get_args())


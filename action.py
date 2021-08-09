'''
@FILE    :   action.py
@DSEC    :   爱奇艺会员打卡
@AUTHOR  :   ioutime
@DATE    :   2021/07/11  00:56:17
@VERSION :   1.1
'''
import requests
import argparse
import execjs
import re
from http import cookiejar
from urllib.parse import unquote
import json

# 创建一个session,作用会自动保存cookie
Session = requests.session()

#主函数
def main(infos):
    '''
    爱奇艺会员打卡,实现手机号登录自动获取cookie或手动获取（建议手动获取）
    '''
    phone = infos["phone"]
    password = infos["password"]
    cookie = infos["cookie"]
    p00001 = infos["p00001"]
    # Run tasks
    if not cookie:
        if not p00001:
            print("需要在secrets中添加cookie")
            push_info(infos,"需要在secrets中添加cookie")
            return
        else:
            p00001s = p00001.split(',')
            more_accounts(infos,p00001s)
            return
    elif cookie and p00001:
        p00001s = p00001.split(',')
        more_accounts(infos,p00001s)
        return                  
    elif not password or not phone:
        transform(infos,cookie)
    else:
        login(infos,phone,encry(password),cookie)

def more_accounts(infos,p00001):
    '''
    多账号签到
    '''
    ans = ''
    for i in p00001:
        ans = ans + "第%s账号：" % (p00001.index(i) + 1)
        print ("第%s账号：" % (p00001.index(i) + 1))
        if len(i) >= 20:
            dct = {}
            dct['P00001']=i
            #签到
            msg  = member_sign(dct)
            if msg != "输入的cookie有问题(P00001)，请重新获取" and msg!='出错了，无法获取platform' and msg!='未签到成功,可能是程序问题,也可能你不是爱奇艺会员':
                ans = ans + '   签到成功\n'
            else:
                ans = ans + '   FALSE\n'
            print(msg)
        else:
            msg = ' p00001不完整'
            ans = ans + '   p00001不完整\n'
            print(msg)
        print('='*40)
    # print(ans)
    #推送
    if len(ans) <= 300:
        push_info(infos,ans)
    else:
        push_info(infos,ans[0:200]+'......')
    

def push_info(infos,msg):
    '''
    推送信息
    '''
    token = infos["token"]
    if not token:
        return
    else: 
        try:
            url = "http://www.pushplus.plus/send?token="+token+"&title=爱奇艺打卡&content="+msg+"&template=html"
            html = requests.get(url=url)
            if html.status_code == 200:
                pass
            else:
                print('推送失败')
        except Exception as e:
            print('推送失败')
            print(e)


def get_args():
    '''
    参数获取
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", dest="phone", help="Your Phone Number.")
    parser.add_argument("-w", dest="password",help="The plaint text value of the password.")
    parser.add_argument("-t", dest="token", help="pushplus的token值")
    parser.add_argument("-c", dest="cookie", help="cookie值")
    parser.add_argument("-s", dest="p00001", help="P00001值")
    args = parser.parse_args()

    return {
        "phone": args.phone,
        "password": args.password,
        "token" : args.token,
        "cookie" : args.cookie,
        "p00001" : args.p00001
    }
 
def encry(password):
    '''
    加密密码 
    '''
    try:
        with open('encryption.txt', encoding='utf-8') as f:
            aiqiyi = f.read()
        js = execjs.compile(aiqiyi)
        password = js.call('rsaFun', password)
        return password
    except:
        print("密码加密失败")

def login(infos,phone,password,cookie):
    '''
    登录
    '''
    url = 'https://passport.iqiyi.com/apis/reglogin/login.action'
    headers = {   
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }
    formData ={
        'email': phone,'fromSDK': '1',
        'passwd': password,'agenttype': '1',
        '__NEW': '1','checkExist': '1',
        'lang': '','ptid': '01010021010000000000',
        'nr': '2','verifyPhone':'1',
        'area_code': '86','dfp': 'a0dd3024dbad184f509b5c7fc18110921d4bf7f60ebbc462dd8b5e2d17f7b9281d',
    }
    res = Session.post(url,headers=headers,data=formData)      
    if res.status_code == 200:
        html = res.json()
        msg = html.get('msg')
        if(msg == '帐号或密码错误'):
            print("帐号或密码错误,使用cookie签到")
            transform(infos,cookie)
            return
        if(msg == '安全校验不通过'):
            msg = "触发了安全验证，或者设备锁未关"
            print(msg+"\n安全校验不通过,使用cookie签到")
            transform(infos,cookie)
            return
        data = html.get('data')
        try:
            nickname = data.get('nickname')
        except:
            msg = msg + "登录失败－nickname"
            print(msg+"\n使用cookie签到")
            transform(infos,cookie)
            return  
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
        print('登录失败－code')
        print("使用cookie签到")
        transform(infos,cookie)
        return

def member_sign(cookies_dict):
    '''
    签到
    '''
    P00001 = cookies_dict.get('P00001')
    if P00001 == None:
        msg = "输入的cookie有问题(P00001)，请重新获取"
        print(msg)
        return msg 
    login = Session.get('https://static.iqiyi.com/js/qiyiV2/20201023105821/common/common.js').text
    regex1=re.compile("platform:\"(.*?)\"")
    platform=regex1.findall(login)
    if len(platform) == 0:
        msg = "出错了，无法获取platform"
        return msg
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
    except Exception as e:
        print(e)
        msg = "未签到成功,可能是程序问题,也可能你不是爱奇艺会员"
    return msg


def get_info(cookies_dict):
    '''
    获取用户信息
    '''
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
        except:
            print("获取具体信息失败")
            msg = ""
    else:
        print("获取个人信息失败")
        msg = ""
    return msg

def logout(nickname,cookies):
    '''
    退出登录
    '''
    logout_url = 'https://passport.iqiyi.com/apis/user/logout.action'
    logout_headers = {
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    }
    logout_fromdata = {
        'agenttype': '1','fromSDK': '1',
        'noredirect': '1','ptid': '01010021010000000000',
        'sdk_version': '1.0.0',
    }
    res = Session.post(url=logout_url,headers=logout_headers,data=logout_fromdata)
    if res.status_code == 200:
        print(nickname+'----->注销成功!')
        print('='*40)
    else:
        print('注销失败')

def transform(infos,cookie):
    '''
    转换完整的COOKIE，并执行签到等功能
    '''
    try:
        cookies = cookie.replace(' ','')
        dct = {}
        lst = cookies.split(';')
        for i in lst:
            name = i.split('=')[0]
            value = i.split('=')[1]
            dct[name] = value
    except:
        msg0 = "输入的cookie有问题，请重新获取"
        print(msg0)
        push_info(infos,msg0)
        return
    #判断是否有要的值
    P00001 = dct.get('P00001')
    if P00001 == None:
        msg0 = "输入的cookie有问题(P00001)，请重新获取"
        print(msg0)
        push_info(infos,msg0)
        return
    #获取nickname
    nickname = ''
    try:
        text = dct.get('P00002')
        text = unquote(text, 'utf-8').encode('utf-8').decode('unicode_escape')
        text = json.loads(text)
        nickname = text.get('nickname') + ': '
        #判断是否是会员
        text2 = dct.get('QC179')
        text2 = unquote(text2, 'utf-8').encode('utf-8').decode('unicode_escape')
        text2 = json.loads(text2)
        vipTypes = text2.get('vipTypes')
        if vipTypes == '' or vipTypes == ' ':
            nickname = nickname +'不是会员'
            print(nickname)
            push_info(infos,nickname)
            return
    except Exception as e:
        print(e)
        nickname = ''
    #签到
    msg0  = nickname + member_sign(dct)
    #用户信息
    msg = msg0 + get_info(dct)
    print(msg)
    push_info(infos,msg)
    return


if __name__=="__main__":
    try:
        main(get_args())
    finally:
        Session.close()
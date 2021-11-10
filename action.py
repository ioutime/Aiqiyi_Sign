'''
@FILE    :   action.py
@DSEC    :   爱奇艺会员打卡
@AUTHOR  :   ioutime
@DATE    :   2021/07/11  00:56:17
@VERSION :   1.2
'''
import requests
import argparse
from http import cookiejar
from urllib.parse import unquote
import json
import datetime
import calendar

# 创建一个session,作用会自动保存cookie
Session = requests.session()

#主函数
def main(infos):
    '''
    爱奇艺会员打卡,实现cookie签到
    '''
    cookie = infos["cookie"]
    p00001 = infos["p00001"]
    # Run tasks
    if not cookie:
        if not p00001:
            print("需要cookie")
            push_info(infos,"需要cookie")
            return
        else:
            p00001s = p00001.split(',')
            more_accounts(infos,p00001s)
            return
    elif cookie and p00001:
        p00001s = p00001.split(',')
        more_accounts(infos,p00001s)
        return
    else :
        transform(infos,cookie)

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
            if msg != "输入的cookie有问题(P00001)，请重新获取" and msg!='签到失败\n'and msg!='签到失败1\n'and msg!='签到失败2\n':
                ans = ans + '   签到成功\n'
            else:
                ans = ans + '   FALSE\n'
            print(msg)
        else:
            msg = ' p00001不完整'
            ans = ans + '   p00001不完整\n'
            print(msg)
        print('='*40)
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
            url = "http://www.pushplus.plus/send?token="+token+"&title=爱奇艺签到&content="+msg+"&template=html"
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
    parser.add_argument("-t", dest="token", help="pushplus的token值")
    parser.add_argument("-c", dest="cookie", help="cookie值")
    parser.add_argument("-s", dest="p00001", help="P00001值")
    args = parser.parse_args()

    return {
        "token" : args.token,
        "cookie" : args.cookie,
        "p00001" : args.p00001
    }

def member_sign(cookies_dict):
    '''
    签到
    '''
    P00001 = cookies_dict.get('P00001')
    if P00001 == None:
        msg = "输入的cookie有问题(P00001)，请重新获取"
        print(msg)
        return msg 
    url = "https://tc.vip.iqiyi.com/taskCenter/task/queryUserTask"
    params = {
        "P00001": P00001,
        "autoSign": "yes"
    }
    try:
        res = requests.get(url, params=params)
        if res.json()["code"] == "A00000":
            try:
                growth = res.json()["data"]["signInfo"]["data"]["rewardMap"]["growth"]
                continueSignDaysSum = res.json()["data"]["signInfo"]["data"]["cumulateSignDaysSum"]
                today = datetime.datetime.today()
                monthDay = calendar.monthrange(today.year,today.month)[1]
                rewardDay = 7 if continueSignDaysSum % monthDay <= 7 else (
                    14 if continueSignDaysSum % monthDay <= 14 else monthDay)
                rouund_day = monthDay if continueSignDaysSum % monthDay == 0 else continueSignDaysSum % monthDay
                msg = f"成长值+{growth}\n连续签到：{continueSignDaysSum}天\n签到周期：{rouund_day}天/{rewardDay}天\n"             
            except:
                print(res.json()["data"]["signInfo"]["msg"])
                msg = "签到失败\n"
        else:
            print(res.json()["msg"])
            msg = "签到失败1\n"
        return msg
    except:
        return "签到失败2\n"

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
        #可能判断不准确（我到现在只遇到'' 和 '1'这种情况，不知道是否有其他情况）
        if vipTypes == '' or vipTypes == ' ':
            nickname = nickname +'你可能不是爱奇艺会员，所以签到脚本可能不成功\n'
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
        print('='*40)
        main(get_args())
        print('='*40)
    finally:
        Session.close()
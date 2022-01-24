'''
@FILE    :   action.py
@DSEC    :   爱奇艺签到
@AUTHOR  :   ioutime
@DATE    :   2021/12/08  21:26:17
@VERSION :   2.1
'''

import requests
import argparse
from urllib.parse import unquote
import json
import datetime
import calendar
import time

def main(infos):
    '''爱奇艺签到、每日三次抽奖,cookie签到'''
    start = time.perf_counter()
    cookie = infos["cookie"]
    p00001 = infos["p00001"]
    # Run tasks
    if not cookie:
        if not p00001:
            print("缺少必要参数")
            end = time.perf_counter()
            runTime = "\n执行时间:"+ str(end - start)
            push_info(infos,"缺少必要参数"+runTime)
        else:
            p00001s = p00001.split(',')
            more_accounts(infos,p00001s)
    elif cookie and p00001:
        p00001s = p00001.split(',')
        more_accounts(infos,p00001s)
    else:
        #转换cookie
        dct = transform(infos,cookie)
        if dct == None:
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
                nickname = nickname +'可能是非会员\n'
        except Exception as e:
            print(e)
            nickname = ''
        #查询抽奖次数
        chance = draw(dct,0).get('chance')
        #抽奖
        msg_draw = '\n今日抽奖次数:'+ str(chance)
        res_msg = ''
        while(chance > 0):
            res_msg = res_msg + '\n第'+ str(chance % 3 + 1) +'次抽奖:'+ draw(dct,1).get('msg')
            chance-=1
            time.sleep(1)
        #签到
        msg0  = nickname + member_sign(dct)
        #用户信息
        msg = msg0 + get_info(dct) + msg_draw + res_msg 
        end = time.perf_counter()
        runTime = "\n执行时间:"+ str(end - start)
        msg = msg + runTime
        print(msg)
        push_info(infos,msg)


def more_accounts(infos,p00001):
    '''
    多账号签到
    '''
    ans = ''
    for i in p00001:
        ans = ans + "第%s账号:" % (p00001.index(i) + 1)
        print ("第%s账号:" % (p00001.index(i) + 1))
        if len(i) >= 20:
            dct = {}
            dct['P00001']=i
            #签到
            msg  = member_sign(dct)
            if msg!='失败\n':
                ans = ans + '   签到成功\n'
            else:
                ans = ans + '   签到失败!\n'
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
            requests.get(url=url)
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
    url = "https://serv.vip.iqiyi.com/vipgrowth/query.action"
    params = {
        "P00001": P00001
    }
    try:
        res = requests.get(url, params=params)
        if res.json()["code"] == "A00000":
            try:
                print(res.json())
                state = res.json()["msg"]
                growthvalue = res.json()["data"]["growthvalue"]
                msg = f"{state}\n当前 VIP 成长值:{growthvalue}天\n"                        
            except:
                print(res.json()["msg"])
                print("签到失败\n")
                msg = "失败\n"
        else:
            print(res.json()["msg"])
            print("签到失败1\n")
            msg = "失败\n"
        return msg
    except:
        print("签到失败2\n")
        return "失败\n"


def get_info(cookies_dict):
    '''
    获取用户信息
    '''
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
            msg = f"VIP等级:{level}\n升级需成长值:{distance}\nVIP到期时间:{deadline}"
        except:
            print("获取具体信息失败")
            msg = ""
    else:
        print("获取个人信息失败")
        msg = ""
    return msg

def draw(cookies_dict,type):
    '''
    查询抽奖次数,抽奖
    type: 0 查询次数；1 抽奖
    '''
    P00001 = cookies_dict.get('P00001')
    P00003 = cookies_dict.get('P00003')
    url = "https://iface2.iqiyi.com/aggregate/3.0/lottery_activity"
    params = {
        "lottery_chance": 1,
        "app_k": "0",
        "app_v": "0",
        "platform_id": 10,
        "dev_os": "2.0.0",
        "dev_ua": "COL-AL10",
        "net_sts": 1,
        "qyid": "2655b332a116d2247fac3dd66a5285011102",
        "psp_uid": P00003,
        "psp_cki": P00001,
        "psp_status": 3,
        "secure_v": 1,
        "secure_p": "0",
        "req_sn": round(time.time()*1000)
    }
    # 抽奖删除 lottery_chance 参数
    if type == 1:
        del params["lottery_chance"]
    res = requests.get(url, params=params)
 
    if not res.json().get('code'):
        chance = int(res.json().get('daysurpluschance'))
        msg = res.json().get("awardName")
        return {"status": "成功", "msg": msg, "chance": chance}
    else:
        try:
            msg = res.json().get("kv", {}).get("msg")
        except:
            msg = res.json()["errorReason"]
        return {"status": "失败", "msg": msg, "chance": 0}

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
    P00003 = dct.get('P00003')
    if P00001 == None:
        msg0 = "输入的cookie有问题(P00001)，请重新获取"
        print(msg0)
        push_info(infos,msg0)
        return
    if P00003 == None:
        msg0 = "输入的cookie有问题(P00003)，请重新获取"
        print(msg0)
        push_info(infos,msg0)
        return
    return dct


if __name__=="__main__":
    print('='*40)
    main(get_args())
    print('='*40)
# **Aiqiyi-Sign**

> 爱奇艺签到打卡
>
> 爱奇艺会员签到打卡，增加经验值，增加爱奇艺会员天数（连续打卡28天，可以增加10天会员）
>
> 项目地址：[Aiqiyi_Sign](https://github.com/ioutime/Aiqiyi_Sign)


## 脚本功能：

1. 登录爱奇艺
2. 支持签到，并显示今日成长值，vip到期时间等
3. 支持本地命令行执行
4. 支持pushplus 微信公众号推送
5. 支持 GitHub Actions 部署

## 注意事项：

- 需要是爱奇艺会员
- 不要太频繁运行该脚本，否则会触发爱奇艺登录的滑块验证
- 需要关闭设备锁


使用方法:
---

### 安装依赖

```shell
pip install -r requirements.txt
```

### 本地执行脚本

参数，phone 和 password 是必要的，其他的选填

```shell
usage: action.py [-h] [-t TOKEN] phone password

positional arguments:
  phone       Your Phone Number.
  password    The plaint text or MD5 value of the password.

optional arguments:
  -h, --help  show this help message and exit
  -t TOKEN    pushplus的token值
```

eg:

```shell
python action.py 电话号码 密码
```

结果

```
========================================
nickname----->登录成功
今日已签到(或签到成功)
成长值+1
连续签到：156天
签到周期：16天/28天
VIP等级：4
升级需成长值：327
VIP到期时间:2021-10-03
nickname----->注销成功!
========================================
```



### pushplus 微信公众号推送

使用[pushplus](http://www.pushplus.plus/)平台进行推送。

使用方法：

1. 访问[pushplus](http://www.pushplus.plus/)官网，登录
2. 找到**一对一推送**，并复制你的**token**
3. 执行脚本时指定参数`-t`，后接上述 token 值

<img src="/img/2021-7-15 token.png"  />

示例：

```shell
python .\action.py 电话号码 密码 -t token
```

结果：

```
今日已签到
成长值 1
连续签到：156天
签到周期：16天/28天
VIP等级：4
升级需成长值：327
VIP到期时间:2021-10-03
```



### github仓库部署:

#### 	1. Fork 该仓库

<img src="/img/2021-7-15 1-0.png" style="zoom:50%;" />

#### 	2. 创建 Secrets

```
创建 PHONE，填入手机号（必填）
创建 PASSWORD（必填）
创建 TOKEN (选填,pushplus的token值)		
```

#### 	<img src="/img/2021-7-15 1.png" style="zoom:50%;" />	  

#### 	3.启用 Action

点击 Actions，选择 **I understand my workflows, go ahead and enable them**

<img src="/img/2021-7-15 1-1.png"  />

**直接fork来的仓库不会自动执行！！！**

必须手动修改项目提交上去，最简单的方法就是修改下图的README.md文件（右侧有网页端编辑按钮）。

<img src="/img/2021-7-15 2.png" style="zoom: 80%;" />	

随便修改什么都行，修改完commit就可以了

<img src="/img/2021-7-15 3.png" style="zoom: 67%;" />

之后**每天 0 点**会自动执行一次脚本



联系方式：
---

邮箱：ioutime@163.com；有问题联系

## 建议：

    关注爱奇艺的公众号，能接收到会员天数的增加消息


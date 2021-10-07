GitHub部署
---

#### 	1. Fork 该仓库

<img src="img/2021-7-15 1-0.png"  />

#### 	2. 创建 Secrets，必填COOKIE（由于手机号登录容易出现安全验证，所以取消PHONE和PASSWORD的必填，改为选填）

```
创建 COOKIE (必填)
创建 PHONE，填入手机号（选填）
创建 PASSWORD，明文密码（选填）
创建 TOKEN (选填,pushplus的token值)		
```

***cookie值获取方法见上面***

<img src="img/2021-7-15 1.png" style="zoom:50%;" />	  

#### 	3.启用 Action

点击 Actions，选择 **I understand my workflows, go ahead and enable them**（第一次用可能会出现）

<img src="img/2021-7-15 1-1.png"  />

**直接fork来的仓库不会自动执行！！！**，最简单的方法就是， **手动修改项目**提交上去，最简单的方法就是修改下图的README.md文件（右侧有网页端编辑按钮）。

<img src="img/2021-7-15 2.png"  />	

随便修改什么都行，修改完commit就可以了

<img src="img/2021-7-15 3.png"  />

之后**每天 0 点**会自动执行一次脚本


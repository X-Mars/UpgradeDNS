# UpgradeDNS
### 功能介绍
用于将阿里云解析到动态ip  
如果服务器位于 ***动态公网ip*** 的环境，那么多数用户在使用 ***花生壳*** 等第三方实现动态域名解析，速度慢，最主要二级或者多级郁闷 ***不专业*** ！  
如果你刚好使用了阿里云的域名云解析，那么此时，你可以使用本脚本实现 ***一级域名*** 的动态解析了。
### 使用方法
1. 安装 ***python2.7 (必须)***
2. 安装阿里云api的python sdk
```shell
pip2.7 install aliyun-python-sdk-core
pip2.7 install aliyun-python-sdk-alidns
```
3. 阿里云控制台申请 ***Access Key*** ，并修改脚本中的 ***"ID"*** 与 ***"Secret"***
4. 如有ECS， ***"RegionId"*** 设置为对应区域，没有ECS就保持不变
5. ***"HostNameList"*** 添加需要自动更新的域名
6. ***"Type"*** 为dns类型，默认为 ***A记录***
7. 脚本使用
```shell
python2.7 UpgradeDNS.py
```
8. 其他
如果ip经常会自动更换，也可以设置定时任务，定时执行脚本哦。

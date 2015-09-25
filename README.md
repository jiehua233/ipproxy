# 代理IP抓取

## 原理说明

通过不断在各大代理IP网站上抓取数据,同时在本地进行代理测试,提取可用的代理IP,并记录其时延,将数据以有序集合保存到redis sorted sets.

程序定期进行数据刷新,删除过期的代理IP,同时抓取新的数据.

代理IP分为三个匿名等级:高匿, 普匿, 透明; 程序中以3, 2, 1标记, 0:未知;可以通过修改`validate.py`中的`r=[3, 2, 1]`指定抓取等级;

保存在redis中的数据,key: `proxy_ip_ping_3`, `proxy_ip_ping_2`, `proxy_ip_ping_1`;

针对某网站时, 可以修改`validate.py`中`_ping()`的`url`值;

## 使用方法

新建python虚拟环境

```bash
$virtualenv ipproxy
$source ipproxy/bin/activate
$pip install -r requirements.txt
```

启动脚本

    $python main.py

调用方法

    参考 `example`

## 数据源

### 每日更新

* [http://www.cz88.net/proxy/http_2.shtml]()
* [http://blog.kuaidaili.com/]()
* [http://www.ip002.com/]()

### 实时更新

* [http://ip.zdaye.com/]()
* [http://www.kuaidaili.com/free/inha/]()
* [http://www.xici.net.co/]()
* [http://cn-proxy.com/archives/218]()
* [http://cn-proxy.com/]()
* [http://www.66ip.cn/3.html]()

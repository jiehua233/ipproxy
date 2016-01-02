# 代理IP抓取

求 star ⭐️ （没错，我就是这么厚脸皮......）

## 原理说明

通过在网络上爬取公开的代理ip，同时在本地进行代理测试，提取可用的代理IP，并记录其网络延时,最后将结果保存到文件以及redis zset(可选).

代理IP分为三个匿名等级：高匿, 普匿, 透明; 程序中以3, 2, 1标记, 0:未知.

## 使用方法

新建python虚拟环境

```bash
$ virtualenv ~/virtualenv/ipproxy
$ source ~/virtualenv/ipproxy/bin/activate
$ pip install -r requirements.txt
```

修改配置文件 `etc/config.py`

```bash
$ cp etc/config.sample.py etc/config.py
$ vim etc/config.py
```
```py
SNIFFER = {
    'PROCESS_NUM': 4,                   # 开启进程数
    'THREAD_NUM': 500,                  # gevent线程数
    'PROXY_TYPE': [0, 1, 2, 3],         # 指定代理IP匿名程度
    'TARGET': 'http://www.baidu.com',   # 测试代理IP的目标
    'TIMEOUT': 10,                      # 测试延时
    'OUTPUT': True,                     # 是否将结果输出到文件（`data/`）
    'BACKEND': 'localhost:6379',        # 是否将结果保存到redis（不保存则为''）
    'KEY_PREFIX': 'ipproxy:',           # redis key前缀
}

LOGGER = {
    "PATH": './ipproxy.log'             # 程序日志
}
```

启动脚本

    $ python main.py
    # 抓取过程的日志保存在 ipproxy.log
    $ tail -f ipproxy.log

注意：运行过程中并没有将结果实时保存到到文件，而是最后才统一写入到文件和redis，因此请耐心等待其运行完毕。

## 抓取结果

结果默认以纯文本形式保存在 `data/` 目录下，格式为 `ip\tspeed`，第二列数值表示代理请求延时

    120.132.95.8:8080	0.0899851322174
    219.136.252.120:80	0.0968101024628
    59.49.35.51:80	0.109569072723
    123.126.108.190:3128	0.136920213699
    111.205.46.26:80	0.137912988663
    106.3.37.223:80	0.146553039551
    ......

如果只需ip，简单操作：

    $ cut -f 1 data/ipproxy-1.txt > data/ip-1.txt

如果在`etc/config.py`中设置了`BACKEND`，则结果也将保存到redis zset方便其他程序使用，具体参考如下示例。

在`redis-cli`中可通过如下命令查看，默认`KEY_PREFIX=ipproxy`:

    $ redis-cli
    127.0.0.1:6379> keys ipproxy:*
    1) "ipproxy:1"
    2) "ipproxy:3"
    3) "ipproxy:2"

    127.0.0.1:6379> zcard ipproxy:1
    (integer) 787

    127.0.0.1:6379> zrange ipproxy:1 0 787
    1) "203.195.162.96:8080"
    2) "123.54.6.37:8000"
    3) "117.177.250.146:8081"
    4) "117.177.250.146:8080"
    5) "202.108.23.231:80"
    6) "195.167.216.50:80"
    7) "124.206.133.227:80"
    8) "183.239.173.138:8080"
    9) "91.121.139.227:80"
    10) "168.213.3.106:80"
    11) "61.136.247.238:3128"
    ......

## 示例

示例中简单示范了如何使用存储在`redis zset`中的代理ip

    参考 `example`

## 抓取优化tips

优化主要是通过对`etc/config.py`的合理配置来提高代理ip的可用性:

* 修改`TARGET`可以使抓取到的代理ip更具针对性和有效性

比如想通过代理ip来批量注册某网站`http://mail.abc.com`邮箱，可以将TARGET设置为`http://mail.abc.com`，这样可以保证抓取到的ip对该网站都是可访问的

* 修改`TIMEOUT`设置超时

根据自己的需求，设置一个可容忍的请求延时，设置较大时，可以抓取到更多代理IP（但也会导致抓取速度大大下降）；设置较小时，抓取到的代理ip数量将会减少

* 修改`PROXY_TYPE`

通过这个选项可以限制抓取的代理ip类型（透明，普匿，高匿），请根据自己的需求设置，这个选项并不保证抓取的代理ip绝对归属于某个类型，比如虽然设置了高匿，但抓取到的ip仍然可能是其他类型（小概率）

* 修改`PROCESS_NUM`和`THREAD_NUM`

修改启动的进程数和线程数，越大速度越快，但也取决于你的电脑配置和网络状态等因素

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

## CHANGELOGS

v 0.2.2

* 抓取过程中在STDOUT中输出部分日志信息，避免`假死`

v 0.2.1

* 更新README，修复部分小bug
* 更新`example`示例

v 0.2.0

* 代码重构，调整了各个模块目录
* 加入了`multiprocess`和`gevent`来提高抓取效率
* 独立配置文件，用户可根据自己的需要调整相应参数来抓取到更加有效的代理ip
* 抓取结果保存到纯文本和redis（可根据自己实际需要选择，非必须）
* 去掉了部分已经失效的公开代理源，增加新的源
* 加入log，打印到文件`ipproxy.log`

v 0.1.0
    
* 完成了基本的抓取功能
* 数据保存在`redis zset`

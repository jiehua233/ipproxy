# 代理IP抓取

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
$ mv etc/config.sample.py etc/config.py
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

    $python main.py

### 调用方法(redis zset)

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

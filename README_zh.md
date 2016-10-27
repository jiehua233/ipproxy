# IPProxy 

一个从各大网站提取代理IP的自动化工具。

(此处应有赞，快点 star ⭐️ 呀)


## 依赖

* Python 2.7
* Virtualenv(可选)
* Pip(可选)

我们推荐你使用 `virtualenv` 创建一个新的 python 虚拟环境来运行这个工具，并使用 `pip` 来安装所需要的第三方依赖。
这样，在遇到问题时可以更容易排查解决，同时也可以避免在系统中安装多余的包。


## 用法

### 新建虚拟环境

使用 virtualenv 新建一个虚拟环境，只需要在 shell 终端执行：

    $ virtualenv ~/virtualenvs/ipproxy
    $ source ~/virtualenvs/ipproxy/bin/activate 
    (ipproxy)$ pip install -r requirements.txt 

如果遇到 pypi 下载缓慢，可以使用 douban pypi:

    (ipproxy)$ pip install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

### 提取代理IP

运行下面这个脚本，就可以自动地从各大代理IP网站提取大量ip：

    (ipproxy)$ python crawl.py 

耐心等待，脚本执行完成后，会将结果以 csv 的格式保存在 `data` 目录中:

```
all.csv
china.csv
foreign.csv
high_anonymous.csv
low_anonymous.csv
non_anonymous.csv
```

每一个 csv 文件都包含了 4 列：IP，端口，匿名程度，地理位置：

```
ip,port,anonymous,info
110.73.0.125,8123,3,中国-广西-防城港
207.226.142.113,3128,3,中国-香港
......
```

对于 `匿名程度` 这一列, 数字 0~3 分别代表:

* 0: 未知
* 1: 透明 
* 2: 普通匿名
* 3: 高度匿名

### 筛选代理IP

通过上面的操作，我们已经获取了大量代理IP，不过针对你的本地网络环境及目标网络环境，
通常只有少部分代理IP是可用的。因此，我们需要进一步进行筛选。

脚本参数列表：

    (ipproxy)$ python check.py --help

```
usage: check.py [-h] [--target TARGET] [--timeout TIMEOUT] [--worker WORKER]
                [--thread THREAD] [--loglevel LOGLEVEL]
                input

positional arguments:
  input                the input proxy ip list, in csv format(supprot gz)

optional arguments:
  -h, --help           show this help message and exit
  --target TARGET      target uri to validate proxy ip, default:
                       http://www.baidu.com
  --timeout TIMEOUT    timeout of validating each ip, default: 15s
  --worker WORKER      run with multi workers, default: CPU cores
  --thread THREAD      run with multi thread in each worker, default: 100
  --loglevel LOGLEVEL  set log level, e.g. debug, info, warn, error; default:
                       info
```

为了提高筛选的速度，我们采用了多进程/多线程的方式并发处理，`worker` 代表进程数，
`thread` 代表线程数；`timeout` 代表请求超时时间（秒）；`target` 代表目标网站。

比如，我们想要筛选高度匿名的代理IP：

    (ipproxy)$ python check.py data/high_anonymous.csv

当然，你也可以指定更多参数：

    (ipproxy)$ python main.py input.csv --target http://www.google.com.hk --timeout 10 --worker 4 --thread 200 --loglevel debug

输出的结果跟原来的 csv 基本一致，并增加了 `速度` 一列(代表请求消耗的时间，越小越好)：

```
ip,port,anonymous,info,speed
110.84.128.143,3128,1,中国-福建-福州,0.10766482353210449
58.247.125.205,10032,3,中国-上海-上海,0.5216059684753418
......
```


## 示例


代理IP的使用方法，可以参考 [example](example/example.py) .


## 数据源

* [http://www.cz88.net/proxy]()
* [http://www.kuaidaili.com]()
* [http://www.xicidaili.com]()
* [http://cn-proxy.com]()
* [http://www.66ip.cn]()


## 版权

没时间解释了，快上车 (⊙﹏⊙)b

# IPProxy 

[中文版](README_zh.md)

A simple tool to crawl proxy ip.

## Requirements

* Python 2.7
* Virtualenv(optional)
* Pip(optional)

You can use `virtualenv` to make a new python virtual environment, and `pip` to install any dependencies. 
However, you can use any other tool you like.

## Usage 

### Build up env

Build up a new virtualenv for this project, run in a shell:

    $ virtualenv ~/virtualenvs/ipproxy
    $ source ~/virtualenvs/ipproxy/bin/activate 
    (ipproxy)$ pip install -r requirements.txt 

### Crawl possible proxy ip

Then crawl any possible proxy ip from some pre-defined website:

    (ipproxy)$ python crawl.py 

Wait for a while, just a cup of coffee (may be a little bit longer, it all depends on your network),
and you'll get the result in the `data` directory:

```
all.csv
china.csv
foreign.csv
high_anonymous.csv
low_anonymous.csv
non_anonymous.csv
```

Every csv file consist four columns: `ip`, `port`, `anonymous`, `info`. Looks like:

```
ip,port,anonymous,info
110.73.0.125,8123,3,中国-广西-防城港
207.226.142.113,3128,3,中国-香港
......
```

For `anonymous` column, it means:

* 0: unknown
* 1: none 
* 2: low
* 3: high

### Check available proxy ip

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

So take the above csv as input, you can just run:

    (ipproxy)$ python check.py data/high_anonymous.csv

You can also specific some more arguments:

    (ipproxy)$ python main.py input.csv --target http://www.google.com.hk --timeout 10 --worker 4 --thread 200 --loglevel debug

Output(`data/proxyip.csv`) is similiar to input, with one more col `speed`(the smaller the better):

```
ip,port,anonymous,info,speed
110.84.128.143,3128,1,中国-福建-福州,0.10766482353210449
58.247.125.205,10032,3,中国-上海-上海,0.5216059684753418
......
```


## Example

Take a look at `example.py`.


## Data Source 

* [http://www.cz88.net/proxy]()
* [http://www.kuaidaili.com]()
* [http://www.xicidaili.com]()
* [http://cn-proxy.com]()
* [http://www.66ip.cn]()


## License

Just enjoy it.

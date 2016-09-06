# IPProxy 

A simple tool to validate any possible proxy ip. It accepts input in csv format(possible proxy ip list), 
then save output to another csv file(available proxy ip list).

## Requirements

* Python 2.7
* Virtualenv(optional)
* Pip(optional)

You can use `virtualenv` to make a new python virtual environment, and `pip` to install any dependencies. 
However, you can use any other tool you like.

## Usage 

Build up a new virtualenv for this project, run in a shell:

    $ virtualenv ~/virtualenvs/ipproxy
    $ source ~/virtualenvs/ipproxy/bin/activate 
    (ipproxy)$ pip install -r requirements.txt 

Options help:

    $ python main.py --help 

```
usage: main.py [-h] [--target TARGET] [--timeout TIMEOUT]
               [--process_num PROCESS_NUM] [--thread_num THREAD_NUM]
               [--log LOG]
               input_csv output_csv

positional arguments:
  input_csv             the input proxy ip list, in csv format(supprot gz)
  output_csv            the output proxy ip list, in csv format

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT       the output proxy ip list, default: output.csv
  --target TARGET       target uri to validate proxy ip, default: http://www.baidu.com
  --timeout TIMEOUT     timeout for validating each ip, default: 15s
  --process_num NUM     run in multi process, default: CPU cores
  --thread_num NUM      run in multi thread of each process, default: 100
  --log LOG             set loggin level, e.g. debug, info, warn, error; default: info
```

So you can just run:

    (ipproxy)$ python main.py input.csv 

it will take `input.csv` as input, and save the available proxy ip to `output.csv`. 

You can also specific some arguments:

    (ipproxy)$ python main.py input.csv --output myproxy.csv --target http://www.baidu.com --timeout 20 --process_num 4 --thread_num 400 --log debug

## Input

Input csv format should look like:

```
ip,port,anonymous,info
110.73.0.125,8123,3,中国-广西-防城港
207.226.142.113,3128,3,中国-香港
......
```

In order to get a list of possible proxy ip, you can use [this tool](https://github.com/jiehua233/ipproxy-pool).

Moreover, in order to simplify your work, I've run it on my own server(update every 6 hours using crontab). 
You should be able to download it from [here](http://static.chenjiehua.me/ipproxy/):

* all.csv
* china.csv
* foreign.csv
* high_anonymous.csv
* low_anonymous.csv
* non_anonymous.csv

Just chose the one you need.

## Output

Output is similiar to input, with one more col `speed`(the smaller the better):

```
ip,port,anonymous,info,speed
110.84.128.143,3128,1,中国-福建-福州,0.10766482353210449
58.247.125.205,10032,3,中国-上海-上海,0.5216059684753418
......
```

## Example

Take a look at `example.py`.

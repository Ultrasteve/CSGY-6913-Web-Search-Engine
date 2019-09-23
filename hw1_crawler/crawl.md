# python爬虫开发日志  
计划使用多线程 or 协程 来增加吞吐量。  

## getPage方法  
<ul>
    <li>urllib和requests的区别</li>
    <p>requests简单许多，但是需要单独安装。</p>
</ul>  
  
## saveToLocalLog方法  
<ul>
    <li>python的文件读写</li>
    <p>mode 有r只读 r+ w+可读可覆盖写，w a 没有的时候不会报错  
    f = open(path, mode)  
    f.read()读全部  
    f.readline()读一行  
    f.seek()移动文件指针  
    使用with可以自动关闭文件，不过也可以用f.close()关闭文件</p>
</ul>

## parseData方法  
关于python的优先队列，若要自己定义比较规则，需要自己实现一个类，并实现cmp函数  
[link](https://www.cnblogs.com/mtcnn/p/9424108.html)

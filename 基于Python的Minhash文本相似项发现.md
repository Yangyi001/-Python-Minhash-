## 基于Python的Minhash文本相似项发现
### 前言
一个基本的数据挖掘问题就是从数据中获得“相似”项。它可以应用在许多方面，典型的应用场景是：通过比较相似度检测抄袭网页，论文查重，检测是否是镜像网页；另一类非常重要的集合相似度的应用称为**协同过滤**，在协同过滤中，系统会向用户推荐相似兴趣用户所喜欢的那些项。  

**距离测度**  
距离测度可以用来衡量集合之间的相似度，集合越接近，距离测度越短。  
一些常见的距离测度有欧氏距离、jaccard距离、余弦距离、编辑距离、海明距离等。  

本篇采用**Minhash技术**，对两个文本数据集Amazon News和Google Report，在Google Report数据集中寻找到Amazon News每条记录的最高**Jaccard相似度**的记录，给出Amazon News数据集中每条记录在Google Report数据集中相似度最高的记录，作为匹配结果输出。  
基于此我们可以通过对两个文本数据集每条相似度最高的记录的jaccard相似度进行统计，以衡量两个文本的相似度，检测是否抄袭。  

### 原理分析及流程
#### Jaccard相似度定义

两条记录之间的相似度我们可以用Jaccard相似度来衡量，Jaccard相似度通过计算交集的相对大小来获得集合之间的相似度，公式如下：
$$ Sim(C1, C2)= |C1\cap C2|/|C1\cup C2| $$即两条记录的交集除以两条记录的并集。  

*注：jaccard相似度不是距离测度，因其不符合集合越接近，距离测度越短。而1-jaccard相似度确是一个距离测度，称为jaccaed距离*

#### Minhash介绍
对于大规模的文本，若要比较相似度，一一比较两个文本的字符是不现实的，会消耗相当大的时间和空间资源，对此我们牺牲一些准确度，使用Minhash技术对文本特征进行压缩提取。不直接比较两个文本，而是利用特征提取的Minhash技术比较其签名。  

理论上选用的Minhash函数应该满足如下条件：两个相似度高的文本其签名相似度也应该较高，反之。  

为了避免偶然出现的两个相似度高的文本其哈希签名相似度低（这是极有可能出现的，因为符合以上条件的Minhash函数的选取是十分困难的），我们通常采用多个Minhash函数来进行比较，增大准确率。这样我们就可以节省大量的时间和空间开销，能较短时间内处理大规模的文本。  

#### Jaccard相似度与Minhash
若我们选用了多个Minhash函数，下面结论是成立的：Jaccard相似度和最小哈希值之间有如下关系：两条记录的Jaccard相似度等于它们最小哈希值相似概率。（此处不做原理分析）  

所以我们要计算两个文本之间的Jaccard相似度，不直接两个文本的字符，而是使用多个Minhash计算出多个最小哈希值，求文本间最小哈希值相似概率（此法计算所得的Jaccard相似度与真实值有偏差，当选取的Minhash足够合理且数量较多，所得结果越准确）。  

#### 实现流程
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200516221307992.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NjMwMjQ4Nw==,size_16,color_FFFFFF,t_70#pic_center)

### 具体实现
导入所需要的包
```
from datasketch import MinHash
import string
```
读入并查看原始数据集前五行
```
In [1]: Amazon = open('amazon-titles.txt')

In [2]: for line in range(5):
   ...:     print(Amazon.readline())
   ...:
clickart 950 000 - premier image pack (dvd-rom)

ca international - arcserve lap/desktop oem 30pk

noah's ark activity center (jewel case ages 3-8)

peachtree by sage premium accounting for nonprofits 2007

singing coach unlimited


In [3]: Google = open('google-names.txt')

In [4]: for line in range(5):
   ...:     print(Google.readline())
   ...:
learning quickbooks 2007

superstart! fun with reading & writing!

qb pos 6.0 basic software

math missions: the amazing arcade adventure (grades 3-5)

production prem cs3 mac upgrad
```
对每一行首先去除标点符号，然后按空白字符分词，部分分词结果如下：
```
In [7]: Amazon_split[0:3]
Out[7]:
[['clickart 950 000 - premier image pack (dvd-rom)',
  ['clickart', '950', '000', 'premier', 'image', 'pack', 'dvdrom']],
 ['ca international - arcserve lap/desktop oem 30pk',
  ['ca', 'international', 'arcserve', 'lapdesktop', 'oem', '30pk']],
 ["noah's ark activity center (jewel case ages 3-8)",
  ['noahs', 'ark', 'activity', 'center', 'jewel', 'case', 'ages', '38']]]

In [8]: Google_split[0:3]
Out[8]:
[['learning quickbooks 2007', ['learning', 'quickbooks', '2007']],
 ['superstart! fun with reading & writing!',
  ['superstart', 'fun', 'with', 'reading', 'writing']],
 ['qb pos 6.0 basic software', ['qb', 'pos', '60', 'basic', 'software']]]
```
如上，为记录及其分词结果。  
计算Amazon News数据集中每条记录在Google Report数据集中相似度最高的记录，部分匹配结果前如下：  
```
In [10]: amazon_google_max_jaccard[0:5]
Out[10]:
[['clickart 950 000 - premier image pack (dvd-rom)',
  'clickart 950000 - premier image pack (dvd-rom)',
  0.6484375],
 ['ca international - arcserve lap/desktop oem 30pk',
  'ca blapdskapoem30 oem arcserve backup v11.1 win 30u for laptops and desktops 0757943274004',
  0.2265625],
 ["noah's ark activity center (jewel case ages 3-8)",
  "the beginners bible: noah's ark activity center: activity center",
  0.3515625],
 ['peachtree by sage premium accounting for nonprofits 2007',
  'sage (ptree) - vernfp2007rt - premium accounting for nonprofits 2007',
  0.578125],
 ['singing coach unlimited',
  'singing coach unlimited - electronic learning products',
  0.4765625]]
```
如上输出所示，给出Amazon News数据集中每条记录在Google Report数据集中相似度最高的记录及最高的jaccard相似度。  

进一步我们可以通过对两个文本数据集每条相似度最高的记录的jaccard相似度进行统计，以衡量两个文本的相似度，检测是否抄袭。

### 总结

相似项发现一个基本的数据挖掘问题。它可以应用在许多方面。  

本篇介绍了其在文档相似度发现中的应用，其他典型的应用场景是：通过比较相似度检测抄袭网页，论文查重，检测是否是镜像网页；另一类非常重要的集合相似度的应用称为**协同过滤**，在协同过滤中，系统会向用户推荐相似兴趣用户所喜欢的那些项。  

有兴趣的读者可以参考网上资料深入了解。

#### 附录
*数据集：amazon-titles.txt  和  google-names.txt  及完整代码已放置于：[Github](https://github.com/Yangyi001/-Python-Minhash-.git)*
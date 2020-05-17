## 基于Python的Minhash算法介绍及应用
### 前言


本篇采用**Minhash技术**，对两个文本数据集Amazon News和Google Report，在Google Report数据集中寻找到Amazon News每条记录的最高**Jaccard相似度**的记录，给出Amazon News数据集中每条记录在Google Report数据集中相似度最高的记录，作为匹配结果输出。  

附件：amazon-titles.txt  和  google-names.txt  
已放置于git  

### 原理分析及流程
#### Jaccard相似度定义

两条记录之间的相似度我们可以用Jaccard相似度来衡量，Jaccard相似度通过计算交集的相对大小来获得集合之间的相似度，公式如下：
$$ Sim(C1, C2)= |C1\cap C2|/|C1\cup C2| $$即两条记录的交集除以两条记录的并集。

#### Minhash介绍
对于大规模的文本，若要比较相似度，一一比较两个文本的字符是不现实的，会消耗相当大的时间和空间资源，对此我们牺牲一些准确度，使用Minhash技术对文本特征进行压缩提取。不直接比较两个文本，而是利用特征提取的Minhash技术比较其签名。  

理论上选用的Minhash函数应该满足如下条件：两个相似度高的文本其签名相似度也应该较高，反之。  

为了避免偶然出现的两个相似度高的文本其哈希签名相似度低（这是极有可能出现的，因为符合以上条件的Minhash函数的选取是十分困难的），我们通常采用多个Minhash函数来进行比较，增大准确率。这样我们就可以节省大量的时间和空间开销，能较短时间内处理大规模的文本。  

#### Jaccard相似度与Minhash
若我们选用了多个Minhash函数，下面结论是成立的：Jaccard相似度和最小哈希值之间有如下关系：两条记录的Jaccard相似度等于它们最小哈希值相似概率。（此处不做原理分析）  

所以我们要计算两个文本之间的Jaccard相似度，不直接两个文本的字符，而是使用多个Minhash计算出多个最小哈希值，求文本间最小哈希值相似概率（此法计算所得的Jaccard相似度与真实值有偏差，当选取的Minhash足够合理且数量较多，所得结果越准确）。  

#### 实现流程
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200516221307992.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NjMwMjQ4Nw==,size_16,color_FFFFFF,t_70#pic_center)


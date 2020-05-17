# 导入所需要的包
from datasketch import MinHash
import string

# 储存带分词的数据行
Amazon_split = []
Google_split = []

# 标点符号的翻译字典
table = str.maketrans('','',string.punctuation)

def split_line(line):
    # 对行进行分词，去除标点符号，按空白字符分词
    wipe_line = line.translate(table)
    split_line = wipe_line.split()

    return split_line

# 读入amazon数据集并分词，以列表保存原数据行和分词结果
with open('amazon-titles.txt', encoding='ISO-8859-1') as Amazon:
    for line in Amazon.readlines():
        line = line.rstrip('\n')
        Amazon_split.append([line, split_line(line)])

# 读入google数据集并分词，以列表保存原数据行和分词结果
with open('google-names.txt', encoding='ISO-8859-1') as Google:
    for line in Google.readlines():
        line = line.rstrip('\n')
        Google_split.append([line, split_line(line)])

# 定义计算两行文本jaccard相似度的函数
def calculate_jaccard(text1,text2):
    # 计算两行文本的jaccard相似度
    minihash1, minihash2 = MinHash(), MinHash()

    for word in text1:
        minihash1.update(word.encode('utf-8'))

    for word in text2:
        minihash2.update(word.encode('utf-8'))

    return minihash1.jaccard(minihash2)

# 保存每一行最匹配的结果
amazon_google_max_jaccard = []

# 对数据行进行匹配
for amazon_line in Amazon_split:
    # 保存最大jaccard相似度及最大相似度的行
    max_jcccard = float('-inf')
    max_jcccard_line = None
    # 寻找jaccard相似度最大的行
    for google_line in Google_split:
        present_jaccard = calculate_jaccard(amazon_line[1], google_line[1])
        if max_jcccard < present_jaccard:
            max_jcccard = present_jaccard
            max_jcccard_line = google_line[0]
    # 加入结果集中
    amazon_google_max_jaccard.append([amazon_line[0], max_jcccard_line, max_jcccard])

# 输出结果前十行
print(amazon_google_max_jaccard[0:10])
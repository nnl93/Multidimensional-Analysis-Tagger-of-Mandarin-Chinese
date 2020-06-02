
# coding: utf-8

# In[92]:


#input your txt file folder
folder = '//'


# In[2]:


#create a csv file to store all linguistic feature data
import csv

with open(folder + 'linguistic_features.csv', 'wb') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)


# In[9]:


#pandas does not allow empty csv to write, so write linguistic features in header
with open(folder + 'linguistic_features.csv', 'w', newline='') as outcsv:
    writer = csv.DictWriter(outcsv, fieldnames = ["Linguistic features"])
    writer.writeheader()


# In[93]:


#load data, read your txt file folder with NLTK
import os
import nltk 
from nltk.corpus import CategorizedPlaintextCorpusReader
corpus = CategorizedPlaintextCorpusReader(
    folder,
    r'(?!\.).*\.txt',
    cat_pattern=os.path.join(r'(neg|pos)', '.*',),
    encoding='utf-8')
corpus.words()
#example words


# In[110]:


#sort text files by their names, if necessary
#if not, check file ids
import fileinput
import fnmatch

files=corpus.fileids()

for f in files: 
    #if fnmatch.fnmatch(f, '7*.txt'):
        print (f)
        #sample_files.append(f)


# In[43]:


import pandas as pd  
df = pd.read_csv(folder + 'linguistic_features.csv')


# In[96]:


#read segmented corpora
sub_corpora=[]
for i in files: 
    sub_corpus=corpus.words(i)
    sub_corpora.append(sub_corpus)


# In[101]:


#first feature english words
#get non-Chinese words
import re
RE = re.compile(u'[⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎，。,；：“”【】、！（）()——《》=？"^\d+$"\r\n]', re.UNICODE)
nochinese_files=[]
for corpus in sub_corpora: 
    nochinese=RE.sub(' ', str(corpus))
    nochinese_files.append(nochinese)


# In[104]:


#get English words 
from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'\w+')
en_words_length=[]
for file in nochinese_files: 
    en_word=tokenizer.tokenize(file)
    en_words_length.append(len(en_word))


# In[105]:


#length of each file in segmented corpora
text_length=[]
for i in sub_corpora: 
    text_length.append(len(i))


# In[108]:


#write standardised english words frequency to linguistic feature file
raw=[x/y for x, y in zip(en_words_length, text_length)]
english_result=[]
for i in raw: 
    english_result.append(round(i*1000, 2))
    
df['english'] = pd.Series(english_result)
df.to_csv(folder + 'linguistic_features.csv')


# In[12]:


#feature AMP amplifiers 
#非常、大大、十分、真的、特别、很、最、肯定、挺、顶、极、
#极为、极其、极度、万分、格外、分外、更、更加、更为、尤其、太、过于、
#老、怪、相当、颇、颇为、有点儿、有些、最为、还、越发、越加、愈加、
#稍、稍微、稍稍、略、略略、略微、比较、较、暴、超、恶、怒、巨、粉、奇
amplifier=['非常', '大大', '十分', '真的', '真', '特别', '很', '最', '肯定', '挺', '顶', '极', '极为', '极其', '极度', '万分', '格外', '分外', '更', '更加', '更为', '尤其', '太', '过于', '老', '怪', '相当', '颇', '颇为', '有点儿', '有些', '最为', '还', '越发', '越加', '愈加', '稍', '稍微', '稍稍', '略', '略略', '略微', '比较', '较', '暴', '超', '恶', '怒', '巨', '粉', '奇', '很大', '相当', '完全', '显著', '总是', '根本', '一定']

#define count and standardise function
def amplifiers(text_type):
    def raw(text_type): 
        return len([x for x in text_type if x in amplifier])
    def normalized(text_type): 
        return raw(text_type) / len(text_type)
    return round(normalized (text_type) * 1000, 2) 


# In[13]:


amplifiers_result=[]
for corpus in sub_corpora: 
    amplifiers_result.append(amplifiers(corpus))
    
df['AMP'] = pd.Series(amplifiers_result)
df.to_csv(folder + 'linguistic_features.csv')


# In[14]:


#strip quotation marks first 
lists=[]
for corpus in sub_corpora: 
    l=list(corpus)
    lists.append(l)


# In[15]:


#feature average word length
def awl(text_type): 
    return round ((sum(len(word) for word in text_type) / len(text_type)), 2)


# In[32]:


awl_result=[]
for l in lists: 
    awl_result.append(awl(l))
    
df['AWL'] = pd.Series(awl_result)
df.to_csv(folder + 'linguistic_features.csv')


# In[17]:


#feature 4 mean sentence length
def asl(text_type): 
    sentences = [[]]
    ends = set('。？!……——')
    for word in text_type:
        if word in ends: sentences.append([])
        else: sentences[-1].append(word)
    if sentences[0]:
        if not sentences[-1]: sentences.pop()
        return round (sum(len(s) for s in sentences)/len(sentences), 2)


# In[31]:


asl_result=[]
for l in lists: 
    asl_result.append(asl(l))

df['ASL'] = pd.Series(asl_result)
df.to_csv(folder + 'linguistic_features.csv')


# In[19]:


#feature 5 standard deviation of sentence length 
import statistics

def asl_std(text_type): 
    sentences = [[]]
    ends = set('。？!……——')
    for word in text_type:
        if word in ends: sentences.append([])
        else: sentences[-1].append(word)
    if sentences[0]:
        if not sentences[-1]: sentences.pop()
        return round(statistics.stdev(len(s) for s in sentences), 2)


# In[20]:


asl_std_result=[]
for l in lists: 
    for corpus in sub_corpora: 
    acl_std_result.append(acl_std(corpus))
    asl_std_result.append(asl_std(l))

df['ASL_std'] = pd.Series(asl_std_result)
df.to_csv(folder + 'linguistic_features.csv')


# In[21]:


#feature 6 mean clause length
def acl(text_type): 
    sentences = [[]]
    ends = set('，：；。？!……——')
    for word in text_type:
        if word in ends: sentences.append([])
        else: sentences[-1].append(word)
    if sentences[0]:
        if not sentences[-1]: sentences.pop()
        return round (sum(len(s) for s in sentences)/len(sentences), 2)


# In[30]:


acl_result=[]
for corpus in sub_corpora: 
    acl_result.append(acl(corpus))

df['ACL'] = pd.Series(acl_result)

df.to_csv(folder + 'linguistic_features.csv')


# In[23]:


#feature 7 standard deviation of clause length 
#import statistics
def acl_std(text_type): 
    sentences = [[]]
    ends = set('，：；。？!……——')
    for word in text_type:
        if word in ends: sentences.append([])
        else: sentences[-1].append(word)
    if sentences[0]:
        if not sentences[-1]: sentences.pop()
        return round(statistics.stdev(len(s) for s in sentences), 2)


# In[29]:


import statistics
acl_std_result=[]
for corpus in sub_corpora: 
    acl_std_result.append(acl_std(corpus))

df['ACL_std'] = pd.Series(acl_std_result)
df.to_csv(folder + 'linguistic_features.csv')


# In[47]:


#feature 13 downtoners DWNT
#一点、有点、有点儿、稍、稍微、一些、有些
downtoners=['一点', '一点儿', '有点', '有点儿', '稍', '稍微', '一些', '有些']
def dwnt(text_type):
    def raw(text_type): 
        return len([x for x in text_type if x in downtoners])
    def normalized(text_type): 
        return raw(text_type) / len(text_type)
    return round(normalized (text_type) * 1000, 2) 


# In[48]:


dwnt_result=[]
for corpus in sub_corpora: 
    dwnt_result.append(dwnt(corpus))
    
df['DWNT'] = pd.Series(dwnt_result)
df.to_csv(folder + 'linguistic_features.csv')


# In[49]:


#feature 16 FPP1 first person pronoun
#我、我的、我自己、我们、我们自己、我们的
#only 我 and 我们 are needed
def fpp1(text_type):
    def raw(text_type): 
        return text_type.count('我')+text_type.count('我们')
    def normalized(text_type): 
        return raw(text_type) / len(text_type)
    return round(normalized (text_type) * 1000, 2) 


# In[50]:


fpp1_result=[]
for corpus in sub_corpora: 
    fpp1_result.append(fpp1(corpus))
    
df['FPP'] = pd.Series(fpp1_result)
df.to_csv(folder + 'linguistic_features.csv')


# In[63]:


#feature 25 SPP2 second person pronoun
#你、你们
def spp2(text_type):
    def raw(text_type): 
        return text_type.count('你')+text_type.count('你们')+text_type.count('您')+text_type.count('您们')
    def normalized(text_type): 
        return raw(text_type) / len(text_type)
    return round(normalized (text_type) * 1000, 2) 


# In[64]:


spp2_result=[]
for corpus in sub_corpora: 
    spp2_result.append(spp2(corpus))
    
df['SPP'] = pd.Series(spp2_result)
df.to_csv(folder + 'linguistic_features.csv')


# In[53]:


#feature 17 hedges HDG
#可能、可以、也许、较少、一些、多个、多为、基本、主要、类似、不少
hedges=['可能', '可以', '也许', '较少', '一些', '多个', '多为', '基本', '主要', '类似', '不少']
def hdg(text_type):
    def raw(text_type): 
        return len([x for x in text_type if x in hedges])
    def normalized(text_type): 
        return raw(text_type) / len(text_type)
    return round(normalized (text_type) * 1000, 2) 


# In[54]:


hdg_result=[]
for corpus in sub_corpora: 
    hdg_result.append(hdg(corpus))
    
df['HDG'] = pd.Series(hdg_result)
df.to_csv(folder + 'linguistic_features.csv')


# In[55]:


#feature 18 INPR indefinite pronouns 无定代词
#任何、谁、大家、某、有人、有个、什么
indefinites=['任何', '谁', '大家', '某', '有人', '有个', '什么']
def inpr(text_type):
    def raw(text_type): 
        return len([x for x in text_type if x in indefinites])
    def normalized(text_type): 
        return raw(text_type) / len(text_type)
    return round(normalized (text_type) * 1000, 2) 


# In[56]:


inpr_result=[]
for corpus in sub_corpora: 
    inpr_result.append(inpr(corpus))
    
df['INPR'] = pd.Series(inpr_result)
df.to_csv(folder + 'linguistic_features.csv')


# In[65]:


#feature 34 SMP seem, appear
#好像、似乎、好象、貌似
def smp(text_type):
    def raw(text_type): 
        return text_type.count('好象')+text_type.count('好像')    +text_type.count('似乎')+text_type.count('貌似')
    def normalized(text_type): 
        return raw(text_type) / len(text_type)
    return round(normalized (text_type) * 1000, 2) 


# In[66]:


smp_result=[]
for corpus in sub_corpora: 
    smp_result.append(smp(corpus))
    
df['SMP'] = pd.Series(smp_result)
df.to_csv(folder + 'linguistic_features.csv')


# In[67]:


#feature 36 third person pronouns
tpp3s=['她', '他', '它', '她们', '他们', '它们']
def tpp3(text_type):
    def raw(text_type): 
        return len([x for x in text_type if x in tpp3s])
    def normalized(text_type): 
        return raw(text_type) / len(text_type)
    return round(normalized (text_type) * 1000, 2) 


# In[69]:


tpp3_result=[]
for corpus in sub_corpora: 
    tpp3_result.append(tpp3(corpus))
    
df['TPP'] = pd.Series(tpp3_result)
df.to_csv(folder + 'linguistic_features.csv')


# In[70]:


#feature 38 emotion words 
def emotion(text): 
    def raw(text): 
        return text.count('烦恼')+text.count('不幸')+text.count('痛苦')+text.count('苦')+text.count('快乐')+text.count('忍')+text.count('喜')+text.count('乐')+text.count('称心')+text.count('痛快')+text.count('得意')+text.count('欣慰')+text.count('高兴')+text.count('愉悦')+text.count('欣喜')+text.count('欢欣')+text.count('可意')+text.count('乐')+text.count('可心')+text.count('欢畅')+text.count('开心')+text.count('康乐')+text.count('欢快')+text.count('快慰')+text.count('欢')+text.count('舒畅')+text.count('快乐')+text.count('快活')+text.count('欢乐')+text.count('畅快')+text.count('舒心')+text.count('舒坦')+text.count('欢娱')+text.count('如意')+text.count('喜悦')+text.count('顺心')+text.count('欢悦')+text.count('舒服')+text.count('爽心')+text.count('晓畅')+text.count('松快')+text.count('幸福')+text.count('惊喜')+text.count('欢愉')+text.count('称意')+text.count('得志')+text.count('情愿')+text.count('愿意')+text.count('欢喜')+text.count('振奋')+text.count('乐意')+text.count('留神')+text.count('乐于')+text.count('爱')+text.count('关怀')+text.count('偏爱')+text.count('珍爱')+text.count('珍惜')+text.count('神往')+text.count('痴迷')+text.count('喜爱')+text.count('器重')+text.count('娇宠')+text.count('溺爱')+text.count('珍视')+text.count('喜欢')+text.count('动心')+text.count('挂牵')+text.count('赞赏')+text.count('爱好')+text.count('满意')+text.count('羡慕')+text.count('赏识')+text.count('热爱')+text.count('钟爱')+text.count('眷恋')+text.count('关注')+text.count('赞同')+text.count('喜欢')+text.count('想')+text.count('挂心')+text.count('挂念')+text.count('惦念')+text.count('挂虑')+text.count('怀念')+text.count('关切')+text.count('关心')+text.count('惦念')+text.count('牵挂')+text.count('怜悯')+text.count('同情')+text.count('吝惜')+text.count('可惜')+text.count('怜惜')+text.count('感谢')+text.count('感激')+text.count('在乎')+text.count('操心')+text.count('愁')+text.count('闷')+text.count('苦')+text.count('哀怨')+text.count('悲恸')+text.count('悲痛')+text.count('哀伤')+text.count('惨痛')+text.count('沉重')+text.count('感伤')+text.count('悲壮')+text.count('酸辛')+text.count('伤心')+text.count('辛酸')+text.count('悲哀')+text.count('哀痛')+text.count('沉痛')+text.count('痛心')+text.count('悲凉')+text.count('悲凄')+text.count('伤感')+text.count('悲切')+text.count('哀戚')+text.count('悲伤')+text.count('心酸')+text.count('悲怆')+text.count('无奈')+text.count('苍凉')+text.count('不好过')+text.count('抑郁')+text.count('慌')+text.count('吓人')+text.count('畏怯')+text.count('紧张')+text.count('惶恐')+text.count('慌张')+text.count('惊骇')+text.count('恐慌')+text.count('慌乱')+text.count('心虚')+text.count('惊慌')+text.count('惶惑')+text.count('惊惶')+text.count('惊惧')+text.count('惊恐')+text.count('恐惧')+text.count('心慌')+text.count('害怕')+text.count('怕')+text.count('畏惧')+text.count('发慌')+text.count('发憷')+text.count('敬')+text.count('推崇')+text.count('尊敬')+text.count('拥护')+text.count('倚重')+text.count('崇尚')+text.count('尊崇')+text.count('敬仰')+text.count('敬佩')+text.count('尊重')+text.count('敬慕')+text.count('佩服')+text.count('景仰')+text.count('敬重')+text.count('景慕')+text.count('崇敬')+text.count('瞧得起')+text.count('崇奉')+text.count('钦佩')+text.count('崇拜')+text.count('孝敬')+text.count('激动')+text.count('来劲')+text.count('炽烈')+text.count('炽热')+text.count('冲动')+text.count('狂热')+text.count('激昂')+text.count('激动')+text.count('高亢')+text.count('亢奋')+text.count('带劲')+text.count('高涨')+text.count('高昂')+text.count('投入')+text.count('兴奋')+text.count('疯狂')+text.count('狂乱')+text.count('感动')+text.count('羞')+text.count('疚')+text.count('羞涩')+text.count('羞怯')+text.count('羞惭')+text.count('负疚')+text.count('窘')+text.count('窘促')+text.count('不过意')+text.count('惭愧')+text.count('不好意思')+text.count('害羞')+text.count('害臊')+text.count('困窘')+text.count('抱歉')+text.count('抱愧')+text.count('对不起')+text.count('羞愧')+text.count('对不住')+text.count('烦')+text.count('烦躁')+text.count('烦燥')+text.count('烦')+text.count('熬心')+text.count('糟心')+text.count('烦乱')+text.count('烦心')+text.count('烦人')+text.count('烦恼')+text.count('烦杂')+text.count('腻烦')+text.count('厌倦')+text.count('厌烦')+text.count('讨厌')+text.count('头疼')+text.count('急')+text.count('浮躁')+text.count('焦虑')+text.count('焦渴')+text.count('焦急')+text.count('焦躁')+text.count('焦炙')+text.count('心浮')+text.count('心焦')+text.count('揪心')+text.count('心急')+text.count('心切')+text.count('着急')+text.count('不安')+text.count('傲')+text.count('自傲')+text.count('骄横')+text.count('骄慢')+text.count('骄矜')+text.count('骄傲')+text.count('自负')+text.count('自信')+text.count('自豪')+text.count('自满')+text.count('自大')+text.count('狂')+text.count('炫耀')+text.count('吃惊')+text.count('诧异')+text.count('吃惊')+text.count('惊疑')+text.count('愕然')+text.count('惊讶')+text.count('惊奇')+text.count('骇怪')+text.count('骇异')+text.count('惊诧')+text.count('惊愕')+text.count('震惊')+text.count('奇怪')+text.count('怒')+text.count('愤怒')+text.count('忿恨')+text.count('激愤')+text.count('生气')+text.count('愤懑')+text.count('愤慨')+text.count('忿怒')+text.count('悲愤')+text.count('窝火')+text.count('暴怒')+text.count('不平')+text.count('火')+text.count('失望')+text.count('失望')+text.count('绝望')+text.count('灰心')+text.count('丧气')+text.count('低落')+text.count('心寒')+text.count('沮丧')+text.count('消沉')+text.count('颓丧')+text.count('颓唐')+text.count('低沉')+text.count('不满')+text.count('安心')+text.count('安宁')+text.count('闲雅')+text.count('逍遥')+text.count('闲适')+text.count('怡和')+text.count('沉静')+text.count('放松')+text.count('安心')+text.count('宽心')+text.count('自在')+text.count('放心')+text.count('恨')+text.count('恶')+text.count('看不惯')+text.count('痛恨')+text.count('厌恶')+text.count('恼恨')+text.count('反对')+text.count('捣乱')+text.count('怨恨')+text.count('憎恶')+text.count('歧视')+text.count('敌视')+text.count('愤恨')+text.count('嫉')+text.count('妒嫉')+text.count('妒忌')+text.count('嫉妒')+text.count('嫉恨')+text.count('眼红')+text.count('忌恨')+text.count('忌妒')+text.count('蔑视')+text.count('蔑视')+text.count('瞧不起')+text.count('怠慢')+text.count('轻蔑')+text.count('鄙夷')+text.count('鄙薄')+text.count('鄙视')+text.count('悔')+text.count('背悔')+text.count('后悔')+text.count('懊恼')+text.count('懊悔')+text.count('悔恨')+text.count('懊丧')+text.count('委屈')+text.count('委屈')+text.count('冤')+text.count('冤枉')+text.count('无辜')+text.count('谅')+text.count('体谅')+text.count('理解')+text.count('了解')+text.count('体贴')+text.count('信任')+text.count('信赖')+text.count('相信')+text.count('信服')+text.count('疑')+text.count('过敏')+text.count('怀疑')+text.count('疑心')+text.count('疑惑')+text.count('其他')+text.count('缠绵')+text.count('自卑')+text.count('自爱')+text.count('反感')+text.count('感慨')+text.count('动摇')+text.count('消魂')+text.count('痒痒')+text.count('为难')+text.count('解恨')+text.count('迟疑')+text.count('多情')+text.count('充实')+text.count('寂寞')+text.count('遗憾')+text.count('神情')+text.count('慧黠')+text.count('狡黠')+text.count('安详')+text.count('仓皇')+text.count('阴冷')+text.count('阴沉')+text.count('犹豫')+text.count('好')+text.count('坏')+text.count('棒')+text.count('一般')+text.count('差')+text.count('得当')+text.count('标准')
    def normalized(text): 
        return raw(text) / len(text)
    return round(normalized (text) * 1000, 2)     


# In[73]:


emotion_result=[]
for corpus in sub_corpora: 
    emotion_result.append(emotion(corpus))
    
df['emotion'] = pd.Series(emotion_result)
df.to_csv(folder + 'linguistic_features.csv')


# In[76]:


#feature 41 classical syntax - words 
def classical(text_type):
    def raw(text_type): 
        return text_type.count('备受')+text_type.count('言必称')+text_type.count('并存')+text_type.count('不得而')+text_type.count('抑且')+text_type.count('不特')+text_type.count('不外乎')+text_type.count('且')+text_type.count('不外乎')+text_type.count('不相')+text_type.count('中不乏')+text_type.count('不啻')+text_type.count('称之为')+text_type.count('称之')+text_type.count('充其量')+text_type.count('出于')+text_type.count('处于')+text_type.count('不次于')+text_type.count('从属于')+text_type.count('从中')+text_type.count('得自于')+text_type.count('得力于')+text_type.count('予以')+text_type.count('给予')+text_type.count('加以')+text_type.count('深具')+text_type.count('之能事')+text_type.count('发轫于')+text_type.count('凡此')+text_type.count('大抵')+text_type.count('凡')+text_type.count('所能及')+text_type.count('所可比')+text_type.count('非但')+text_type.count('庶可')+text_type.count('之故')+text_type.count('工于')+text_type.count('苟')+text_type.count('顾')+text_type.count('广为')+text_type.count('果')+text_type.count('核以')+text_type.count('何其')+text_type.count('或可')+text_type.count('跻身')+text_type.count('跻于')+text_type.count('不日即')+text_type.count('藉')+text_type.count('之大成')+text_type.count('再加')+text_type.count('略加')+text_type.count('详加')+text_type.count('以俱来')+text_type.count('见胜')+text_type.count('见长')+text_type.count('兼')+text_type.count('渐次')+text_type.count('化')+text_type.count('混同于')+text_type.count('归之于')+text_type.count('推广到')+text_type.count('名之为')+text_type.count('引为')+text_type.count('矣')+text_type.count('较')+text_type.count('借以')+text_type.count('尽其')+text_type.count('略陈己见')+text_type.count('而言')+text_type.count('而论')+text_type.count('决定于')+text_type.count('之先河')+text_type.count('苦不能')+text_type.count('莫不是')+text_type.count('乃')+text_type.count('泥于')+text_type.count('偏于')+text_type.count('颇有')+text_type.count('岂不')+text_type.count('岂可')+text_type.count('乎')+text_type.count('哉')+text_type.count('起源于')+text_type.count('何况')+text_type.count('切于')+text_type.count('取信于')+text_type.count('如')+text_type.count('则')+text_type.count('若')+text_type.count('岂')+text_type.count('舍')+text_type.count('甚于')+text_type.count('时年')+text_type.count('时值')+text_type.count('使之')+text_type.count('有别于')+text_type.count('倍加')+text_type.count('所在')+text_type.count('示人以')+text_type.count('随致')+text_type.count('之所以')+text_type.count('所以然')+text_type.count('所verb者')+text_type.count('无所')+text_type.count('有所')+text_type.count('皆指')+text_type.count('所引致')+text_type.count('罕为')+text_type.count('鲜为')+text_type.count('多为')+text_type.count('唯')+text_type.count('尚未')+text_type.count('无一不')+text_type.count('无不能')+text_type.count('无从')+text_type.count('可见')+text_type.count('毋宁')+text_type.count('无宁')+text_type.count('务')+text_type.count('系于')+text_type.count('仅限于')+text_type.count('方能')+text_type.count('需')+text_type.count('须')+text_type.count('许之为')+text_type.count('一改')+text_type.count('一变')+text_type.count('与否')+text_type.count('业已')+text_type.count('不以为然')+text_type.count('为能')+text_type.count('为多')+text_type.count('为最')+text_type.count('以期')+text_type.count('不宜')+text_type.count('宜于')+text_type.count('异于')+text_type.count('益见')+text_type.count('抑或')+text_type.count('故')+text_type.count('之便')+text_type.count('应推')+text_type.count('着手')+text_type.count('着眼')+text_type.count('可证')+text_type.count('可知')+text_type.count('可见')+text_type.count('而成')+text_type.count('有不')+text_type.count('有所')+text_type.count('有待于')+text_type.count('有赖于')+text_type.count('有助于')+text_type.count('有进于')+text_type.count('之分')+text_type.count('之别')+text_type.count('多有')+text_type.count('囿于')+text_type.count('与之')+text_type.count('同/共')+text_type.count('同为')+text_type.count('欲')+text_type.count('必')+text_type.count('喻之')+text_type.count('曰')+text_type.count('之际')+text_type.count('已然')+text_type.count('在于')+text_type.count('则')+text_type.count('者')+text_type.count('即是')+text_type.count('皆是')+text_type.count('云者')+text_type.count('者有之')+text_type.count('首属')+text_type.count('首推')+text_type.count('莫过于')+text_type.count('之')+text_type.count('之于')+text_type.count('置身于')+text_type.count('转而')+text_type.count('自')+text_type.count('自况')+text_type.count('自命')+text_type.count('自诩')+text_type.count('自认')+text_type.count('自居')+text_type.count('自许')+text_type.count('以降')+text_type.count('足以')
    def normalized(text_type): 
        return raw(text_type) / len(text_type)
    return round(normalized (text_type) * 1000, 2) 


# In[77]:


classical_result=[]
for corpus in sub_corpora: 
    classical_result.append(classical(corpus))
    
df['classical_syntax'] = pd.Series(classical_result)
df.to_csv(folder + 'linguistic_features.csv')


# In[78]:


#feature 42 disyllabic words 
def disyllabic(text_type):
    def raw(text_type): 
        return text_type.count('购买')+text_type.count('具有')+text_type.count('在于')+text_type.count('寻找')+text_type.count('获得')+text_type.count('询问')+text_type.count('进入')+text_type.count('等候')+text_type.count('安定')+text_type.count('安装')+text_type.count('办理')+text_type.count('保持')+text_type.count('保留')+text_type.count('保卫')+text_type.count('保障')+text_type.count('报道')+text_type.count('暴露')+text_type.count('爆发')+text_type.count('被迫')+text_type.count('必然')+text_type.count('必修')+text_type.count('必要')+text_type.count('避免')+text_type.count('编制')+text_type.count('变动')+text_type.count('变革')+text_type.count('辩论')+text_type.count('表达')+text_type.count('表示')+text_type.count('表演')+text_type.count('并肩')+text_type.count('补习')+text_type.count('不断')+text_type.count('不时')+text_type.count('不住')+text_type.count('布置')+text_type.count('采取')+text_type.count('采用')+text_type.count('参考')+text_type.count('测量')+text_type.count('测试')+text_type.count('测验')+text_type.count('颤动')+text_type.count('抄写')+text_type.count('陈列')+text_type.count('成立')+text_type.count('成为')+text_type.count('承担')+text_type.count('承认')+text_type.count('持枪')+text_type.count('充分')+text_type.count('充满')+text_type.count('充实')+text_type.count('仇恨')+text_type.count('出版')+text_type.count('处于')+text_type.count('处处')+text_type.count('传播')+text_type.count('传达')+text_type.count('创立')+text_type.count('次要')+text_type.count('匆忙')+text_type.count('从容')+text_type.count('从事')+text_type.count('促进')+text_type.count('摧毁')+text_type.count('达成')+text_type.count('达到')+text_type.count('打扫')+text_type.count('大力')+text_type.count('大有')+text_type.count('担任')+text_type.count('导致')+text_type.count('到达')+text_type.count('等待')+text_type.count('等候')+text_type.count('奠定')+text_type.count('雕刻')+text_type.count('调查')+text_type.count('动员')+text_type.count('独自')+text_type.count('端正')+text_type.count('锻炼')+text_type.count('夺取')+text_type.count('发表')+text_type.count('发动')+text_type.count('发挥')+text_type.count('发射')+text_type.count('发生')+text_type.count('发行')+text_type.count('发扬')+text_type.count('发展')+text_type.count('反抗')+text_type.count('防守')+text_type.count('防御')+text_type.count('防止')+text_type.count('防治')+text_type.count('非法')+text_type.count('废除')+text_type.count('粉碎')+text_type.count('丰富')+text_type.count('封锁')+text_type.count('符合')+text_type.count('负担')+text_type.count('负责')+text_type.count('复述')+text_type.count('复习')+text_type.count('复印')+text_type.count('复杂')+text_type.count('复制')+text_type.count('富有')+text_type.count('改编')+text_type.count('改革')+text_type.count('改进')+text_type.count('改良')+text_type.count('改善')+text_type.count('改正')+text_type.count('干涉')+text_type.count('敢于')+text_type.count('高大')+text_type.count('高度')+text_type.count('高速')+text_type.count('格外')+text_type.count('给以')+text_type.count('更加')+text_type.count('公开')+text_type.count('公然')+text_type.count('巩固')+text_type.count('贡献')+text_type.count('共同')+text_type.count('构成')+text_type.count('购买')+text_type.count('观测')+text_type.count('观察')+text_type.count('观看')+text_type.count('贯彻')+text_type.count('灌溉')+text_type.count('光临')+text_type.count('规划')+text_type.count('合成')+text_type.count('合法')+text_type.count('宏伟')+text_type.count('缓和')+text_type.count('缓缓')+text_type.count('回答')+text_type.count('汇报')+text_type.count('混淆')+text_type.count('活跃')+text_type.count('获得')+text_type.count('基本')+text_type.count('集合')+text_type.count('集中')+text_type.count('极为')+text_type.count('即将')+text_type.count('计划')+text_type.count('记载')+text_type.count('继承')+text_type.count('加工')+text_type.count('加紧')+text_type.count('加速')+text_type.count('加以')+text_type.count('驾驶')+text_type.count('歼灭')+text_type.count('坚定')+text_type.count('减轻')+text_type.count('检验')+text_type.count('简直')+text_type.count('建立')+text_type.count('建造')+text_type.count('建筑')+text_type.count('交换')+text_type.count('交流')+text_type.count('结束')+text_type.count('竭力')+text_type.count('解决')+text_type.count('解释')+text_type.count('紧急')+text_type.count('紧密')+text_type.count('谨慎')+text_type.count('进军')+text_type.count('进攻')+text_type.count('进入')+text_type.count('进行')+text_type.count('尽力')+text_type.count('禁止')+text_type.count('精彩')+text_type.count('进过')+text_type.count('经历')+text_type.count('经受')+text_type.count('经营')+text_type.count('竞争')+text_type.count('竟然')+text_type.count('纠正')+text_type.count('举办')+text_type.count('举行')+text_type.count('具备')+text_type.count('具体')+text_type.count('具有')+text_type.count('开办')+text_type.count('开动')+text_type.count('开发')+text_type.count('开明')+text_type.count('开辟')+text_type.count('开枪')+text_type.count('开设')+text_type.count('开展')+text_type.count('抗议')+text_type.count('克服')+text_type.count('刻苦')+text_type.count('空前')+text_type.count('扩大')+text_type.count('来自')+text_type.count('滥用')+text_type.count('朗读')+text_type.count('力求')+text_type.count('力争')+text_type.count('连接')+text_type.count('列举')+text_type.count('流传')+text_type.count('垄断')+text_type.count('笼罩')+text_type.count('轮流')+text_type.count('掠夺')+text_type.count('满腔')+text_type.count('盲目')+text_type.count('猛烈')+text_type.count('猛然')+text_type.count('梦想')+text_type.count('勉强')+text_type.count('面临')+text_type.count('明明')+text_type.count('明确')+text_type.count('难以')+text_type.count('扭转')+text_type.count('拍摄')+text_type.count('排列')+text_type.count('攀登')+text_type.count('炮打')+text_type.count('赔偿')+text_type.count('评价')+text_type.count('评论')+text_type.count('赔偿')+text_type.count('评价')+text_type.count('评论')+text_type.count('破坏')+text_type.count('普遍')+text_type.count('普及')+text_type.count('起源')+text_type.count('签订')+text_type.count('强调')+text_type.count('抢夺')+text_type.count('切实')+text_type.count('侵略')+text_type.count('侵入')+text_type.count('轻易')+text_type.count('取得')+text_type.count('全部')+text_type.count('全面')+text_type.count('燃烧')+text_type.count('热爱')+text_type.count('忍受')+text_type.count('仍旧')+text_type.count('日益')+text_type.count('如同')+text_type.count('散布')+text_type.count('丧失')+text_type.count('设法')+text_type.count('设立')+text_type.count('实施')+text_type.count('实现')+text_type.count('实行')+text_type.count('实验')+text_type.count('适合')+text_type.count('试验')+text_type.count('收集')+text_type.count('收缩')+text_type.count('树立')+text_type.count('束缚')+text_type.count('思考')+text_type.count('思念')+text_type.count('思索')+text_type.count('丝毫')+text_type.count('四处')+text_type.count('饲养')+text_type.count('损害')+text_type.count('损坏')+text_type.count('损失')+text_type.count('缩短')+text_type.count('缩小')+text_type.count('贪图')+text_type.count('谈论')+text_type.count('探索')+text_type.count('逃避')+text_type.count('提倡')+text_type.count('提供')+text_type.count('提前')+text_type.count('体现')+text_type.count('调节')+text_type.count('调整')+text_type.count('停止')+text_type.count('统一')+text_type.count('突破')+text_type.count('推迟')+text_type.count('推动')+text_type.count('推进')+text_type.count('脱离')+text_type.count('歪曲')+text_type.count('完善')+text_type.count('万分')+text_type.count('万万')+text_type.count('危害')+text_type.count('违背')+text_type.count('违反')+text_type.count('维持')+text_type.count('维护')+text_type.count('围绕')+text_type.count('伟大')+text_type.count('位于')+text_type.count('污染')+text_type.count('无比')+text_type.count('无法')+text_type.count('无穷')+text_type.count('无限')+text_type.count('武装')+text_type.count('吸取')+text_type.count('袭击')+text_type.count('喜爱')+text_type.count('显示')+text_type.count('限制')+text_type.count('陷入')+text_type.count('相互')+text_type.count('详细')+text_type.count('响应')+text_type.count('享受')+text_type.count('象征')+text_type.count('消除')+text_type.count('消耗')+text_type.count('小心')+text_type.count('写作')+text_type.count('辛勤')+text_type.count('修改')+text_type.count('修正')+text_type.count('修筑')+text_type.count('选择')+text_type.count('严格')+text_type.count('严禁')+text_type.count('严厉')+text_type.count('严密')+text_type.count('严肃')+text_type.count('研制')+text_type.count('延长')+text_type.count('掩盖')+text_type.count('养成')+text_type.count('一经')+text_type.count('依法')+text_type.count('依旧')+text_type.count('依然')+text_type.count('抑制')+text_type.count('应用')+text_type.count('永远')+text_type.count('踊跃')+text_type.count('游览')+text_type.count('予以')+text_type.count('遇到')+text_type.count('预防')+text_type.count('预习')+text_type.count('阅读')+text_type.count('运用')+text_type.count('再三')+text_type.count('遭到')+text_type.count('遭受')+text_type.count('遭遇')+text_type.count('增加')+text_type.count('增进')+text_type.count('增强')+text_type.count('占领')+text_type.count('占有')+text_type.count('战胜')+text_type.count('掌握')+text_type.count('照例')+text_type.count('镇压')+text_type.count('征服')+text_type.count('征求')+text_type.count('争夺')+text_type.count('争论')+text_type.count('整顿')+text_type.count('证明')+text_type.count('直到')+text_type.count('执行')+text_type.count('制定')+text_type.count('制订')+text_type.count('制造')+text_type.count('治疗')+text_type.count('中断')+text_type.count('重大')+text_type.count('专心')+text_type.count('转入')+text_type.count('转移')+text_type.count('装备')+text_type.count('装饰')+text_type.count('追求')+text_type.count('自学')+text_type.count('综合')+text_type.count('总结')+text_type.count('阻止')+text_type.count('钻研')+text_type.count('遵守')+text_type.count('左右')
    def normalized(text_type): 
        return raw(text_type) / len(text_type)
    return round(normalized (text_type) * 1000, 2)      


# In[79]:


disyllabic_result=[]
for corpus in sub_corpora: 
    disyllabic_result.append(disyllabic(corpus))
    
df['disyllabic_words'] = pd.Series(disyllabic_result)
df.to_csv(folder + 'linguistic_features.csv')


# In[80]:


#feature 60 HSK core vocabulary level 1 150 words 

HSK1=['爱', '八', '爸爸', '杯子', '北京', '本', '不', '不客气', '菜', '茶', '吃', '出租车', '打电话', '大', '的', '点', '电脑', '电视', '电影', '东西', '都', '读', '对不起', '多', '多少', '儿子', '二', '饭店', '飞机', '分钟', '高兴', '个', '工作', '狗', '汉语', '好', '号', '喝', '和', '很', '后面', '回', '会', '几', '家', '叫', '今天', '九', '开', '看', '看见', '块', '来', '老师', '了', '冷', '里', '六', '妈妈', '吗', '买', '猫', '没关系', '没有', '米饭', '名字', '明天', '哪', '哪儿', '那', '呢', '能', '你', '年', '女儿', '朋友', '漂亮', '苹果', '七', '前面', '钱', '请', '去', '热', '人', '认识', '三', '商店', '上', '上午', '少', '谁', '什么', '十', '时候', '是', '书', '水', '水果', '睡觉', '说', '四', '岁', '他', '她', '太', '天气', '听', '同学', '喂', '我', '我们', '五', '喜欢', '下', '下午', '下雨', '先生', '现在', '想', '小', '小姐', '些', '写', '谢谢', '星期', '学生', '学习', '学校', '一', '一点儿', '衣服', '医生', '医院', '椅子', '有', '月', '再见', '在', '怎么', '怎么样', '这', '中国', '中午', '住', '桌子', '字', '昨天', '坐', '做']

def hsk1(text_type):
    def raw(text_type): 
        return len([x for x in text_type if x in HSK1])
    def normalized(text_type): 
        return raw(text_type) / len(text_type)
    return round(normalized (text_type) * 1000, 2) 


# In[81]:


hsk1_result=[]
for corpus in sub_corpora: 
    hsk1_result.append(hsk1(corpus))
    
df['HSK_1'] = pd.Series(hsk1_result)
df.to_csv(folder + 'linguistic_features.csv')


# In[106]:


#for corpus in sub_corpora: 
   # print (hsk1(corpus))


# In[82]:


HSK3=['阿姨', '啊', '矮', '爱', '爱好', '安静', '把', '吧', '白', '百', '班', '搬', '办法', '办公室', '半', '帮忙', '帮助', '包', '饱', '报纸', '北方', '被', '鼻子', '比', '比较', '比赛', '笔记本', '必须', '变化', '别', '别人', '宾馆', '冰箱', '不但', '而且', '菜单', '参加', '草', '层', '差', '长', '唱歌', '超市', '衬衫', '成绩', '城市', '迟到', '出', '除了', '穿', '船', '春', '词典', '次', '聪明', '从', '错', '打篮球', '打扫', '打算', '大家', '带', '担心', '蛋糕', '当然', '到', '地', '得', '灯', '等', '地方', '地铁', '地图', '弟弟', '第一', '电梯', '电子邮件', '东', '冬', '懂', '动物', '短', '段', '锻炼', '对', '多么', '饿', '耳朵', '发', '发烧', '发现', '方便', '房间', '放', '放心', '非常', '分', '服务员', '附近', '复习', '干净', '感冒', '感兴趣', '刚才', '高', '告诉', '哥哥', '个子', '给', '根据', '跟', '更', '公共汽车', '公斤', '公司', '公园', '故事', '刮风', '关', '关系', '关心', '关于', '贵', '国家', '过', '过去', '还', '还是', '孩子', '害怕', '好吃', '黑', '黑板', '红', '后来', '护照', '花', '画', '坏', '欢迎', '环境', '换', '黄河', '回答', '会议', '火车站', '或者', '几乎', '机场', '机会', '鸡蛋', '极', '记得', '季节', '检查', '简单', '见面', '件', '健康', '讲', '教', '角', '脚', '教室', '接', '街道', '节目', '节日', '结婚', '结束', '姐姐', '解决', '介绍', '借', '进', '近', '经常', '经过', '经理', '久', '旧', '就', '句子', '决定', '觉得', '咖啡', '开始', '考试', '可爱', '可能', '可以', '渴', '刻', '客人', '课', '空调', '口', '哭', '裤子', '快', '快乐', '筷子', '蓝', '老', '累', '离', '离开', '礼物', '历史', '脸', '练习', '两', '辆', '聊天', '了解', '邻居', '零', '留学', '楼', '路', '旅游', '绿', '马', '马上', '卖', '满意', '慢', '忙', '帽子', '每', '妹妹', '门', '米', '面包', '面条', '明白', '拿', '奶奶', '男', '南', '难', '难过', '年级', '年轻', '鸟', '您', '牛奶', '努力', '女', '爬山', '盘子', '旁边', '胖', '跑步', '皮鞋', '啤酒', '便宜', '票', '瓶子', '妻子', '其实', '其他', '奇怪', '骑', '起床', '起飞', '起来', '千', '铅笔', '清楚', '晴', '请假', '秋', '去年', '裙子', '然后', '让', '热情', '认为', '认真', '日', '容易', '如果', '伞', '上班', '上网', '谁', '身体', '生病', '生气', '生日', '声音', '时间', '世界', '事情', '试', '手表', '手机', '瘦', '叔叔', '舒服', '树', '数学', '刷牙', '双', '水平', '说话', '司机', '送', '虽然', '但是', '它', '她', '太阳', '特别', '疼', '踢足球', '提高', '题', '体育', '甜', '条', '跳舞', '同事', '同意', '头发', '突然', '图书馆', '腿', '外', '完', '完成', '玩', '晚上', '碗', '万', '往', '忘记', '为', '为了', '为什么', '位', '文化', '问', '问题', '西', '西瓜', '希望', '习惯', '洗', '洗手间', '洗澡', '夏', '先', '相信', '香蕉', '向', '像', '小时', '小心', '校长', '笑', '新', '新闻', '新鲜', '信用卡', '行李箱', '姓', '熊猫', '休息', '需要', '选择', '雪', '颜色', '眼睛', '羊肉', '要求', '药', '要', '爷爷', '也', '一般', '一边', '一定', '一共', '一会儿', '一起', '一下', '一样', '一直', '已经', '以前', '意思', '因为', '所以', '阴', '音乐', '银行', '饮料', '应该', '影响', '用', '游戏', '游泳', '有名', '又', '右边', '鱼', '遇到', '元', '远', '愿意', '月亮', '越', '运动', '再', '早上', '站', '张', '丈夫', '着急', '找', '照顾', '照片', '照相机', '着', '真', '正在', '只', '只有', '才', '中间', '中文', '终于', '种', '重要', '周末', '主要', '注意', '准备', '自己', '自行车', '总是', '走', '嘴', '最', '最后', '最近', '左边', '作业']


# In[83]:


#feature 61 HSK core vocabulary level 3 (150-600), 450 words 
def hsk3(text_type):
    def raw(text_type): 
        return len([x for x in text_type if x in HSK3])
    def normalized(text_type): 
        return raw(text_type) / len(text_type)
    return round(normalized (text_type) * 1000, 2) 


# In[84]:


hsk3_result=[]
for corpus in sub_corpora: 
    hsk3_result.append(hsk3(corpus))
    
df['HSK_3'] = pd.Series(hsk3_result)
df.to_csv(folder + 'linguistic_features.csv')


# In[85]:


HSK6=['哎', '唉', '挨', '癌症', '爱不释手', '爱戴', '爱护', '爱情', '爱惜', '爱心', '暧昧', '安宁', '安排', '安全', '安慰', '安详', '安置', '安装', '岸', '按摩', '按时', '按照', '案件', '案例', '暗', '暗示', '昂贵', '凹凸', '熬', '熬夜', '奥秘', '巴不得', '巴结', '扒', '疤', '拔苗助长', '把关', '把手', '把握', '罢工', '霸道', '掰', '百分之', '摆', '摆脱', '败坏', '拜访', '拜年', '拜托', '颁布', '颁发', '斑', '版本', '办理', '半途而废', '扮演', '伴侣', '伴随', '绑架', '榜样', '棒', '傍晚', '磅', '包庇', '包袱', '包裹', '包含', '包括', '包围', '包装', '包子', '薄', '饱和', '饱经沧桑', '宝贝', '宝贵', '保持', '保存', '保管', '保护', '保留', '保密', '保姆', '保守', '保卫', '保险', '保养', '保障', '保证', '保重', '报仇', '报酬', '报答', '报到', '报道', '报复', '报告', '报警', '报名', '报社', '报销', '抱', '抱负', '抱歉', '抱怨', '暴力', '暴露', '曝光', '爆发', '爆炸', '卑鄙', '背', '悲哀', '悲惨', '悲观', '北极', '贝壳', '备份', '备忘录', '背景', '背叛', '背诵', '倍', '被动', '被告', '被子', '奔波', '奔驰', '本科', '本来', '本领', '本能', '本钱', '本人', '本身', '本事', '本质', '笨', '笨拙', '崩溃', '甭', '迸发', '蹦', '逼迫', '鼻涕', '比方', '比例', '比如', '比喻', '比重', '彼此', '鄙视', '必然', '必要', '毕竟', '毕业', '闭塞', '弊病', '弊端', '避免', '臂', '边疆', '边界', '边境', '边缘', '编辑', '编织', '鞭策', '鞭炮', '贬低', '贬义', '扁', '变故', '变迁', '变质', '便', '便利', '便条', '便于', '遍', '遍布', '辨认', '辩护', '辩解', '辩论', '辩证', '辫子', '标本', '标点', '标记', '标题', '标志', '标准', '表达', '表格', '表决', '表面', '表明', '表情', '表示', '表态', '表现', '表演', '表扬', '表彰', '憋', '别墅', '别致', '别扭', '濒临', '冰雹', '冰激凌', '丙', '饼干', '并非', '并列', '并且', '病毒', '拨', '波浪', '波涛', '玻璃', '剥削', '播放', '播种', '伯母', '脖子', '博大精深', '博览会', '博士', '博物馆', '搏斗', '薄弱', '补偿', '补充', '补救', '补贴', '捕捉', '哺乳', '不安', '不得不', '不得了', '不得已', '不断', '不妨', '不敢当', '不顾', '不管', '不过', '不见得', '不禁', '不仅', '不堪', '不可思议', '不愧', '不料', '不免', '不耐烦', '不然', '不如', '不时', '不惜', '不相上下', '不像话', '不屑一顾', '不言而喻', '不要紧', '不由得', '不择手段', '不止', '不足', '布', '布告', '布局', '布置', '步伐', '步骤', '部分', '部门', '部署', '部位', '擦', '猜', '才干', '材料', '财产', '财富', '财务', '财政', '裁缝', '裁判', '裁员', '采访', '采购', '采集', '采纳', '采取', '彩虹', '彩票', '踩', '参观', '参考', '参谋', '参与', '参照', '餐厅', '残疾', '残酷', '残留', '残忍', '惭愧', '灿烂', '仓促', '仓库', '苍白', '舱', '操场', '操劳', '操练', '操心', '操纵', '操作', '嘈杂', '草案', '草率', '册', '厕所', '侧面', '测量', '测验', '策划', '策略', '层出不穷', '层次', '曾经', '叉子', '差别', '差距', '插', '插座', '查获', '岔', '刹那', '诧异', '差不多', '拆', '柴油', '搀', '馋', '缠绕', '产品', '产生', '产业', '阐述', '颤抖', '昌盛', '长城', '长江', '长途', '尝', '尝试', '常识', '偿还', '场', '场合', '场面', '场所', '敞开', '畅通', '畅销', '倡导', '倡议', '抄', '钞票', '超过', '超级', '超越', '巢穴', '朝', '朝代', '嘲笑', '潮流', '潮湿', '吵', '吵架', '炒', '车库', '车厢', '彻底', '撤退', '撤销', '沉淀', '沉闷', '沉默', '沉思', '沉重', '沉着', '陈旧', '陈列', '陈述', '衬托', '称心如意', '趁', '称', '称号', '称呼', '称赞', '成本', '成分', '成功', '成果', '成交', '成就', '成立', '成人', '成熟', '成天', '成为', '成效', '成心', '成语', '成员', '成长', '呈现', '诚恳', '诚实', '诚挚', '承办', '承包', '承担', '承诺', '承认', '承受', '城堡', '乘', '乘坐', '盛', '程度', '程序', '惩罚', '澄清', '橙', '秤', '吃惊', '吃苦', '吃亏', '吃力', '池塘', '迟钝', '迟缓', '迟疑', '迟早', '持久', '持续', '尺子', '赤道', '赤字', '翅膀', '冲', '冲动', '冲击', '冲突', '充当', '充电器', '充分', '充满', '充沛', '充实', '充足', '重叠', '重复', '重新', '崇拜', '崇高', '崇敬', '宠物', '抽屉', '抽象', '抽烟', '稠密', '筹备', '丑', '丑恶', '臭', '出版', '出差', '出发', '出口', '出路', '出卖', '出色', '出身', '出神', '出生', '出示', '出息', '出席', '出现', '初步', '初级', '除', '除非', '除夕', '厨房', '处分', '处境', '处理', '处置', '储备', '储存', '储蓄', '触犯', '川流不息', '穿越', '传播', '传达', '传单', '传染', '传授', '传说', '传统', '传真', '船舶', '喘气', '串', '窗户', '窗帘', '床单', '闯', '创立', '创新', '创业', '创造', '创作', '吹', '吹牛', '吹捧', '炊烟', '垂直', '锤', '纯粹', '纯洁', '词汇', '词语', '辞职', '慈善', '慈祥', '磁带', '雌雄', '此外', '次品', '次序', '次要', '伺候', '刺', '刺激', '匆忙', '从此', '从而', '从来', '从前', '从容', '从事', '丛', '凑合', '粗糙', '粗鲁', '粗心', '促进', '促使', '醋', '窜', '催', '摧残', '脆弱', '存', '存在', '搓', '磋商', '挫折', '措施', '错误', '搭', '搭档', '搭配', '答应', '达成', '达到', '答案', '答辩', '答复', '打扮', '打包', '打工', '打官司', '打击', '打架', '打交道', '打量', '打猎', '打喷嚏', '打扰', '打听', '打印', '打仗', '打招呼', '打折', '打针', '大不了', '大臣', '大方', '大概', '大伙儿', '大厦', '大使馆', '大肆', '大体', '大象', '大型', '大意', '大约', '大致', '呆', '歹徒', '大夫', '代表', '代价', '代理', '代替', '带领', '贷款', '待遇', '怠慢', '逮捕', '戴', '担保', '担任', '单纯', '单调', '单独', '单位', '单元', '耽误', '胆怯', '胆小鬼', '诞辰', '诞生', '淡', '淡季', '淡水', '蛋白质', '当', '当场', '当初', '当代', '当地', '当面', '当前', '当时', '当事人', '当务之急', '当心', '当选', '挡', '党', '档案', '档次', '刀', '导弹', '导航', '导向', '导演', '导游', '导致', '岛屿', '捣乱', '倒闭', '倒霉', '到处', '到达', '到底', '倒', '盗窃', '道德', '道理', '道歉', '稻谷', '得不偿失', '得力', '得天独厚', '得意', '得罪', '灯笼', '登机牌', '登记', '登陆', '登录', '蹬', '等待', '等候', '等级', '等于', '瞪', '低', '堤坝', '滴', '的确', '敌人', '敌视', '抵达', '抵抗', '抵制', '底', '地步', '地道', '地点', '地理', '地球', '地区', '地势', '地毯', '地位', '地震', '地址', '地质', '递', '递增', '颠簸', '颠倒', '典礼', '典型', '点心', '点缀', '电池', '电台', '电源', '垫', '惦记', '奠定', '叼', '雕刻', '雕塑', '吊', '钓', '调查', '调动', '掉', '跌', '丁', '叮嘱', '盯', '顶', '定期', '定义', '丢', '丢人', '丢三落四', '东道主', '东张西望', '董事长', '动荡', '动画片', '动机', '动静', '动力', '动脉', '动身', '动手', '动态', '动员', '动作', '冻', '冻结', '栋', '洞', '兜', '陡峭', '斗争', '豆腐', '逗', '督促', '毒品', '独裁', '独立', '独特', '堵车', '堵塞', '赌博', '杜绝', '肚子', '度过', '端', '端午节', '端正', '短促', '短信', '断', '断定', '断绝', '堆', '堆积', '队伍', '对比', '对策', '对称', '对待', '对方', '对付', '对话', '对抗', '对立', '对联', '对面', '对手', '对象', '对应', '对于', '对照', '兑换', '兑现', '吨', '蹲', '顿', '顿时', '多亏', '多余', '多元化', '哆嗦', '朵', '躲藏', '堕落', '额外', '恶心', '恶化', '恶劣', '遏制', '恩怨', '儿童', '而', '而已', '耳环', '二氧化碳', '发表', '发布', '发财', '发愁', '发达', '发呆', '发动', '发抖', '发挥', '发觉', '发明', '发票', '发射', '发生', '发誓', '发行', '发言', '发炎', '发扬', '发育', '发展', '罚款', '法律', '法人', '法院', '番', '翻', '翻译', '凡是', '烦恼', '繁华', '繁忙', '繁荣', '繁体字', '繁殖', '反驳', '反常', '反对', '反而', '反复', '反感', '反抗', '反馈', '反面', '反射', '反思', '反问', '反应', '反映', '反正', '反之', '泛滥', '范畴', '范围', '贩卖', '方', '方案', '方法', '方面', '方式', '方位', '方向', '方言', '方圆', '方针', '防守', '防御', '防止', '防治', '妨碍', '房东', '仿佛', '访问', '纺织', '放大', '放弃', '放射', '放暑假', '放松', '飞禽走兽', '飞翔', '飞跃', '非', '非法', '肥沃', '肥皂', '诽谤', '肺', '废除', '废话', '废寝忘食', '废墟', '沸腾', '分辨', '分别', '分布', '分寸', '分红', '分解', '分裂', '分泌', '分明', '分配', '分歧', '分散', '分手', '分析', '吩咐', '纷纷', '坟墓', '粉末', '粉色', '粉碎', '分量', '份', '奋斗', '愤怒', '丰富', '丰满', '丰盛', '丰收', '风暴', '风度', '风格', '风光', '风景', '风气', '风趣', '风俗', '风土人情', '风味', '风险', '封闭', '封建', '封锁', '疯狂', '锋利', '逢', '讽刺', '奉献', '否定', '否决', '否认', '否则', '夫妇', '夫人', '敷衍', '扶', '服从', '服气', '服装', '俘虏', '符号', '符合', '幅', '幅度', '辐射', '福利', '福气', '抚摸', '抚养', '俯视', '辅导', '辅助', '腐败', '腐烂', '腐蚀', '腐朽', '父亲', '付款', '负担', '负责', '妇女', '附和', '附件', '附属', '复活', '复兴', '复印', '复杂', '复制', '副', '赋予', '富', '富裕', '腹泻', '覆盖', '改变', '改革', '改进', '改良', '改善', '改正', '钙', '盖', '盖章', '概括', '概念', '干杯', '干脆', '干旱', '干扰', '干涉', '干预', '干燥', '尴尬', '赶', '赶紧', '赶快', '敢', '感动', '感激', '感觉', '感慨', '感情', '感染', '感受', '感想', '感谢', '干', '干活儿', '干劲', '刚', '纲领', '钢铁', '岗位', '港口', '港湾', '杠杆', '高超', '高潮', '高档', '高峰', '高级', '高明', '高尚', '高速公路', '高涨', '搞', '稿件', '告别', '告辞', '告诫', '疙瘩', '胳膊', '鸽子', '搁', '割', '歌颂', '革命', '格局', '格式', '格外', '隔壁', '隔阂', '隔离', '个别', '个人', '个体', '个性', '各', '各抒己见', '各自', '根', '根本', '根深蒂固', '根源', '跟前', '跟随', '跟踪', '更新', '更正', '耕地', '工厂', '工程师', '工具', '工人', '工业', '工艺品', '工资', '公安局', '公布', '公道', '公告', '公关', '公开', '公里', '公民', '公平', '公然', '公认', '公式', '公务', '公寓', '公元', '公正', '公证', '公主', '功夫', '功劳', '功能', '功效', '攻击', '攻克', '供不应求', '供给', '宫殿', '恭敬', '恭喜', '巩固', '共和国', '共计', '共鸣', '共同', '贡献', '勾结', '沟通', '钩子', '构成', '构思', '购物', '够', '估计', '孤独', '孤立', '姑姑', '姑娘', '姑且', '辜负', '古代', '古典', '古董', '古怪', '股东', '股份', '股票', '骨干', '骨头', '鼓动', '鼓励', '鼓舞', '鼓掌', '固定', '固然', '固体', '固有', '固执', '故乡', '故意', '故障', '顾客', '顾虑', '顾问', '雇佣', '挂', '挂号', '乖', '拐弯', '拐杖', '怪不得', '关闭', '关怀', '关键', '关照', '观察', '观点', '观光', '观念', '观众', '官', '官方', '管理', '管辖', '管子', '贯彻', '冠军', '惯例', '灌溉', '罐', '光', '光彩', '光滑', '光辉', '光临', '光芒', '光明', '光盘', '光荣', '广播', '广场', '广大', '广泛', '广告', '广阔', '逛', '归根到底', '归还', '归纳', '规定', '规范', '规格', '规划', '规矩', '规律', '规模', '规则', '规章', '轨道', '柜台', '贵族', '跪', '滚', '棍棒', '锅', '国防', '国籍', '国际', '国庆节', '国王', '国务院', '果断', '果然', '果实', '果汁', '过程', '过度', '过渡', '过分', '过奖', '过滤', '过敏', '过期', '过失', '过问', '过瘾', '过于', '哈', '嗨', '海拔', '海滨', '海关', '海鲜', '海洋', '害羞', '含糊', '含义', '寒假', '寒暄', '罕见', '喊', '汗', '捍卫', '行列', '行业', '航班', '航空', '航天', '航行', '毫米', '毫无', '豪华', '豪迈', '好处', '好像', '号码', '号召', '好客', '好奇', '耗费', '呵', '合并', '合成', '合法', '合格', '合伙', '合理', '合适', '合算', '合同', '合影', '合作', '何必', '何况', '和蔼', '和解', '和睦', '和平', '和气', '和谐', '核心', '盒子', '嘿', '痕迹', '狠心', '恨', '恨不得', '横', '哼', '轰动', '烘', '宏观', '宏伟', '洪水', '哄', '喉咙', '猴子', '吼', '后背', '后代', '后顾之忧', '后果', '后悔', '后勤', '厚', '候选', '呼唤', '呼吸', '呼啸', '呼吁', '忽略', '忽然', '忽视', '胡乱', '胡说', '胡同', '胡须', '壶', '湖泊', '蝴蝶', '糊涂', '互联网', '互相', '护士', '花瓣', '花蕾', '花生', '划', '华丽', '华侨', '华裔', '滑', '化肥', '化石', '化学', '化验', '化妆', '划分', '画蛇添足', '话题', '话筒', '怀念', '怀疑', '怀孕', '欢乐', '还原', '环节', '缓和', '缓解', '幻想', '患者', '荒凉', '荒谬', '荒唐', '慌张', '皇帝', '皇后', '黄昏', '黄金', '恍然大悟', '晃', '灰', '灰尘', '灰心', '挥', '挥霍', '恢复', '辉煌', '回报', '回避', '回顾', '回收', '回忆', '悔恨', '毁灭', '汇报', '汇率', '会晤', '贿赂', '昏迷', '荤', '婚礼', '婚姻', '浑身', '混合', '混乱', '混淆', '混浊', '活动', '活该', '活力', '活泼', '活跃', '火', '火柴', '火箭', '火焰', '火药', '伙伴', '或许', '货币', '获得', '讥笑', '饥饿', '机动', '机构', '机灵', '机密', '机器', '机械', '机遇', '机智', '肌肉', '积极', '积累', '基本', '基础', '基地', '基金', '基因', '激动', '激发', '激励', '激烈', '激情', '及格', '及时', '及早', '吉祥', '级别', '极端', '极其', '极限', '即便', '即将', '即使', '急功近利', '急剧', '急忙', '急切', '急于求成', '急躁', '急诊', '疾病', '集合', '集体', '集团', '集中', '嫉妒', '籍贯', '给予', '计划', '计较', '计算', '记录', '记性', '记忆', '记载', '记者', '纪录', '纪律', '纪念', '纪要', '技巧', '技术', '系领带', '忌讳', '季度', '季军', '迹象', '既然', '继承', '继续', '寄', '寄托', '寂静', '寂寞', '加班', '加工', '加剧', '加油站', '夹杂', '夹子', '佳肴', '家常', '家伙', '家具', '家属', '家庭', '家务', '家乡', '家喻户晓', '嘉宾', '甲', '假', '假如', '假设', '假装', '价格', '价值', '驾驶', '嫁', '尖端', '尖锐', '坚持', '坚定', '坚固', '坚决', '坚强', '坚韧', '坚实', '坚硬', '肩膀', '艰巨', '艰苦', '艰难', '监督', '监视', '监狱', '兼职', '煎', '拣', '捡', '检讨', '检验', '减肥', '减少', '剪彩', '剪刀', '简化', '简历', '简陋', '简体字', '简要', '简直', '见多识广', '见解', '见闻', '见义勇为', '间谍', '间隔', '间接', '建立', '建设', '建议', '建筑', '剑', '健全', '健身', '舰艇', '践踏', '溅', '鉴别', '鉴定', '鉴于', '键盘', '将近', '将就', '将军', '将来', '僵硬', '讲究', '讲座', '奖金', '奖励', '奖赏', '桨', '降低', '降临', '降落', '酱油', '交', '交叉', '交代', '交换', '交际', '交流', '交涉', '交通', '交往', '交易', '郊区', '浇', '娇气', '骄傲', '胶水', '焦点', '焦急', '角度', '角落', '侥幸', '狡猾', '饺子', '搅拌', '缴纳', '较量', '教材', '教练', '教授', '教训', '教养', '教育', '阶层', '阶段', '皆', '结实', '接触', '接待', '接近', '接连', '接受', '接着', '揭露', '节', '节省', '节约', '节制', '节奏', '杰出', '结构', '结果', '结合', '结晶', '结局', '结论', '结算', '结账', '截止', '截至', '竭尽全力', '解除', '解放', '解雇', '解剖', '解散', '解释', '解体', '戒', '戒备', '戒指', '届', '界限', '借鉴', '借口', '借助', '金融', '金属', '津津有味', '尽管', '尽快', '尽量', '紧急', '紧迫', '紧张', '锦上添花', '谨慎', '尽力', '进步', '进而', '进攻', '进化', '进口', '进行', '进展', '近代', '近来', '晋升', '浸泡', '禁止', '茎', '京剧', '经典', '经费', '经济', '经历', '经商', '经纬', '经验', '经营', '惊动', '惊奇', '惊讶', '兢兢业业', '精彩', '精打细算', '精华', '精简', '精力', '精密', '精确', '精神', '精通', '精心', '精益求精', '精致', '井', '颈椎', '景色', '警察', '警告', '警惕', '竞赛', '竞选', '竞争', '竟然', '敬礼', '敬业', '境界', '镜头', '镜子', '纠纷', '纠正', '究竟', '酒吧', '酒精', '救', '救护车', '救济', '就近', '就业', '就职', '舅舅', '拘留', '拘束', '居民', '居然', '居住', '鞠躬', '局部', '局面', '局势', '局限', '桔子', '咀嚼', '沮丧', '举', '举办', '举动', '举世瞩目', '举行', '举足轻重', '巨大', '拒绝', '具备', '具体', '俱乐部', '剧本', '剧烈', '据说', '据悉', '距离', '聚会', '聚精会神', '捐', '卷', '决策', '决赛', '决心', '角色', '觉悟', '觉醒', '绝对', '绝望', '倔强', '军队', '军事', '均匀', '君子', '卡车', '卡通', '开采', '开除', '开发', '开放', '开阔', '开朗', '开明', '开幕式', '开辟', '开水', '开拓', '开玩笑', '开心', '开展', '开支', '刊登', '刊物', '勘探', '侃侃而谈', '砍', '砍伐', '看不起', '看待', '看法', '看望', '慷慨', '扛', '抗议', '考察', '考古', '考核', '考虑', '考验', '烤鸭', '靠', '靠拢', '科目', '科学', '棵', '颗', '磕', '咳嗽', '可观', '可见', '可靠', '可口', '可怜', '可怕', '可是', '可恶', '可惜', '可行', '渴望', '克', '克服', '克制', '刻不容缓', '刻苦', '客观', '客户', '客厅', '课程', '课题', '肯定', '恳切', '啃', '坑', '空', '空洞', '空间', '空气', '空前绝后', '空想', '空虚', '孔', '恐怖', '恐吓', '恐惧', '恐怕', '空白', '空隙', '空闲', '控制', '口气', '口腔', '口头', '口味', '口音', '扣', '枯萎', '枯燥', '哭泣', '苦', '苦尽甘来', '苦涩', '夸', '夸张', '挎', '跨', '会计', '快活', '宽', '宽敞', '宽容', '款待', '款式', '筐', '旷课', '况且', '矿产', '矿泉水', '框架', '亏待', '亏损', '昆虫', '捆绑', '困', '困难', '扩充', '扩大', '扩散', '扩张', '垃圾桶', '拉', '喇叭', '蜡烛', '辣', '辣椒', '啦', '来不及', '来得及', '来历', '来源', '来自', '拦', '栏目', '懒', '懒惰', '烂', '狼狈', '狼吞虎咽', '朗读', '浪费', '浪漫', '捞', '劳动', '劳驾', '牢固', '牢骚', '唠叨', '老百姓', '老板', '老虎', '老婆', '老实', '老鼠', '姥姥', '乐观', '乐趣', '乐意', '雷', '雷达', '类似', '类型', '冷淡', '冷静', '冷酷', '冷落', '冷却', '愣', '厘米', '离婚', '梨', '黎明', '礼拜天', '礼节', '礼貌', '礼尚往来', '里程碑', '理睬', '理发', '理解', '理论', '理所当然', '理想', '理由', '理直气壮', '理智', '力量', '力气', '力求', '力所能及', '力争', '历代', '历来', '厉害', '立场', '立方', '立即', '立交桥', '立刻', '立体', '立足', '利害', '利润', '利息', '利益', '利用', '例如', '例外', '粒', '俩', '连', '连忙', '连年', '连锁', '连同', '连续', '联合', '联欢', '联络', '联盟', '联系', '联想', '廉洁', '恋爱', '良好', '良心', '凉快', '粮食', '亮', '谅解', '晾', '辽阔', '了不起', '列车', '列举', '临床', '临时', '淋', '吝啬', '伶俐', '灵感', '灵魂', '灵活', '灵敏', '铃', '凌晨', '零件', '零钱', '零食', '零星', '领导', '领会', '领事馆', '领土', '领悟', '领先', '领袖', '领域', '另外', '溜', '浏览', '留', '留恋', '留念', '留神', '流传', '流浪', '流泪', '流利', '流露', '流氓', '流通', '流行', '龙', '聋哑', '隆重', '垄断', '笼罩', '搂', '漏', '炉灶', '陆地', '陆续', '录取', '录音', '旅行', '屡次', '履行', '律师', '乱', '掠夺', '轮船', '轮廓', '轮流', '轮胎', '论坛', '论文', '论证', '啰唆', '逻辑', '络绎不绝', '落成', '落后', '落实', '麻痹', '麻烦', '麻木', '麻醉', '马虎', '码头', '蚂蚁', '骂', '嘛', '埋伏', '埋没', '埋葬', '迈', '麦克风', '脉搏', '埋怨', '馒头', '满', '满足', '蔓延', '漫长', '漫画', '慢性', '忙碌', '盲目', '茫茫', '茫然', '毛', '毛病', '毛巾', '矛盾', '茂盛', '冒充', '冒犯', '冒险', '贸易', '枚', '眉毛', '媒介', '媒体', '煤炭', '美观', '美丽', '美满', '美妙', '美术', '魅力', '萌芽', '猛烈', '梦', '梦想', '眯', '弥补', '弥漫', '迷惑', '迷路', '迷人', '迷信', '谜语', '秘密', '秘书', '密度', '密封', '密码', '密切', '蜜蜂', '棉花', '免得', '免费', '免疫', '勉励', '勉强', '面对', '面积', '面临', '面貌', '面子', '苗条', '描绘', '描写', '瞄准', '秒', '渺小', '藐视', '灭亡', '蔑视', '民间', '民主', '民族', '敏感', '敏捷', '敏锐', '名次', '名额', '名副其实', '名牌', '名片', '名胜古迹', '名誉', '明明', '明确', '明显', '明星', '明智', '命令', '命名', '命运', '摸', '摸索', '模范', '模仿', '模糊', '模式', '模特', '模型', '膜', '摩擦', '摩托车', '磨合', '魔鬼', '魔术', '抹杀', '陌生', '莫名其妙', '墨水儿', '默默', '谋求', '某', '模样', '母亲', '母语', '木头', '目标', '目的', '目睹', '目光', '目录', '目前', '沐浴', '拿手', '哪怕', '纳闷儿', '耐心', '耐用', '南辕北辙', '难道', '难得', '难怪', '难堪', '难免', '难能可贵', '难受', '恼火', '脑袋', '内', '内部', '内涵', '内科', '内幕', '内容', '内在', '嫩', '能干', '能力', '能量', '能源', '嗯', '拟定', '逆行', '年代', '年度', '年纪', '年龄', '念', '捏', '凝固', '凝聚', '凝视', '拧', '宁可', '宁肯', '宁愿', '牛仔裤', '扭转', '纽扣儿', '农村', '农历', '农民', '农业', '浓', '浓厚', '弄', '奴隶', '女士', '暖和', '虐待', '挪', '哦', '欧洲', '殴打', '呕吐', '偶尔', '偶然', '偶像', '趴', '拍', '排斥', '排除', '排队', '排放', '排练', '排列', '徘徊', '派', '派别', '派遣', '攀登', '盘旋', '判断', '判决', '盼望', '畔', '庞大', '抛弃', '泡沫', '陪', '培训', '培养', '培育', '赔偿', '佩服', '配备', '配合', '配偶', '配套', '盆', '盆地', '烹饪', '捧', '碰', '批', '批发', '批判', '批评', '批准', '披', '劈', '皮肤', '皮革', '疲惫', '疲倦', '疲劳', '脾气', '匹', '屁股', '譬如', '偏差', '偏见', '偏僻', '偏偏', '篇', '便宜', '片', '片断', '片刻', '片面', '骗', '漂浮', '飘', '飘扬', '撇', '拼搏', '拼命', '拼音', '贫乏', '贫困', '频道', '频繁', '频率', '品尝', '品德', '品质', '品种', '乒乓球', '平', '平安', '平常', '平等', '平凡', '平方', '平衡', '平静', '平均', '平面', '平时', '平坦', '平行', '平庸', '平原', '评估', '评价', '评论', '凭', '屏幕', '屏障', '坡', '泼', '颇', '迫不及待', '迫害', '迫切', '破', '破产', '破坏', '破例', '魄力', '扑', '铺', '葡萄', '朴实', '朴素', '普遍', '普及', '普通话', '瀑布', '凄凉', '期待', '期间', '期望', '期限', '欺负', '欺骗', '齐全', '齐心协力', '其次', '其余', '其中', '奇迹', '奇妙', '歧视', '旗袍', '旗帜', '乞丐', '岂有此理', '企图', '企业', '启程', '启发', '启蒙', '启示', '启事', '起草', '起初', '起伏', '起哄', '起码', '起源', '气氛', '气概', '气功', '气候', '气魄', '气色', '气势', '气味', '气象', '气压', '气质', '迄今为止', '汽油', '器材', '器官', '掐', '洽谈', '恰当', '恰到好处', '恰巧', '千方百计', '千万', '迁就', '迁徙', '牵', '牵扯', '牵制', '谦虚', '谦逊', '签', '签署', '签证', '前景', '前提', '前途', '潜力', '潜水', '潜移默化', '浅', '谴责', '欠', '枪', '强调', '强烈', '强制', '墙', '抢', '抢劫', '抢救', '强迫', '悄悄', '敲', '桥', '桥梁', '瞧', '巧克力', '巧妙', '窍门', '翘', '切', '切实', '锲而不舍', '钦佩', '侵犯', '侵略', '亲爱', '亲密', '亲戚', '亲切', '亲热', '亲自', '勤奋', '勤俭', '勤劳', '青', '青春', '青少年', '轻', '轻视', '轻松', '轻易', '倾听', '倾向', '倾斜', '清澈', '清晨', '清除', '清淡', '清洁', '清理', '清晰', '清醒', '清真', '情报', '情节', '情景', '情况', '情理', '情形', '情绪', '晴朗', '请柬', '请教', '请求', '请示', '请帖', '庆祝', '穷', '丘陵', '球迷', '区别', '区分', '区域', '曲折', '驱逐', '屈服', '趋势', '渠道', '曲子', '取', '取缔', '取消', '娶', '去世', '趣味', '圈', '圈套', '权衡', '权力', '权利', '权威', '全部', '全局', '全力以赴', '全面', '拳头', '犬', '劝', '缺点', '缺乏', '缺口', '缺少', '缺席', '缺陷', '瘸', '却', '确保', '确定', '确立', '确切', '确认', '确实', '确信', '群', '群众', '然而', '燃烧', '染', '嚷', '让步', '饶恕', '扰乱', '绕', '惹祸', '热爱', '热泪盈眶', '热烈', '热门', '热闹', '热心', '人才', '人道', '人格', '人工', '人家', '人间', '人口', '人类', '人民币', '人生', '人士', '人事', '人为', '人物', '人性', '人员', '人质', '仁慈', '忍不住', '忍耐', '忍受', '认定', '认可', '任何', '任命', '任务', '任性', '任意', '任重道远', '扔', '仍旧', '仍然', '日常', '日程', '日记', '日历', '日期', '日新月异', '日益', '日用品', '日子', '荣幸', '荣誉', '容貌', '容纳', '容器', '容忍', '溶解', '融化', '融洽', '柔和', '揉', '如何', '如今', '儒家', '入口', '软', '软件', '若干', '弱', '弱点', '撒谎', '洒', '散文', '散布', '散步', '散发', '嗓子', '丧失', '骚扰', '嫂子', '色彩', '森林', '杀', '沙发', '沙漠', '沙滩', '刹车', '啥', '傻', '筛选', '晒', '山脉', '删除', '闪电', '闪烁', '扇子', '善良', '善于', '擅长', '擅自', '伤害', '伤脑筋', '伤心', '商标', '商量', '商品', '商务', '商业', '上当', '上级', '上进', '上任', '上瘾', '上游', '尚且', '捎', '梢', '稍微', '勺子', '哨', '奢侈', '舌头', '蛇', '舍不得', '设备', '设计', '设立', '设施', '设想', '设置', '社会', '社区', '射击', '涉及', '摄氏度', '摄影', '申报', '申请', '伸', '身材', '身份', '呻吟', '绅士', '深', '深奥', '深沉', '深刻', '深情厚谊', '神话', '神经', '神秘', '神奇', '神气', '神圣', '神态', '神仙', '审查', '审理', '审美', '审判', '甚至', '渗透', '慎重', '升', '生产', '生存', '生动', '生活', '生机', '生理', '生命', '生疏', '生态', '生物', '生肖', '生效', '生锈', '生意', '生育', '生长', '声调', '声明', '声势', '声誉', '牲畜', '绳子', '省', '省会', '省略', '胜负', '胜利', '盛产', '盛开', '盛情', '盛行', '剩', '尸体', '失败', '失眠', '失去', '失事', '失望', '失误', '失业', '失踪', '师范', '师傅', '诗', '狮子', '施加', '施展', '湿润', '十分', '十足', '石头', '石油', '时差', '时常', '时代', '时而', '时光', '时机', '时刻', '时髦', '时期', '时尚', '时事', '识别', '实话', '实惠', '实际', '实践', '实力', '实施', '实事求是', '实习', '实现', '实行', '实验', '实用', '实在', '实质', '拾', '食物', '使', '使劲儿', '使命', '使用', '始终', '士兵', '示范', '示威', '示意', '世代', '世纪', '市场', '似的', '势必', '势力', '事故', '事迹', '事件', '事实', '事态', '事务', '事物', '事先', '事项', '事业', '试卷', '试图', '试验', '视力', '视频', '视线', '视野', '是非', '是否', '适合', '适宜', '适应', '逝世', '释放', '收', '收藏', '收获', '收据', '收入', '收拾', '收缩', '收益', '收音机', '手法', '手工', '手势', '手术', '手套', '手续', '手艺', '手指', '守护', '首', '首都', '首饰', '首先', '首要', '寿命', '受不了', '受到', '受伤', '受罪', '授予', '售货员', '书法', '书籍', '书记', '书架', '书面', '梳子', '舒畅', '舒适', '疏忽', '疏远', '输', '输入', '蔬菜', '熟练', '熟悉', '属于', '鼠标', '数', '束', '束缚', '树立', '竖', '数额', '数据', '数量', '数码', '数字', '耍', '衰老', '衰退', '摔倒', '甩', '帅', '率领', '涮火锅', '双胞胎', '双方', '爽快', '水利', '水龙头', '水泥', '税', '顺便', '顺利', '顺序', '瞬间', '说不定', '说服', '说明', '硕士', '司法', '司令', '丝绸', '丝毫', '私人', '私自', '思考', '思念', '思索', '思维', '思想', '斯文', '撕', '死', '死亡', '四肢', '寺庙', '似乎', '饲养', '肆无忌惮', '耸', '搜索', '艘', '苏醒', '俗话', '诉讼', '素食', '素质', '速度', '宿舍', '塑料袋', '塑造', '酸', '算数', '虽然……但是……', '随便', '随即', '随身', '随时', '随手', '随意', '随着', '岁月', '碎', '隧道', '孙子', '损坏', '损失', '缩短', '所', '所有', '索取', '索性', '锁', '塌', '踏实', '塔', '台', '台风', '台阶', '抬', '太极拳', '太空', '太太', '态度', '泰斗', '贪婪', '贪污', '摊', '瘫痪', '谈', '谈判', '弹钢琴', '弹性', '坦白', '坦率', '叹气', '探测', '探索', '探讨', '探望', '汤', '糖', '倘若', '躺', '烫', '趟', '掏', '滔滔不绝', '逃', '逃避', '桃', '陶瓷', '陶醉', '淘气', '淘汰', '讨好', '讨价还价', '讨论', '讨厌', '套', '特长', '特点', '特定', '特色', '特殊', '特意', '特征', '疼爱', '提', '提拔', '提倡', '提纲', '提供', '提炼', '提前', '提示', '提问', '提醒', '提议', '题材', '题目', '体裁', '体会', '体积', '体谅', '体面', '体贴', '体系', '体现', '体验', '天才', '天赋', '天空', '天伦之乐', '天然气', '天生', '天堂', '天文', '天真', '田径', '田野', '填空', '舔', '挑剔', '条件', '条款', '条理', '条约', '调和', '调剂', '调节', '调解', '调料', '调皮', '调整', '挑拨', '挑衅', '挑战', '跳跃', '亭子', '停', '停泊', '停顿', '停滞', '挺', '挺拔', '通常', '通过', '通货膨胀', '通缉', '通俗', '通讯', '通用', '通知', '同胞', '同情', '同时', '同志', '铜', '童话', '统筹兼顾', '统计', '统统', '统一', '统治', '痛苦', '痛快', '偷', '投机', '投票', '投入', '投诉', '投降', '投掷', '投资', '透露', '透明', '秃', '突出', '突破', '图案', '徒弟', '途径', '涂抹', '土地', '土豆', '土壤', '吐', '兔子', '团', '团结', '团体', '团圆', '推', '推测', '推迟', '推辞', '推翻', '推广', '推荐', '推理', '推论', '推销', '退', '退步', '退休', '吞吞吐吐', '托运', '拖延', '脱', '脱离', '妥当', '妥善', '妥协', '椭圆', '唾弃', '挖掘', '哇', '娃娃', '瓦解', '袜子', '歪', '歪曲', '外表', '外公', '外行', '外交', '外界', '外向', '丸', '完备', '完毕', '完美', '完全', '完善', '完整', '玩具', '玩弄', '玩意儿', '顽固', '顽强', '挽回', '挽救', '惋惜', '万分', '万一', '王子', '网络', '网球', '网站', '往常', '往返', '往事', '往往', '妄想', '危害', '危机', '危险', '威风', '威力', '威望', '威胁', '威信', '微不足道', '微观', '微笑', '为难', '为期', '违背', '违反', '围巾', '围绕', '唯独', '唯一', '维持', '维护', '维生素', '维修', '伟大', '伪造', '尾巴', '委屈', '委托', '委员', '卫生间', '卫星', '未必', '未来', '未免', '位于', '位置', '味道', '畏惧', '胃', '胃口', '喂（叹词）', '喂（动词）', '蔚蓝', '慰问', '温带', '温度', '温和', '温暖', '温柔', '文件', '文具', '文明', '文凭', '文物', '文献', '文学', '文雅', '文艺', '文章', '文字', '闻', '吻', '稳定', '问候', '问世', '窝', '卧室', '握手', '乌黑', '污蔑', '污染', '诬陷', '屋子', '无', '无比', '无偿', '无耻', '无动于衷', '无非', '无辜', '无精打采', '无赖', '无理取闹', '无聊', '无论', '无奈', '无能为力', '无穷无尽', '无数', '无所谓', '无微不至', '无忧无虑', '无知', '武器', '武术', '武侠', '武装', '侮辱', '舞蹈', '勿', '务必', '物理', '物美价廉', '物业', '物质', '物资', '误差', '误会', '误解', '雾', '夕阳', '西红柿', '吸取', '吸收', '吸引', '昔日', '牺牲', '溪', '熄灭', '膝盖', '习俗', '袭击', '媳妇', '喜闻乐见', '喜悦', '戏剧', '系', '系列', '系统', '细胞', '细节', '细菌', '细致', '瞎', '峡谷', '狭隘', '狭窄', '霞', '下属', '下载', '吓', '夏令营', '先进', '先前', '纤维', '掀起', '鲜明', '鲜艳', '闲话', '贤惠', '弦', '咸', '衔接', '嫌', '嫌疑', '显得', '显然', '显示', '显著', '县', '现场', '现成', '现代', '现金', '现实', '现象', '现状', '限制', '线索', '宪法', '陷害', '陷阱', '陷入', '馅儿', '羡慕', '乡镇', '相差', '相处', '相当', '相等', '相对', '相反', '相辅相成', '相关', '相似', '相同', '相应', '香', '香肠', '镶嵌', '详细', '享受', '响', '响亮', '响应', '想方设法', '想念', '想象', '向导', '向来', '向往', '项', '项链', '项目', '巷', '相声', '象棋', '象征', '橡皮', '削', '消除', '消毒', '消防', '消费', '消耗', '消化', '消极', '消灭', '消失', '消息', '销毁', '销售', '潇洒', '小吃', '小伙子', '小麦', '小气', '小说', '小心翼翼', '孝顺', '肖像', '笑话', '效果', '效率', '效益', '歇', '协会', '协商', '协调', '协议', '协助', '斜', '携带', '写作', '血', '泄露', '泄气', '屑', '谢绝', '心得', '心甘情愿', '心理', '心灵', '心情', '心态', '心疼', '心血', '心眼儿', '心脏', '辛苦', '辛勤', '欣赏', '欣慰', '欣欣向荣', '新陈代谢', '新郎', '新娘', '新颖', '薪水', '信封', '信号', '信赖', '信念', '信任', '信息', '信心', '信仰', '信誉', '兴奋', '兴隆', '兴旺', '腥', '刑事', '行', '行动', '行人', '行为', '行政', '形成', '形容', '形式', '形势', '形态', '形象', '形状', '醒', '兴高采烈', '兴致勃勃', '幸福', '幸亏', '幸运', '性别', '性感', '性格', '性命', '性能', '性质', '凶恶', '凶手', '兄弟', '汹涌', '胸', '胸怀', '胸膛', '雄厚', '雄伟', '休闲', '修复', '修改', '修建', '修理', '修养', '羞耻', '绣', '嗅觉', '须知', '虚假', '虚荣', '虚伪', '虚心', '需求', '许多', '许可', '序言', '叙述', '畜牧', '酗酒', '宣布', '宣传', '宣誓', '宣扬', '喧哗', '悬挂', '悬念', '悬殊', '悬崖峭壁', '旋律', '旋转', '选拔', '选举', '选手', '炫耀', '削弱', '学历', '学期', '学术', '学说', '学位', '学问', '雪上加霜', '血压', '熏陶', '寻觅', '寻找', '巡逻', '询问', '循环', '循序渐进', '训练', '迅速', '压力', '压迫', '压岁钱', '压缩', '压抑', '压榨', '压制', '呀', '押金', '鸦雀无声', '牙齿', '牙膏', '亚军', '亚洲', '烟花爆竹', '淹没', '延长', '延期', '延伸', '延续', '严格', '严寒', '严禁', '严峻', '严厉', '严密', '严肃', '严重', '言论', '岩石', '炎热', '沿海', '研究', '盐', '掩盖', '掩护', '掩饰', '眼光', '眼镜', '眼色', '眼神', '演变', '演出', '演讲', '演习', '演绎', '演员', '演奏', '厌恶', '宴会', '验收', '验证', '阳光', '阳台', '养成', '氧气', '痒', '样品', '样式', '样子', '腰', '邀请', '谣言', '摇', '摇摆', '摇滚', '遥控', '遥远', '咬', '要不', '要点', '要命', '要是', '要素', '钥匙', '耀眼', '也许', '野蛮', '野心', '业务', '业余', '叶子', '页', '夜', '液体', '一辈子', '一旦', '一度', '一帆风顺', '一贯', '一举两得', '一流', '一律', '一目了然', '一切', '一如既往', '一丝不苟', '一向', '一再', '一致', '衣裳', '依旧', '依据', '依靠', '依赖', '依然', '依托', '仪器', '仪式', '移动', '移民', '遗产', '遗传', '遗憾', '遗留', '遗失', '疑惑', '疑问', '乙', '以', '以便', '以及', '以来', '以免', '以往', '以为', '以至', '以致', '亿', '义务', '艺术', '议论', '亦', '异常', '意见', '意料', '意识', '意图', '意外', '意味着', '意向', '意义', '意志', '毅力', '毅然', '翼', '因此', '因而', '因素', '因为……所以……', '阴谋', '音响', '银', '引导', '引起', '引擎', '引用', '饮食', '隐蔽', '隐患', '隐瞒', '隐私', '隐约', '印刷', '印象', '英俊', '英明', '英雄', '英勇', '婴儿', '迎接', '迎面', '盈利', '营养', '营业', '赢', '影子', '应酬', '应付', '应聘', '应邀', '应用', '硬', '硬件', '拥抱', '拥护', '拥挤', '拥有', '庸俗', '永恒', '永远', '勇敢', '勇气', '勇于', '涌现', '踊跃', '用功', '用户', '用途', '优点', '优惠', '优美', '优胜劣汰', '优势', '优先', '优秀', '优异', '优越', '忧郁', '幽默', '悠久', '尤其', '由', '由于', '邮局', '犹如', '犹豫', '油腻', '油漆', '油炸', '游览', '友好', '友谊', '有利', '有趣', '有条不紊', '幼儿园', '幼稚', '诱惑', '于是', '娱乐', '渔民', '愉快', '愚蠢', '愚昧', '舆论', '与', '与其', '与日俱增', '宇宙', '羽毛球', '羽绒服', '语法', '语气', '语言', '玉', '玉米', '预报', '预订', '预防', '预料', '预期', '预算', '预习', '预先', '预言', '预兆', '欲望', '寓言', '愈', '冤枉', '元旦', '元首', '元素', '元宵节', '园林', '员工', '原告', '原来', '原理', '原谅', '原料', '原始', '原先', '原因', '原则', '圆', '圆满', '缘故', '源泉', '愿望', '约会', '约束', '乐谱', '乐器', '岳母', '阅读', '晕', '云', '允许', '孕育', '运气', '运输', '运算', '运行', '运用', '酝酿', '蕴藏', '熨', '杂技', '杂交', '杂志', '砸', '咋', '灾害', '灾难', '栽培', '宰', '再接再厉', '再三', '在乎', '在意', '在于', '咱们', '攒', '暂且', '暂时', '赞成', '赞美', '赞叹', '赞助', '脏', '遭受', '遭殃', '遭遇', '糟糕', '糟蹋', '造成', '造型', '噪音', '则', '责备', '责怪', '责任', '贼', '增加', '增添', '赠送', '扎', '扎实', '渣', '眨', '诈骗', '摘', '摘要', '窄', '债券', '沾光', '粘贴', '瞻仰', '斩钉截铁', '展开', '展览', '展示', '展望', '展现', '崭新', '占', '占据', '占领', '占线', '战斗', '战略', '战术', '战役', '战争', '章程', '长辈', '涨', '掌握', '帐篷', '账户', '障碍', '招标', '招待', '招聘', '招收', '朝气蓬勃', '着火', '着凉', '着迷', '沼泽', '召开', '照', '照常', '照样', '照耀', '折腾', '遮挡', '折', '折磨', '哲学', '针对', '侦探', '珍贵', '珍惜', '珍稀', '珍珠', '真理', '真实', '真相', '真正', '真挚', '斟酌', '诊断', '枕头', '阵', '阵地', '阵容', '振动', '振奋', '振兴', '震撼', '震惊', '镇定', '镇静', '正月', '争端', '争夺', '争论', '争气', '争取', '争先恐后', '争议', '征服', '征求', '征收', '挣扎', '睁', '蒸发', '整顿', '整个', '整理', '整齐', '整体', '正', '正常', '正当', '正负', '正规', '正好', '正经', '正气', '正确', '正式', '正义', '正宗', '证件', '证据', '证明', '证实', '证书', '郑重', '政策', '政府', '政权', '政治', '挣', '症状', '之', '之际', '支', '支撑', '支持', '支出', '支流', '支配', '支票', '支援', '支柱', '枝', '知道', '知觉', '知识', '知足常乐', '脂肪', '执行', '执照', '执着', '直', '直播', '直接', '直径', '侄子', '值班', '值得', '职能', '职位', '职务', '职业', '植物', '殖民地', '只好', '只要', '指', '指标', '指导', '指定', '指挥', '指甲', '指令', '指南针', '指示', '指望', '指责', '至今', '至少', '至于', '志气', '志愿者', '制裁', '制定', '制度', '制服', '制约', '制造', '制止', '制作', '质量', '治安', '治理', '治疗', '致辞', '致力', '致使', '秩序', '智慧', '智力', '智能', '智商', '滞留', '中断', '中介', '中立', '中心', '中旬', '中央', '忠诚', '忠实', '终点', '终究', '终身', '终止', '衷心', '肿瘤', '种类', '种子', '种族', '众所周知', '种植', '重', '重大', '重点', '重量', '重视', '重心', '舟', '州', '周边', '周到', '周密', '周年', '周期', '周围', '周折', '周转', '粥', '昼夜', '皱纹', '株', '诸位', '猪', '竹子', '逐步', '逐渐', '逐年', '主办', '主持', '主导', '主动', '主观', '主管', '主流', '主权', '主人', '主任', '主题', '主席', '主义', '主意', '主张', '拄', '煮', '嘱咐', '助理', '助手', '住宅', '注册', '注射', '注视', '注释', '注重', '驻扎', '祝福', '祝贺', '著名', '著作', '铸造', '抓', '抓紧', '拽', '专长', '专程', '专家', '专利', '专门', '专题', '专心', '专业', '砖', '转', '转变', '转达', '转告', '转让', '转移', '转折', '传记', '赚', '庄稼', '庄严', '庄重', '装', '装备', '装饰', '装卸', '装修', '壮观', '壮丽', '壮烈', '状况', '状态', '撞', '幢', '追', '追悼', '追究', '追求', '坠', '准确', '准时', '准则', '卓越', '着手', '着想', '着重', '咨询', '姿势', '姿态', '资本', '资产', '资格', '资金', '资料', '资深', '资源', '资助', '滋润', '滋味', '子弹', '仔细', '紫', '自卑', '自从', '自动', '自发', '自豪', '自觉', '自力更生', '自满', '自然', '自私', '自信', '自由', '自愿', '自主', '字母', '字幕', '宗教', '宗旨', '综合', '棕色', '踪迹', '总裁', '总而言之', '总共', '总和', '总结', '总理', '总算', '总统', '总之', '纵横', '走廊', '走漏', '走私', '揍', '租', '租赁', '足以', '阻碍', '阻拦', '阻挠', '阻止', '组', '组成', '组合', '组织', '祖父', '祖国', '祖先', '钻研', '钻石', '嘴唇', '最初', '最好', '罪犯', '醉', '尊敬', '尊严', '尊重', '遵守', '遵循', '琢磨', '左右', '作弊', '作废', '作风', '作家', '作品', '作为', '作文', '作息', '作用', '作者', '座', '座位', '座右铭', '做主']


# In[86]:


#feature 62 HSK core vocabulary level 6 (600-5000), 4403 words 
def hsk6(text_type):
    def raw(text_type): 
        return len([x for x in text_type if x in HSK6])
    def normalized(text_type): 
        return raw(text_type) / len(text_type)
    return round(normalized (text_type) * 1000, 2) 


# In[87]:


hsk6_result=[]
for corpus in sub_corpora: 
    hsk6_result.append(hsk6(corpus))
    
df['HSK_6'] = pd.Series(hsk6_result)
df.to_csv(folder + 'linguistic_features.csv')


# In[88]:


honourifics=['千金', '相公', '姑姥爷', '伯伯', '伯父', '伯母', '大伯', '大哥', '大姐', '大妈', '大爷', '大嫂', '嫂夫人', '大婶儿', '大叔', '大姨', '哥', '姐', '大娘', '妈妈', '奶 奶', '爷爷', '姨', '老伯', '老兄', '老爹', '老大爷', '老爷爷', '老太太', '老奶奶', '老大娘', '老板', '老公', '老婆婆', '老前辈', '老人家', '老师', '老师傅', '老寿星', '老太爷', '老翁', '老爷子', '老丈', '老总', '大驾', '夫人', '高徒', '高足', '官人', '贵客', '贵人', '嘉宾', '列位', '男士', '女士', '女主 人', '前辈', '台驾', '太太', '先生', '贤契', '贤人', '贤士', '先哲', '小姐', '学长', '爷', '诸位', '足下', '师傅', '师母', '师娘', '人士', '长老', '禅师', '船老大', '大师', '大师傅', '大王', '恩师', '法师', '法王', '佛爷', '夫子', '父母官', '国父', '麾下', '教授', '武师', '千 岁', '孺人', '圣母', '圣人', '师父', '王尊', '至尊', '座', '少奶奶', '少爷', '金枝玉叶', '工程师', '高级工程师', '经济师', '讲师', '教授', '副教授', '教师', '老师', '国家主席', '国家总理', '部长', '厅长', '市长', '局长', '科长', '校长', '烈士', '先烈', '先哲', '荣誉军人', '陛下', '殿下', '阁下', '阿公', '阿婆', '大人', '公', '公公', '娘子', '婆婆', '丈人', '师长', '义士', '勇士', '志士', '壮士']


# In[89]:


def honor(text_type):
    def raw(text_type): 
        return len([x for x in text_type if x in honourifics])
    def normalized(text_type): 
        return raw(text_type) / len(text_type)
    return round(normalized (text_type) * 1000, 2) 


# In[90]:


honor_result=[]
for corpus in sub_corpora: 
    honor_result.append(honor(corpus))
    
df['honourifics'] = pd.Series(honor_result)
df.to_csv(folder + 'linguistic_features.csv')


# In[91]:


humbles=['学生', '兄弟', '小弟', '弟', '妹', '儿子', '女儿']


# In[94]:


#feature 80 abstract nouns 
def abstract(text):
    def raw(text): 
        return text.count('社会')+text.count('问题')+text.count('生活')+text.count('经济')+text.count('关系')+text.count('作用')+text.count('中国')+text.count('现在')+text.count('情况')+text.count('时候')+text.count('人民')+text.count('活动')+text.count('方面')+text.count('科学')+text.count('条件')+text.count('思想')+text.count('过程')+text.count('影响')+text.count('方法')+text.count('要求')+text.count('技术')+text.count('事')+text.count('时间')+text.count('世界')+text.count('教育')+text.count('社会主义')+text.count('组织')+text.count('地方')+text.count('文化')+text.count('运动')+text.count('历史')+text.count('地区')+text.count('物质')+text.count('形式')+text.count('政治')+text.count('自然')+text.count('东西')+text.count('结构')+text.count('现象')+text.count('理论')+text.count('工业')+text.count('人类')+text.count('精神')+text.count('结果')+text.count('时期')+text.count('意义')+text.count('语言')+text.count('内容')+text.count('计划')+text.count('水平')+text.count('产品')+text.count('基础')+text.count('环境')+text.count('特点')+text.count('能力')+text.count('知识')+text.count('经验')+text.count('实际')+text.count('性质')+text.count('政府')+text.count('作品')+text.count('目的')+text.count('规律')+text.count('力量')+text.count('办法')+text.count('心理')+text.count('原则')+text.count('商品')+text.count('实践')+text.count('行为')+text.count('矛盾')+text.count('原因')+text.count('因素')+text.count('地位')+text.count('方向')+text.count('资本主义')+text.count('程度')+text.count('政策')+text.count('范围')+text.count('法律')+text.count('声音')+text.count('时代')+text.count('质量')+text.count('阶段')+text.count('方式')+text.count('人物')+text.count('速度')+text.count('自由')+text.count('价值')+text.count('困难')+text.count('中心')+text.count('事情')+text.count('事物')+text.count('对象')+text.count('现代')+text.count('事业')+text.count('利益')+text.count('材料')+text.count('内部')+text.count('音乐')+text.count('形象')+text.count('国际')+text.count('温度')+text.count('年代')+text.count('观点')+text.count('战争')+text.count('阶级')+text.count('希望')+text.count('家庭')+text.count('空气')+text.count('身体')+text.count('本身')+text.count('感情')+text.count('身上')+text.count('生命')+text.count('效果')+text.count('思维')+text.count('一部分')+text.count('意见')+text.count('标准')+text.count('无产阶级')+text.count('会议')+text.count('信息')+text.count('功能')+text.count('态度')+text.count('概念')+text.count('高度')+text.count('手段')+text.count('基础上')+text.count('理想')+text.count('说话')+text.count('化学')+text.count('措施')+text.count('目标')+text.count('帝国主义')+text.count('生物')+text.count('新闻')+text.count('行动')+text.count('民主')+text.count('资源')+text.count('物体')+text.count('资料')+text.count('意识')+text.count('观念')+text.count('道德')+text.count('实际上')+text.count('位置')+text.count('道路')+text.count('本质')+text.count('军事')+text.count('商业')+text.count('集体')+text.count('体系')+text.count('祖国')+text.count('机关')+text.count('意思')+text.count('机会')+text.count('习惯')+text.count('宗教')+text.count('领域')+text.count('机构')+text.count('国民经济')+text.count('形态')+text.count('哲学')+text.count('比例')+text.count('马克思主义')+text.count('类型')+text.count('成果')+text.count('脸上')+text.count('情绪')+text.count('能量')+text.count('成分')+text.count('健康')+text.count('成绩')+text.count('文艺')+text.count('空间')+text.count('品种')+text.count('主义')+text.count('主体')+text.count('规模')+text.count('形势')+text.count('方针')+text.count('意志')+text.count('责任')+text.count('队伍')+text.count('原理')+text.count('颜色')+text.count('项目')+text.count('委员会')+text.count('情感')+text.count('重点')+text.count('整体')+text.count('生产资料')+text.count('工程')+text.count('战略')+text.count('消息')+text.count('事件')+text.count('情形')+text.count('行政')+text.count('科技')+text.count('交通')+text.count('数学')+text.count('营养')+text.count('成本')+text.count('专业')+text.count('财政')+text.count('食物')+text.count('路线')+text.count('权力')+text.count('利润')+text.count('大部分')+text.count('元素')
    def normalized(text): 
        return raw(text) / len(text)
    return round(normalized (text) * 1000, 2) 


# In[95]:


abstract_result=[]
for corpus in sub_corpora: 
    abstract_result.append(abstract(corpus))

df['abstract'] = pd.Series(abstract_result)
df.to_csv(folder + 'linguistic_features.csv')


# In[96]:


text_lists=[]
for corpus in sub_corpora: 
    text_list=list(corpus)
    text_lists.append(text_list)


# In[97]:


#feature 94 unique items 
def unique(text): 
    return round((len([x for x in text if text.count(x)==1]) / len(text))*1000, 2)


# In[98]:


unique_result=[]
for corpus in sub_corpora: 
    unique_result.append(unique(corpus))


# In[99]:


df['unique'] = pd.Series(unique_result)
df.to_csv(folder + 'linguistic_features.csv')

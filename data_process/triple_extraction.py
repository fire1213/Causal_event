# -*- coding: utf-8 -*-
'''
Created on 2018年11月17日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
from sentence_parser import *
import re
import re, jieba
import jieba.posseg as pseg
from pyltp import SentenceSplitter
import os
from pymongo import MongoClient
import codecs
import pandas as pd
# class CausalitySentencesExractor():#提取因果句子
#     def __init__(self):
#         pass
# 
#     '''1由果溯因配套式'''
#     def ruler1(self, sentence):
#         '''
#         conm2:〈[之]所以,因为〉、〈[之]所以,由于〉、 <[之]所以,缘于〉
#         conm2_model:<Conj>{Effect},<Conj>{Cause}
#         '''
#         datas = []
#         word_pairs =[['之?所以', '因为'], ['之?所以', '由于'], ['之?所以', '缘于']]
#         for word in word_pairs:
#             pattern = re.compile(r'\s?(%s)/[p|c]+\s(.*)(%s)/[p|c]+\s(.*)' % (word[0], word[1]))
#             result = pattern.findall(sentence)
#             if result:
#                 return sentence
#     '''2由因到果配套式'''
#     def ruler2(self, sentence):
#         '''
#         conm1:〈因为,从而〉、〈因为,为此〉、〈既[然],所以〉、〈因为,为此〉、〈由于,为此〉、〈只有|除非,才〉、〈由于,以至[于]>、〈既[然],却>、
#         〈如果,那么|则〉、<由于,从而〉、<既[然],就〉、〈既[然],因此〉、〈如果,就〉、〈只要,就〉〈因为,所以〉、 <由于,于是〉、〈因为,因此〉、
#          <由于,故〉、 〈因为,以致[于]〉、〈因为,因而〉、〈由于,因此〉、<因为,于是〉、〈由于,致使〉、〈因为,致使〉、〈由于,以致[于] >
#          〈因为,故〉、〈因[为],以至[于]>,〈由于,所以〉、〈因为,故而〉、〈由于,因而〉
#         conm1_model:<Conj>{Cause}, <Conj>{Effect}
#         '''
#         datas = []
#         word_pairs =[['因为', '从而'], ['因为', '为此'], ['既然?', '所以'],
#                     ['因为', '为此'], ['由于', '为此'], ['除非', '才'],
#                     ['只有', '才'], ['由于', '以至于?'], ['既然?', '却'],
#                     ['如果', '那么'], ['如果', '则'], ['由于', '从而'],
#                     ['既然?', '就'], ['既然?', '因此'], ['如果', '就'],
#                     ['只要', '就'], ['因为', '所以'], ['由于', '于是'],
#                     ['因为', '因此'], ['由于', '故'], ['因为', '以致于?'],
#                     ['因为', '以致'], ['因为', '因而'], ['由于', '因此'],
#                     ['因为', '于是'], ['由于', '致使'], ['因为', '致使'],
#                     ['由于', '以致于?'], ['因为', '故'], ['因为?', '以至于?'],
#                     ['由于', '所以'], ['因为', '故而'], ['由于', '因而']]
# 
#         for word in word_pairs:
#             pattern = re.compile(r'\s?(%s)/[p|c]+\s(.*)(%s)/[p|c]+\s(.*)' % (word[0], word[1]))
#             result = pattern.findall(sentence)
#             if result:
#                 return sentence
#             
#     '''3由因到果居中式明确'''
#     def ruler3(self, sentence):
#         '''
#         cons2:于是、所以、故、致使、以致[于]、因此、以至[于]、从而、因而
#         cons2_model:{Cause},<Conj...>{Effect}
#         '''
#         datas=[]
#         pattern = re.compile(r'(.*)[,，]+.*(于是|所以|故|致使|以致于?|因此|以至于?|从而|因而)/[p|c]+\s(.*)')
#         result = pattern.findall(sentence)
#         str1=''
#         data = dict()
#         if result:
#             return sentence
#     '''4由因到果居中式精确'''
#     def ruler4(self, sentence):
#         '''
#         verb1:牵动、导向、使动、导致、勾起、引入、指引、使、予以、产生、促成、造成、引导、造就、促使、酿成、
#             引发、渗透、促进、引起、诱导、引来、促发、引致、诱发、推进、诱致、推动、招致、影响、致使、滋生、归于、
#             作用、使得、决定、攸关、令人、引出、浸染、带来、挟带、触发、关系、渗入、诱惑、波及、诱使
#         verb1_model:{Cause},<Verb|Adverb...>{Effect}
#         '''
#         datas=[]
#         pattern = re.compile(r'(.*)\s+(牵动|已致|导向|使动|导致|勾起|引入|指引|使|予以|产生|促成|造成|引导|造就|促使|酿成|引发|渗透|促进|引起|诱导|引来|促发|引致|诱发|推进|诱致|推动|招致|影响|致使|滋生|归于|作用|使得|决定|攸关|令人|引出|浸染|带来|挟带|触发|关系|渗入|诱惑|波及|诱使)/[d|v]+\s(.*)')
#         result = pattern.findall(sentence)
#         if result:
#             return sentence
# 
#     '''5由因到果前端式模糊'''
#     def ruler5(self, sentence):
#         '''
#         prep:为了、依据、为、按照、因[为]、按、依赖、照、比、凭借、由于
#         prep_model:<Prep...>{Cause},{Effect}
#         '''
#         pattern = re.compile(r'\s?(为了|依据|按照|因为|因|按|依赖|凭借|由于)/[p|c]+\s(.*)[,，]+(.*)')
#         result = pattern.findall(sentence)
#         data = dict()
#         if result:
#             return sentence
# 
# 
#     '''6由因到果居中式模糊'''
#     def ruler6(self, sentence):
#         '''
#         adverb:以免、以便、为此、才
#         adverb_model:{Cause},<Verb|Adverb...>{Effect}
#         '''
#         datas=[]
#         pattern = re.compile(r'(.*)(以免|以便|为此|才)\s(.*)')
#         result = pattern.findall(sentence)
#         data = dict()
#         if result:
#             return sentence
#  
# 
#     '''7由因到果前端式精确'''
#     def ruler7(self, sentence):
#         '''
#         cons1:既[然]、因[为]、如果、由于、只要
#         cons1_model:<Conj...>{Cause},{Effect}
#         '''
#         datas=[]
#         pattern = re.compile(r'\s?(既然?|因|因为|如果|由于|只要)/[p|c]+\s(.*)[,，]+(.*)')
#         result = pattern.findall(sentence)
#         data = dict()
#         if result:
#             return sentence
# 
#     '''8由果溯因居中式模糊'''
#     def ruler8(self, sentence):
#         '''
#         3
#         verb2:根源于、取决、来源于、出于、取决于、缘于、在于、出自、起源于、来自、发源于、发自、源于、根源于、立足[于]
#         verb2_model:{Effect}<Prep...>{Cause}
#         '''
#         datas=[]
#         pattern = re.compile(r'(.*)(根源于|取决|来源于|出于|取决于|缘于|在于|出自|起源于|来自|发源于|发自|源于|根源于|立足|立足于)/[p|c]+\s(.*)')
#         result = pattern.findall(sentence)
#         data = dict()
#         if result:
#             return sentence
#     '''9由果溯因居端式精确'''
#     def ruler9(self, sentence):
#         '''
#         cons3:因为、由于
#         cons3_model:{Effect}<Conj...>{Cause}
#         '''
#         datas=[]
#         pattern = re.compile(r'(.*)是?\s(因为|由于)/[p|c]+\s(.*)')
#         result = pattern.findall(sentence)
#         data = dict()
#         if result:
#             return sentence
# 
#     '''抽取主函数'''
#     def extract_triples(self, sentence):
#         infos =[]
#       #  print(sentence)
#         if self.ruler1(sentence):
#             infos.append(self.ruler1(sentence))
#         elif self.ruler2(sentence):
#             infos.append(self.ruler2(sentence))
#         elif self.ruler3(sentence):
#             infos.append(self.ruler3(sentence))
#         elif self.ruler4(sentence):
#             infos.append(self.ruler4(sentence))
#         elif self.ruler5(sentence):
#             infos.append(self.ruler5(sentence))
#         elif self.ruler6(sentence):
#             infos.append(self.ruler6(sentence))
#         elif self.ruler7(sentence):
#             infos.append(self.ruler7(sentence))
#         elif self.ruler8(sentence):
#             infos.append(self.ruler8(sentence))
#         elif self.ruler9(sentence):
#             infos.append(self.ruler9(sentence))
# 
#         return infos
# 
#     '''抽取主控函数'''
#     def extract_main(self, content):
#         datas=['']
#         subsents1=[]
#         sentences = self.process_content(content)
#         for sentence in sentences:
#             subsents1.append(sentence)
#             subsents = self.fined_sentence(sentence)
#             subsents1.extend(subsents)
#         for sent in subsents1:
#             print(sent)
#             result = self.extract_triples(sent)
#         return datas
# 
#     '''文章分句处理'''
#     def process_content(self, content):
#         return [sentence for sentence in SentenceSplitter.split(content) if sentence]
# 
#     '''切分最小句'''
#     def fined_sentence(self, sentence):
#         return re.split(r'[？！，；]', sentence)

class TripleExtractor:
    def __init__(self):
        self.parser = LtpParser()

    '''文章分句处理, 切分长句，冒号，分号，感叹号等做切分标识'''
    def split_sents(self, content):
        return [sentence for sentence in re.split(r'[？?！!。；，;：:\n\r]', content) if sentence]

    '''利用语义角色标注,直接获取主谓宾三元组,基于A0,A1,A2'''
    def ruler1(self, words, postags, roles_dict, role_index):
        v = words[role_index]
        role_info = roles_dict[role_index]
        if 'A0' in role_info.keys() and 'A1' in role_info.keys():
            s = ''.join([words[word_index] for word_index in range(role_info['A0'][1], role_info['A0'][2]+1) if
                         postags[word_index][0] not in ['w', 'u', 'x'  ] and words[word_index]])
            o = ''.join([words[word_index] for word_index in range(role_info['A1'][1], role_info['A1'][2]+1) if
                         postags[word_index][0] not in ['w', 'u', 'x'] and words[word_index]])
            if s  and o:
                return '1', str(s+v+o)#[s, v, o]#
        elif 'A0' in role_info:
            s = ''.join([words[word_index] for word_index in range(role_info['A0'][1], role_info['A0'][2] + 1) if
                         postags[word_index][0] not in ['w', 'u', 'x']])
            if s:
                return '2', [s,v]
        elif 'A1' in role_info:
            o = ''.join([words[word_index] for word_index in range(role_info['A1'][1], role_info['A1'][2]+1) if
                         postags[word_index][0] not in ['w', 'u', 'x']])
            return '3', str(v+o)#[v,o]
        return '4', []

    '''三元组抽取主函数'''
    def ruler2(self, words, postags, child_dict_list, arcs, roles_dict):
        svos = []
        words1=[]
        for index in range(len(postags)):
            tmp = 1
            # 先借助语义角色标注的结果，进行三元组抽取
            if index in roles_dict:
                flag, triple = self.ruler1(words, postags, roles_dict, index)
                if flag == '1':
                    svos.append(triple)
                    tmp = 0
#                 elif flag=='2':
#                     svos.append(triple)
#                     tmp = 0
                elif flag=='3':
                    svos.append(triple)
                    tmp = 0
            if tmp == 1:
                # 如果语义角色标记为空，则使用依存句法进行抽取
                # if postags[index] == 'v':
                if postags[index]:
                # 抽取以谓词为中心的事实三元组
                    child_dict = child_dict_list[index]
                    # 主谓宾
                    if 'SBV' in child_dict and 'VOB' in child_dict:
                        r = words[index]
                        e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                        e2 = self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
                        svos.append(e1+r+e2)#e1+r+e2)#[e1, r, e2]

                    # 定语后置，动宾关系
                    relation = arcs[index][0]
                    head = arcs[index][2]
                    if relation == 'ATT':
                        if 'VOB' in child_dict:
                            e1 = self.complete_e(words, postags, child_dict_list, head - 1)
                            r = words[index]
                            e2 = self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
                            temp_string = r + e2
                            if temp_string == e1[:len(temp_string)]:
                                e1 = e1[len(temp_string):]
                            if temp_string not in e1:
                                svos.append(e1+r+e2)#)#[e1, r, e2]
                    # 含有介宾关系的主谓动补关系
                    if 'SBV' in child_dict and 'CMP' in child_dict:
                        e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                        cmp_index = child_dict['CMP'][0]
                        r = words[index] + words[cmp_index]
                        if 'POB' in child_dict_list[cmp_index]:
                            e2 = self.complete_e(words, postags, child_dict_list, child_dict_list[cmp_index]['POB'][0])
                            svos.append(e1+r+e2)#e1+r+e2)#[e1, r, e2]                      
        return svos

    '''对找出的主语或者宾语进行扩展'''
    def complete_e(self, words, postags, child_dict_list, word_index):
        child_dict = child_dict_list[word_index]
        prefix = ''
        if 'ATT' in child_dict:
            for i in range(len(child_dict['ATT'])):
                prefix += self.complete_e(words, postags, child_dict_list, child_dict['ATT'][i])
        postfix = ''
        if postags[word_index] == 'v':
            if 'VOB' in child_dict:
                postfix += self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
            if 'SBV' in child_dict:
                prefix = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0]) + prefix

        return prefix +words[word_index] + postfix# 

    '''程序主控函数'''
    def triples_main(self, content):
        sentences = self.split_sents(content)
        svos = []
        svos1=[]
        svos_string=''
        for sentence in sentences:
            words, postags, child_dict_list, roles_dict, arcs = self.parser.parser_main(sentence)
            svo = self.ruler2(words, postags, child_dict_list, arcs, roles_dict)
#             print(svo)
            if str(svo) not in svos_string:
                svos += svo
                svos_string+=str(svo)           
        return svos


# '''测试'''
# def test():
#     content1 = """环境很好，位置独立性很强，比较安静很切合店名，半闲居，偷得半日闲。点了比较经典的菜品，味道果然不错！烤乳鸽，超级赞赞赞，脆皮焦香，肉质细嫩，超好吃。艇仔粥料很足，香葱自己添加，很贴心。金钱肚味道不错，不过没有在广州吃的烂，牙口不好的慎点。凤爪很火候很好，推荐。最惊艳的是长寿菜，菜料十足，很新鲜，清淡又不乏味道，而且没有添加调料的味道，搭配的非常不错！"""
#     content2 = """近日，一条男子高铁吃泡面被女乘客怒怼的视频引发热议。女子情绪激动，言辞激烈，大声斥责该乘客，称高铁上有规定不能吃泡面，质问其“有公德心吗”“没素质”。视频曝光后，该女子回应称，因自己的孩子对泡面过敏，曾跟这名男子沟通过，但对方执意不听，她才发泄不满，并称男子拍视频上传已侵犯了她的隐私权和名誉权，将采取法律手段。12306客服人员表示，高铁、动车上一般不卖泡面，但没有规定高铁、动车上不能吃泡面。
#                 高铁属于密封性较强的空间，每名乘客都有维护高铁内秩序，不破坏该空间内空气质量的义务。这也是乘客作为公民应当具备的基本品质。但是，在高铁没有明确禁止食用泡面等食物的背景下，以影响自己或孩子为由阻挠他人食用某种食品并厉声斥责，恐怕也超出了权利边界。当人们在公共场所活动时，不宜过分干涉他人权利，这样才能构建和谐美好的公共秩序。
#                 一般来说，个人的权利便是他人的义务，任何人不得随意侵犯他人权利，这是每个公民得以正常工作、生活的基本条件。如果权利可以被肆意侵犯而得不到救济，社会将无法运转，人们也没有幸福可言。如西谚所说，“你的权利止于我的鼻尖”，“你可以唱歌，但不能在午夜破坏我的美梦”。无论何种权利，其能够得以行使的前提是不影响他人正常生活，不违反公共利益和公序良俗。超越了这个边界，权利便不再为权利，也就不再受到保护。
#                 在“男子高铁吃泡面被怒怼”事件中，初一看，吃泡面男子可能侵犯公共场所秩序，被怒怼乃咎由自取，其实不尽然。虽然高铁属于封闭空间，但与禁止食用刺激性食品的地铁不同，高铁运营方虽然不建议食用泡面等刺激性食品，但并未作出禁止性规定。由此可见，即使食用泡面、榴莲、麻辣烫等食物可能产生刺激性味道，让他人不适，但是否食用该食品，依然取决于个人喜好，他人无权随意干涉乃至横加斥责。这也是此事件披露后，很多网友并未一边倒地批评食用泡面的男子，反而认为女乘客不该高声喧哗。
#                 现代社会，公民的义务一般分为法律义务和道德义务。如果某个行为被确定为法律义务，行为人必须遵守，一旦违反，无论是受害人抑或旁观群众，均有权制止、投诉、举报。违法者既会受到应有惩戒，也会受到道德谴责，积极制止者则属于应受鼓励的见义勇为。如果有人违反道德义务，则应受到道德和舆论谴责，并有可能被追究法律责任。如在公共场所随地吐痰、乱扔垃圾、脱掉鞋子、随意插队等。此时，如果行为人对他人的劝阻置之不理甚至行凶报复，无疑要受到严厉惩戒。
#                 当然，随着社会的发展，某些道德义务可能上升为法律义务。如之前，很多人对公共场所吸烟不以为然，烟民可以旁若无人地吞云吐雾。现在，要是还有人不识时务地在公共场所吸烟，必然将成为众矢之的。
#                 再回到“高铁吃泡面”事件，要是随着人们观念的更新，在高铁上不得吃泡面等可能产生刺激性气味的食物逐渐成为共识，或者上升到道德义务或法律义务。斥责、制止他人吃泡面将理直气壮，否则很难摆脱“矫情”，“将自我权利凌驾于他人权利之上”的嫌疑。
#                 在相关部门并未禁止在高铁上吃泡面的背景下，吃不吃泡面系个人权利或者个人私德，是不违反公共利益的个人正常生活的一部分。如果认为他人吃泡面让自己不适，最好是请求他人配合并加以感谢，而非站在道德制高点强制干预。只有每个人行使权利时不逾越边界，与他人沟通时好好说话，不过分自我地将幸福和舒适凌驾于他人之上，人与人之间才更趋于平等，公共生活才更趋向美好有序。"""
#     content3 = '''（原标题：央视独家采访：陕西榆林产妇坠楼事件在场人员还原事情经过）
#     央视新闻客户端11月24日消息，2017年8月31日晚，在陕西省榆林市第一医院绥德院区，产妇马茸茸在待产时，从医院五楼坠亡。事发后，医院方面表示，由于家属多次拒绝剖宫产，最终导致产妇难忍疼痛跳楼。但是产妇家属却声称，曾向医生多次提出剖宫产被拒绝。
#     事情经过究竟如何，曾引起舆论纷纷，而随着时间的推移，更多的反思也留给了我们，只有解决了这起事件中暴露出的一些问题，比如患者的医疗选择权，人们对剖宫产和顺产的认识问题等，这样的悲剧才不会再次发生。央视记者找到了等待产妇的家属，主治医生，病区主任，以及当时的两位助产师，一位实习医生，希望通过他们的讲述，更准确地还原事情经过。
#     产妇待产时坠亡，事件有何疑点。公安机关经过调查，排除他杀可能，初步认定马茸茸为跳楼自杀身亡。马茸茸为何会在医院待产期间跳楼身亡，这让所有人的目光都聚焦到了榆林第一医院，这家在当地人心目中数一数二的大医院。
#     就这起事件来说，如何保障患者和家属的知情权，如何让患者和医生能够多一份实质化的沟通？这就需要与之相关的法律法规更加的细化、人性化并且充满温度。用这种温度来消除孕妇对未知的恐惧，来保障医患双方的权益，迎接新生儿平安健康地来到这个世界。'''
#     content4 = '李克强总理今天来我家了,我感到非常荣幸'
#     content5 = ''' 以色列国防军20日对加沙地带实施轰炸，造成3名巴勒斯坦武装人员死亡。此外，巴勒斯坦人与以色列士兵当天在加沙地带与以交界地区发生冲突，一名巴勒斯坦人被打死。当天的冲突还造成210名巴勒斯坦人受伤。
#     当天，数千名巴勒斯坦人在加沙地带边境地区继续“回归大游行”抗议活动。部分示威者燃烧轮胎，并向以军投掷石块、燃烧瓶等，驻守边境的以军士兵向示威人群发射催泪瓦斯并开枪射击。'''
#     extractor = TripleExtractor()
#     svos = extractor.triples_main(content2)
#     print('svos', svos)
# 
# test()
if __name__ == '__main__':
    extractor1 = TripleExtractor()
    mongo_con=MongoClient('172.20.66.56', 27017)
    db=mongo_con.Causal_event
    collection=db.sj_extraction
    #extractor = CausalitySentencesExractor()
    path = r'E:\\Causal_events\\forum50_articles_causality_extract'
    #sentence="我爱你,中国"
    files = os.listdir(path)
#     i=1251
    for file in files:
#         i+=1
#         while(file=='税务文明的核心是依法治税(2002.10.25).txt.csv'):
#             print(i)
        pathname = os.path.join(path, file)
        print(file)
        #准确获取一个txt的位置，利用字符串的拼接
        txt_path = pathname
        f = open(txt_path,'r',encoding='utf-8')
        article_causality_sentence=pd.read_csv(f).drop_duplicates(subset=['原因','结果'])
        #print(datas)
        yuanyin=[]
        jieguo=[]
        tag1=[]
        for index,i in article_causality_sentence.iterrows():
            svos=1
            yuanyin_svos = extractor1.triples_main(i['原因'])#原因三元组对
        
            tag=i['标签']#事件标签
            tag1.append(tag)
            jieguo_svos = extractor1.triples_main(i['结果'])#结果三元组对
            if len(yuanyin_svos)==0:
                yuanyin_svos.append(i['原因'])
                svos=0
            if len(jieguo_svos)==0:
                jieguo_svos.append(i['结果'])
                svos=0
            '''
            事件提取并去重
            '''
            yuanyin_svos_sj=[]
            jieguo_svos_sj=[]
            print(yuanyin_svos)
            for k in yuanyin_svos:
                yuanyin_svos1=[]
                yuanyin_svos1+=yuanyin_svos
#                 print('....:',yuanyin_svos1)
                yuanyin_svos1.remove(k)
                if str(k) not in str(yuanyin_svos1).replace("'", ''):
                    if len(str(k))>=4:
                        yuanyin_svos_sj.append(k)
            yuanyin_svos_sj1=str(yuanyin_svos_sj).replace('[','').replace(']','').replace("'", '').replace("\xa0", '')
            yuanyin.append(yuanyin_svos_sj1)
            for j in jieguo_svos:
                jieguo_svos1=[]
                jieguo_svos1+=jieguo_svos
                jieguo_svos1.remove(j)
                print(j)
                if str(j) not in str(jieguo_svos1).replace("'", ''):
                    if len(str(j))>=4:
                        jieguo_svos_sj.append(j)
            jieguo_svos_sj1=str(jieguo_svos_sj).replace('[','').replace(']','').replace("'", '').replace("\xa0", '')
            jieguo.append(jieguo_svos_sj1) 
            print('原因:'+yuanyin_svos_sj1) 
            print('结果:'+jieguo_svos_sj1)
            if yuanyin_svos_sj1 and jieguo_svos_sj1:
                        collection.insert({'栏目':'50人论坛财经评论','文件名':i['文件名'],'原因事件':yuanyin_svos_sj1,'结果事件':jieguo_svos_sj1,'标签':tag,'svos':svos})
        article_causality_sentence['原因事件']=yuanyin
        article_causality_sentence['结果事件']=jieguo
        article_causality_sentence['标签']=tag1
        article_causality_sentence.to_csv('E:\\Causal_events\\forum50_articles_sj_extract\\'+str(file))
#         article_causality_sentence.to_csv('E:\\Causal_events\\sina_economics_sj_extraction.csv',mode='a')
               
            
    
    

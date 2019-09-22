from bs4 import BeautifulSoup
from urllib.request import urlopen
import string
import re
baseWikipediaURL = 'https://en.wikipedia.org/wiki/'

# An array of dictionaries
# Each dictionary should hold every word found in a given wikipedia webpage
# The key should be the word and the value should be its number of occurrences
dictWordArray = []
baseTotalDict = {}
commonWordsDict = {}

interests = ["augmented_reality", "3d_printing", "Decentralized_autonomous_organization", "blockchain", "nuclear_fusion", "shipbuilding"]

def getStopWords():
    stopwords = ['a', 'about', 'above', 'across', 'after', 'afterwards']
    stopwords += ['again', 'against', 'all', 'almost', 'alone', 'along']
    stopwords += ['already', 'also', 'although', 'always', 'am', 'among']
    stopwords += ['amongst', 'amoungst', 'amount', 'an', 'and', 'another']
    stopwords += ['any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere']
    stopwords += ['are', 'around', 'as', 'at', 'back', 'be', 'became']
    stopwords += ['because', 'become', 'becomes', 'becoming', 'been']
    stopwords += ['before', 'beforehand', 'behind', 'being', 'below']
    stopwords += ['beside', 'besides', 'between', 'beyond', 'bill', 'both']
    stopwords += ['bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant']
    stopwords += ['co', 'computer', 'con', 'could', 'couldnt', 'cry', 'de']
    stopwords += ['describe', 'detail', 'did', 'do', 'done', 'down', 'due']
    stopwords += ['during', 'each', 'eg', 'eight', 'either', 'eleven', 'else']
    stopwords += ['elsewhere', 'empty', 'enough', 'etc', 'even', 'ever']
    stopwords += ['every', 'everyone', 'everything', 'everywhere', 'except']
    stopwords += ['few', 'fifteen', 'fifty', 'fill', 'find', 'fire', 'first']
    stopwords += ['five', 'for', 'former', 'formerly', 'forty', 'found']
    stopwords += ['four', 'from', 'front', 'full', 'further', 'get', 'give']
    stopwords += ['go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her']
    stopwords += ['here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers']
    stopwords += ['herself', 'him', 'himself', 'his', 'how', 'however']
    stopwords += ['hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed']
    stopwords += ['interest', 'into', 'is', 'it', 'its', 'itself', 'keep']
    stopwords += ['last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made']
    stopwords += ['many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine']
    stopwords += ['more', 'moreover', 'most', 'mostly', 'move', 'much']
    stopwords += ['must', 'my', 'myself', 'name', 'namely', 'neither', 'never']
    stopwords += ['nevertheless', 'next', 'nine', 'no', 'nobody', 'none']
    stopwords += ['noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of']
    stopwords += ['off', 'often', 'on','once', 'one', 'only', 'onto', 'or']
    stopwords += ['other', 'others', 'otherwise', 'our', 'ours', 'ourselves']
    stopwords += ['out', 'over', 'own', 'part', 'per', 'perhaps', 'please']
    stopwords += ['put', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed']
    stopwords += ['seeming', 'seems', 'serious', 'several', 'she', 'should']
    stopwords += ['show', 'side', 'since', 'sincere', 'six', 'sixty', 'so']
    stopwords += ['some', 'somehow', 'someone', 'something', 'sometime']
    stopwords += ['sometimes', 'somewhere', 'still', 'such', 'system', 'take']
    stopwords += ['ten', 'than', 'that', 'the', 'their', 'them', 'themselves']
    stopwords += ['then', 'thence', 'there', 'thereafter', 'thereby']
    stopwords += ['therefore', 'therein', 'thereupon', 'these', 'they']
    stopwords += ['thick', 'thin', 'third', 'this', 'those', 'though', 'three']
    stopwords += ['three', 'through', 'throughout', 'thru', 'thus', 'to']
    stopwords += ['together', 'too', 'top', 'toward', 'towards', 'twelve']
    stopwords += ['twenty', 'two', 'un', 'under', 'until', 'up', 'upon']
    stopwords += ['us', 'use', 'very', 'via', 'was', 'we', 'well', 'were', 'what']
    stopwords += ['whatever', 'when', 'whence', 'whenever', 'where']
    stopwords += ['whereafter', 'whereas', 'whereby', 'wherein', 'whereupon']
    stopwords += ['wherever', 'whether', 'which', 'while', 'whither', 'who']
    stopwords += ['whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with']
    stopwords += ['within', 'without', 'would', 'yet', 'you', 'your']
    stopwords += ['yours', 'yourself', 'yourselves']
    stopwords += ['example', 'allows', 'different', 'called', 'require', 'associated']
    stopwords += ['enabling', 'enabled', 'takes', 'lack', 'projects', 'following']
    stopwords += ['general', 'given', 'prevent', 'means', 'large', 'known', 'open']
    stopwords += ['number', 'multiple', 'need', 'new']
    return stopwords

def wordListToFreqDict(wordlist):
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(zip(wordlist,wordfreq))

def sortFreqDict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux

def removeStopwords(wordlist):
    return [w for w in wordlist if w not in getStopWords()]

def mergeListDictFrequencies(rootDict, tmpDict):
    for (count, word) in tmpDict:
        if word in rootDict:
            rootDict[word] += count
        else:
            rootDict[word] = count

    return rootDict

def mergeDictFrequencies(rootDict, tmpDict):
    for (key, value) in tmpDict.items():
        if key in rootDict:
            rootDict[key] += value
        else:
            rootDict[key] = value

    return rootDict

def mergeDictCommonWords(firstDict, secondDict):
    tmpDict = {}
    if not firstDict:
        return secondDict
    for (key, value) in secondDict.items():
        if key in firstDict:
            tmpDict[key] = value + firstDict[key]
    return tmpDict

for interest in interests:
    rootTopicDictionary = {}
    page = urlopen(baseWikipediaURL + interest)
    soup = BeautifulSoup(page, 'html.parser')
    bodyElement = soup.find("div", {"class":"mw-parser-output"})
    bodyText = bodyElement.find_all("p")
    for p in bodyText:
        initialText = p.get_text().lower()
        removedBrackets = re.sub("[\[].*?[\]]", "", initialText)
        scrubbedWordList = removedBrackets.translate(str.maketrans('','',string.punctuation)).split()
        listNoCommonWords = removeStopwords(scrubbedWordList)
        dictionary = wordListToFreqDict(listNoCommonWords)
        sortedDict = sortFreqDict(dictionary)
        rootTopicDictionary = mergeListDictFrequencies(rootTopicDictionary, sortedDict)

    dictWordArray += [rootTopicDictionary]

commonWordsDict = {}
for value in dictWordArray:
    commonWordsDict = mergeDictCommonWords(commonWordsDict, value)
    baseTotalDict = mergeDictFrequencies(baseTotalDict, value)

MIN_FREQUENCY = 1
#print(sorted(dict((k, v) for k, v in baseTotalDict.items() if v >= MIN_FREQUENCY).items(), key = lambda kv:(kv[1], kv[0])))
print(sorted(dict((k, v) for k, v in commonWordsDict.items() if v >= MIN_FREQUENCY).items(), key = lambda kv:(kv[1], kv[0])))

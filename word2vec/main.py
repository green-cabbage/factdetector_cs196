# import modules & set up logging
import gensim, logging
from gensim.models.word2vec import Word2Vec
import json
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

'''
class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()
'''

##sentences = MySentences('/some/directory')

sentences = [['first', 'sentence'], ['second', 'sentence']]
# train word2vec on the two sentences
model = Word2Vec.load_word2vec_format('./googlenews.bin', binary=True)
#model = gensim.models.Word2Vec(sentences, min_count=1,size=200,workers=4)
#print(model.wv['computer'])
a=model.wv['computer']
b= a.tolist()
with open('result.json', 'w') as fp:
    json.dump(b, fp)
##a=open("30words.txt")
##model = Word2Vec.load_word2vec_format('khkjhjkhjhjk     ', binary=False)
##C:\Users\HyeonSeo\PycharmProjects\word2vec\30words.txt
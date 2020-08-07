import numpy as np
np.random.seed(1234)
import math
import scipy.stats

EPS = 1e-06

class semantic_matching:
    def __init__(self):
        super(semantic_matching, self).__init__()

    def cos_sim(self, vecA, vecB):
        print("in cos")
        if vecA.shape != vecB.shape:\
            raise RuntimeError("array {} shape not match {}".format(vecA.shape, vecB.shape))
        if vecA.ndim == 1:
            vecA_norm = np.linalg.norm(vecA)
            vecB_norm = np.linalg.norm(vecB)
        elif vecA.ndim == 2:
            vecA_norm = np.linalg.norm(vecA, axis=1, keepdims=True)
            vecB_norm = np.linalg.norm(vecB, axis=1, keepdims=True)
        else:
            raise RuntimeError("array dimensions {} not right".format(vecA.ndim))
        sim = np.dot(vecA, vecB.T)/(vecA_norm * vecB_norm)
        return sim


    def distEclud(self, vecA, vecB):
        return np.sqrt(np.sum(np.power((vecA - vecB), 2)))


    def similar(self, stockEmb, stockTopic, textTopic):
        """
        计算股票主题和文章主题相似性
        :param stockEmb: [1,n]->vector
        :param stockTopic: [k,n]->matrix
        :param textTopic:[k,n]->matrix
        :return: sim
        """
        coe1 = [self.cos_sim(stockEmb,stockTopic[n]) for n in range(stockTopic.shape[0])]
        coe2 = [self.cos_sim(stockEmb,textTopic[n]) for n in range(textTopic.shape[0])]
        aveEmbstockT = np.zeros(shape=(1,stockTopic.shape[1] ))
        aveEmbtextT = np.zeros(shape=(1,textTopic.shape[1] ))
        for i in range(stockTopic.shape[0]):
            aveEmbstockT = aveEmbstockT + coe1[i]/np.sum(coe1)*stockTopic[i]        
        for j in range(textTopic.shape[0]):
            aveEmbtextT = aveEmbtextT + coe2[j]/np.sum(coe2)*textTopic[j]
        result = self.cos_sim(aveEmbstockT,aveEmbtextT)
        return result

    def kullback_leibler_divergence(self, vecA, vecB):
        """
        计算两个分布之间的KL散度
        :param vecA: [1,n]->vector: distributionA
        :param vecA: [1,n]->vector: distributionB
        :return: KL_divergence
        """
        if vecA.shape != vecB.shape:
            raise RuntimeError("array {} shape not match {}".format(vecA.shape, vecB.shape))
        KL = 0.0
        length = vecA.shape[0]
        for i in range(length):
            if vecB[i] < EPS:
                vecB[i] = EPS
            KL += vecA[i] * np.log(vecA[i] / vecB[i])
        return KL

    def jensen_shannon_divergence(self, vecA, vecB):
        '''
        计算两个分布之间的JS散度
        :param vecA: [1,n]->vector: distributionA
        :param vecA: [1,n]->vector: distributionB
        :return: JS_divergence
        '''
        if vecA.shape != vecB.shape:
            raise RuntimeError("array {} shape not match {}".format(vecA.shape, vecB.shape))
        length = vecA.shape[0]
        for i in range(length):
            if vecA[i] < EPS:
                vecA[i] = EPS
            if vecB[i] < EPS:
                vecB[i] = EPS
        vec_mean = (vecA + vecB)*0.5
        jsd = self.kullback_leibler_divergence(vecA,vec_mean) + self.kullback_leibler_divergence(vecB,vec_mean)
        return jsd

    def hellinger_distance(self, vecA, vecB):
        '''
        计算两个分布之间的hellinger_distance
        :param vecA: [1,n]->vector: distributionA
        :param vecA: [1,n]->vector: distributionB
        :return: hellinger_distance
        '''
        if vecA.shape != vecB.shape:
            raise RuntimeError("array {} shape not match {}".format(vecA.shape, vecB.shape))
        length = vecA.shape[0]
        hellinger = 0
        for i in range(length):
            temp = math.sqrt(vecA[i]) - math.sqrt(vecB[i])
            hellinger += temp * temp
        result = math.sqrt(hellinger) * 0.7071067812
        return result

    def wasserstein_distance(self, vecA, vecB):
        '''
        计算两个分布之间的wasserstein_distance
        :param vecA: [1,n]->vector: distributionA
        :param vecA: [1,n]->vector: distributionB
        :return: wasserstein_distance
        '''
        pass


def likelihood_based_similarity():
    '''
    计算使用短文本到长文本之间的似然值表示之间的相似度
    :param vecA: [1,n]->vector: distributionA
    :param vecA: [1,n]->vector: distributionB
    :return: wasserstein_distance
    '''
    pass

if __name__ == "__main__":
    # 随机生成两个离散型分布
    x = [np.random.randint(1, 11) for i in range(10)]
    px = x / np.sum(x)
    # print(px)
    y = [np.random.randint(1, 11) for i in range(10)]
    py = y / np.sum(y)
    # print(py)
    # 利用scipy API进行计算
    # scipy计算函数可以处理非归一化情况，因此这里使用
    # scipy.stats.entropy(x, y)或scipy.stats.entropy(px, py)均可
    KL = scipy.stats.entropy(x, y) 
    print(KL)
    
    measure = semantic_matching()
    print(measure.kullback_leibler_divergence(px, py))
    print(measure.jensen_shannon_divergence(px,py))
    print(measure.hellinger_distance(px, py))

    print(1 - abs(measure.cos_sim(px,py)))
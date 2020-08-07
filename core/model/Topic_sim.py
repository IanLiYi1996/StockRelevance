#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np

# def cos_sim(vector_a, vector_b):
#     """
#     计算两个向量之间的余弦相似度
#     :param vector_a: 向量 a 
#     :param vector_b: 向量 b
#     :return: sim
#     """
#     vector_a = np.mat(vector_a)
#     vector_b = np.mat(vector_b)
#     num = float(vector_a * vector_b.T)
#     denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
#     cos = num / denom
#     sim = 0.5 + 0.5 * cos
#     return sim

def cos_sim(vecA, vecB):
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


def distEclud(vecA, vecB):
    return np.sqrt(np.sum(np.power((vecA - vecB), 2)))


def similar(stockEmb, stockTopic, textTopic):
    """
    计算股票主题和文章主题相似性
    :param stockEmb: [1,n]->vector
    :param stockTopic: [k,n]->matrix
    :param textTopic:[k,n]->matrix
    :return: sim
    """
    coe1 = [cos_sim(stockEmb,stockTopic[n]) for n in range(stockTopic.shape[0])]
    coe2 = [cos_sim(stockEmb,textTopic[n]) for n in range(textTopic.shape[0])]
    aveEmbstockT = np.zeros(shape=(1,stockTopic.shape[1] ))
    aveEmbtextT = np.zeros(shape=(1,textTopic.shape[1] ))
    for i in range(stockTopic.shape[0]):
        aveEmbstockT = aveEmbstockT + coe1[i]/np.sum(coe1)*stockTopic[i]        
    for j in range(textTopic.shape[0]):
        aveEmbtextT = aveEmbtextT + coe2[j]/np.sum(coe2)*textTopic[j]
    result = cos_sim(aveEmbstockT,aveEmbtextT)
    return result

if __name__ == "__main__":
    a = np.array([1,2,3])
    b = np.array([-0.26959  ,  0.029244 ,  0.13901])
    c = np.array([6,7,8,9,10,11])
    print(abs(cos_sim(a,b)))
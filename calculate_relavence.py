def getStockdict():
    stock_dict = {}
    stock_topic = {}
    with open('C:/Users/liyi_intern/Documents/Codes/nlp-stock-relevance/stock_topic.txt', 'r', encoding='utf-8') as stock:
        for line in stock.readlines():
            items = line.strip().split(',')
            stock_dict[items[0]] = items[1]
            stock_topic[items[1]] = items[2].replace('2_','').split('|')
        print(stock_topic)

if __name__ == '__main__':
    getStockdict()
    with open('C:/Users/liyi_intern/Documents/Codes/nlp-stock-relevance/test_stock.csv', 'r', encoding='utf-8') as data:
        for line in data.readlines():
            items = line.strip().split(',')
            stock,title, text = items[0], items[2], items[3]
            print(stock,title,text)
            
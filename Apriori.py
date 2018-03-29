import sys
from collections import defaultdict
from itertools import chain, combinations


def init():
    #init TDB
    _transactions = list()
    f = open(sys.argv[2], 'r')
    inputStrings = f.readlines()
    for inputString in inputStrings:
        inputString = inputString[:-1]
        _localFrozenSet = frozenset(inputString.split("\t"))
        _localSet = set()
        for item in _localFrozenSet:
            _localSet.add(int(item))
        _transactions.append(frozenset(_localSet))

    #init _minSup
    _minSup = float(sys.argv[1])

    #init _CSet
    _Cset = set()
    for transaction in _transactions:
        for item in transaction:
            _Cset.add(item)
    return _transactions, _minSup, _Cset

def joinSet(itemSet, length):
    returnSet=set()
    for i in itemSet:
        for j in itemSet:
            if len(set(i).union(set(j)))==length:
                returnSet.add(frozenset(set(i).union(set(j))))
    return returnSet


def prune(itemSet, transactions, minSup, freqSet):
    returnSet=set()
    for item in itemSet:
        for transaction in transactions:
            if set(item).issubset(transaction):
                freqSet[item]+=1
    for item in itemSet:
        if (float(freqSet[item])/len(transactions))*100>=minSup:
            returnSet.add(item)
    return returnSet

def makeSubset(iterable):
    xs = list(iterable)
    return chain.from_iterable(combinations(xs,n) for n in range(len(xs)+1))

def runApriori():
    Cset = set()
    Lset = set()
    transactions = list()
    minSup = int()
    freqSet = defaultdict(int)
    totalSet = dict()

    transactions, minSup, Cset=init()
    for item in Cset:
        for transaction in transactions:
            if item in transaction:
                tSet=frozenset({item})
                freqSet[tSet]+=1
    localSet = set()
    for item in Cset:
        tSet = frozenset({item})
        if freqSet[tSet] >= minSup:
            Lset.add(item)
            localSet.add(tSet)
    totalSet[1] = localSet
    Lset = localSet
    k=2
    while(len(Lset) != 0):
        if k!=2:
            totalSet[k-1] = Lset
        Cset = joinSet(Lset, k)
        Lset = prune(Cset, transactions, minSup, freqSet)
        Lset = set(Lset)
        k=k+1
    def getSupport(item):
        return float(freqSet[item])/len(transactions)

    for key, value in totalSet.items():
        for item in value:
            if len(item)>1:
                for subsetTuple in list(makeSubset(item)):
                    if (len(subsetTuple)>0) & (len(subsetTuple)!=len(item)):
                        subset=frozenset(subsetTuple)
                        remain=frozenset(item).difference(subset)
                        _support=getSupport(item)*100
                        _confidence=float(freqSet[item])/freqSet[subset]*100
                        support=round(float(_support),2)
                        confidence=round(_confidence,2)

                        output=str(set(subset))+"\t"+str(set(remain))+"\t"+str(support)+"\t"+str(confidence)+"\n"

                        with open(sys.argv[3],'a') as f:
                            f.writelines(output)


if __name__ == "__main__":
    runApriori()


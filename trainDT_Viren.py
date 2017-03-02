# trainDT.py: Decision Tree Trainer
#
# Author: Virendra Rajpurohit
# 

import sys
import operator
import matplotlib.pylab as plt
import matplotlib.patches as patches
import math
import csv
import pickle
import copy

d=0
# readFile : function reads the input .csv file and returns samples list	
def readFile(filename):
    print("Reading file : ", filename)
    samples=[]
    with open(filename) as inFile:
        rline = csv.reader(inFile)
        for row in rline:
            if (row):
                sNode=smpl(float(row[0]),float(row[1]),int(row[2]))
                samples.append(sNode)
    return samples
 
class dtreeNode:
    def __init__(self,clas=0,root=None,val=0,IG=0,level=0,left=None,right=None,s=[]):
        self.root=root
        self.left=left
        self.right=right        
        self.val=val
        self.IG=IG
        self.level=level
        self.s=s
        self.clas=clas
  
class DT:
    #tree information
    s=[]
    levels=0
    leafNodes=0
    parent=''
    
    def display_node(self,node,tab):
        # Number of Nodes
        print(str(tab)+str(" "*tab), end='')
        print(" Number of nodes " + str(len(node.s)), end='')
        print()
        tab= tab +1
        if(node.IG==0):
            #print("IG==0",node.root,node.val)
            return (node.clas,node.level,node.root)
        else:
            print(str(tab)+str(" "*tab), end='')
            print(str(" "*tab)+"Left Child ",end='')
            print(self.display_node(node.left,tab),end='')
            print()
            print(str(tab)+str(" "*tab), end='')
            print(str(" "*tab)+"Right Child ",end='')
            print(self.display_node(node.right,tab),end='')

    def reChiPrun(self,tree):
        #print("Chi - squared prunning recursivly")
        if(tree.left):                
            if(tree.left.IG==0):
                l=tree.left
                r=tree.right
                if checkSign(tree.s,l.s,r.s):
                    #print("checked node is relevant, stopped prunning")
                    return
                else:
                    self.root=None
                    self.s=[]
            else:
                self.reChiPrun(tree.left)
                self.reChiPrun(tree.right)
        else:
            return
            
class smpl:
    def __init__(self,A,B,Class):
        self.A=A
        self.B=B
        self.Class=Class

def isEmpty(samples):
    if (len(samples)-1)<=0:
        return True
    else:
        return False
    
def countClass(samples):
    c=[0,0,0,0,0]
    for s in samples:
            c[s.Class]+=1
    return c            
        
def sameClass(samples):
    classCounts=[]
    classCounts=countClass(samples)
    for i in range(1,5):
        if classCounts[i]==len(samples):
            return True,i
    return False,mode(samples)
      
def mode(samples):
    c=countClass(samples)
    return c.index(max(c))

def nSort(samples,attrval):
    if(attrval=="A"):
        new_samples=sorted(samples, key=operator.attrgetter('A'))
    else:
        new_samples=sorted(samples, key=operator.attrgetter('B'))
    return new_samples
      
def splitSamples(samples,attrval,spval):
    leftS=[]
    rightS=[]
    for i in samples:
        if(attrval=='A'):
            if i.A<spval:
                leftS.append(i)
            else:
                rightS.append(i)
        else:
            if i.B<spval:
                leftS.append(i)
            else:
                rightS.append(i)
    return leftS, rightS

def cEntropy(samples):
    total=len(samples)
    c=[]
    p=[0,0,0,0,0]
    entropy=0
    c=countClass(samples)
    for i in range(1,5):
        p[i]=c[i]/total
        if(p[i]!=0):
            entropy += - p[i]*math.log(p[i], 2)
    return entropy
    
def computeIG(samples,left,right):
    IG = 0   
    total=len(samples)
    nl=len(left)
    nr=len(right)
    entropy=cEntropy(samples)
    entropyLeft=cEntropy(left)
    entropyRight=cEntropy(right)
    IG=entropy-((nl/total)*entropyLeft + (nr/total)*entropyRight)
    return IG
glist=[]   
dl=0 
def chooseAttr(samples,attrs):
    global glist
    global dl
    iG=0
    splitVal=0
    bestAttr="noValue"
    for attribute in attrs:
        new_attr = nSort(samples,attribute)
        for i in range(len(new_attr)-1):
            if(attribute=='A'):
                splitPtr=(new_attr[i].A+new_attr[i+1].A)/2
            else:
                splitPtr=(new_attr[i].B+new_attr[i+1].B)/2
            left,right=splitSamples(samples,attribute,splitPtr)
            infoGain=computeIG(samples,left,right)
            if (infoGain>iG):
                iG=infoGain
                splitVal=splitPtr
                bestAttr=attribute
                l = left
                r = right
    print(splitVal, bestAttr,len(l),len(r))
    leng=len(glist)
    #print("glist len",leng)
    if(leng==0):
        glist.append(['c',dl,splitVal, bestAttr,len(l),len(r)])
    else:
        dl+=1
        curLis=glist[dl-1]
        if(curLis[4]+curLis[5]==len(l)):
            glist.append(['l',dl,splitVal, bestAttr,len(l),len(r)])
        else:
            glist.append(['r',dl,splitVal, bestAttr,len(l),len(r)])   
    
    return splitVal, bestAttr,iG,l,r

def nzero(c):
    return (i for i in c if i!=0)
def classCnt(c):
    lis=list(nzero(c))
    #print("Non-Zero list",lis)
    return lis
    
def checkSign(samples,left,right):
    bCheck=False
    #print("Chi prunning")
    dof=[0,0.004,0.103,0.352]
    c=countClass(samples)
    lis=classCnt(c)
    deg=(len(lis))-1
    thval=dof[deg]
    #print("degree , thval",deg,thval)
    #Actual counts   
    cl=countClass(left)
    cr=countClass(right)
    total=len(samples)
    sumL=len(left)
    sumR=len(right)
    chiSqX=0
    #expected counts
    ceL=[0,0,0,0,0]
    ceR=[0,0,0,0,0]
    for i in range(1,len(lis)):
        for j in range(1,3):
            if(j==1):
                ceL[i]=(cl[i]+cr[i])*sumL/total
                if(ceL[i]!=0):
                    chiSqX+=(cl[i]-ceL[i])**2/ceL[i]
            if(j==2):
                ceR[i]=(cl[i]+cr[i])*sumR/total
                if(ceR[i]!=0):
                    chiSqX+=(cl[i]-ceR[i])**2/ceR[i]
    #print("Chi Sq :",chiSqX,)
    if(chiSqX>thval):
        #print("chi>thval------------------------")
        bCheck=True
    #print("bCheck: relevant node: ",chiSqX, bCheck, thval)
    return bCheck              
 
#Decision tree algorithm implementation  
def DTL_Chi(samples,attrs,default):
    #print("DTL: ",len(samples))
    global d
    global tree
    global rlevel
    sameClassification, classification=sameClass(samples)
    if isEmpty(samples):
        return dtreeNode(default)
    elif sameClassification:
        return dtreeNode(classification)
    else:
        spval, best, IG, l, r = chooseAttr(samples,attrs)
        #if(spval==0):
            
        leftSamples, rightSamples = splitSamples(samples,best,spval)
        pcheck=checkSign(samples,l,r)
        #print("pcheck _ ",pcheck )
        if(pcheck):
            node = dtreeNode(0,best,spval,IG,d,l,r,samples)
        else:
            #print("pcheck _ ",pcheck ,end='')
            #print("------------------Node prunned")
            return dtreeNode(mode(samples))

        node.s = copy.deepcopy(samples)
        node.d = d+1
        node.root  =best
        node.val = spval
        node.l = copy.deepcopy(leftSamples)
        node.r = copy.deepcopy(rightSamples)
        node.left = DTL_Chi(leftSamples,attrs,mode(leftSamples))
        node.right = DTL_Chi(rightSamples,attrs,mode(rightSamples))
        return  copy.deepcopy(node)
        
def DTL(samples,attrs,default):
    #print("DTL: ",len(samples))
    global valb
    global tree
    global rlevel
    sameClassification, classification=sameClass(samples)
    if isEmpty(samples):
        return dtreeNode(default)
        
    elif sameClassification:
        return dtreeNode(classification)
    else:
        spval, best, IG, l, r = chooseAttr(samples,attrs)
        rlevel+=1
        if(spval==0):
            return
        leftSamples, rightSamples = splitSamples(samples,best,spval)
        # create Node
        node = dtreeNode(0,best,spval,IG,d,l,r,samples)
        node.s = copy.deepcopy(samples)
        node.d = d+1
        node.root  =best
        node.val = spval
        node.l = copy.deepcopy(leftSamples)
        node.r = copy.deepcopy(rightSamples)
        node.left = DTL(leftSamples,attrs,mode(leftSamples))
        node.right = DTL(rightSamples,attrs,mode(rightSamples))
        return  copy.deepcopy(node)
    #return tree
# main function
def plot1(lis,data):    
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_xlim(0.0,1.0)
    ax.set_ylim(0.0,1.0)
    mark=['o','^','*','+','x','s','d','p','h']
    colr=["red","green","blue","black","red","green","blue","black","red","green","blue","black"]
    for i in range(len(lis)-1):
        el=lis[i]
        if(el[3]=='A'):
            x=el[2]
            y=0.0
            h=1.0-y
            w=1.0-x
        else:
            x=0.0
            y=el[2]
            h=1.0-x
            w=1.0-y
        #print("list ele :",i,el)
        p=patches.Rectangle((x,y), h,w, fill=False,
                edgecolor=colr[i])
        ax.add_patch(p)
    for i in data:
        j=i.Class-1
        ax.scatter(i.A,i.B,color=colr[j],marker=mark[j])
    fig.savefig('dtee1.png')
def plot2(data):    
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_xlim(0.0,1.0)
    ax.set_ylim(0.0,1.0)
    mark=['o','^','*','+','x','s','d','p','h']
    colr=["red","green","blue","black","red","green","blue","black","red","green","blue","black"]
    for i in data:
        j=i.Class-1
        ax.scatter(i.A,i.B,color=colr[j],marker=mark[j])
    fig.savefig('dtee1.png')
def main():
    global glist
    print('\nDecision Tree Training')
    # read data from file and return to samples list
    samples=readFile('train_data.csv')
    attrs=['A','B']
    default=mode(samples)
    x=DT()
    y=DT()
    x.parent=DTL(samples,attrs,default)
    pickle.dump( x.parent, open( "dtreefile.p", "wb" ) )
    x.display_node(x.parent,0)
    #plot1(glist,samples)

    print("Decision Tree with CHi-Squared Prunning")
    y.parent=DTL_Chi(samples,attrs,default)
    pickle.dump( y.parent, open( "dtreeChi.p", "wb" ) )
    y.display_node(x.parent,0)
    #plot1(glist[9:],samples)
    #testData=readFile('test_data.csv')
    
    #plot2(samples)
    #plot2(testData)
main()
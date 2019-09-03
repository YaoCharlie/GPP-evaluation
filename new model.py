#-*- coding:utf-8 -*-
#!/usr/bin/python3.4
import math
#def Par(ki,par):
#    fpar=par/(ki+par)
#    return fpar
def Par(p1,p2,p3,p4,par):
    down5=1.0+p4*par
    if down5==0:
        down5=0.000001
    fp=(p3*par)/down5
    if fp<0:
        fp=0
    down6=1.0+p1*math.exp(p2*(fp**0.5))
    if down6==0:
        down6=0.000001
    fpar=1.0/down6
    if fpar<0:
        fpar=0
    if fpar>1:
        fpar=1
    return fpar

def Temp(Q,Tr,T):
    ftemp=math.pow(Q,(T-Tr)/10)
    if ftemp<0:
        ftemp=0
    if ftemp>1:
        ftemp=1
    return ftemp
     
def Kleaf(a,b,c,Min,EET):
    kleaf0=Min
    EETmax=max(EET)
    L=[]
    for i in range(len(EET)):
        kleaf=a*(EET[i]/EETmax)+b*kleaf0+c
        if kleaf>1.0:
            kleaf=1.0
        if kleaf<Min:
            kleaf=Min    
        kleaf0=kleaf
        L.append(kleaf)
    kleafmax=max(L)
    for i in range(len(L)):
        if kleafmax<1.0:
            L[i]=L[i]/kleafmax
        if L[i]>1.0:
            L[i]=1.0
        if L[i]<Min:
            L[i]=Min
    return L
#def sm(Smax,Smin,Sopt,s):
#    fsm=((s-Smin)*(s-Smax))/(((s-Smin)*(s-Smax))-(s-Sopt)**2)
#    if fsm<0.0:
#        fsm=0.001
#    if fsm>1.0:
#        fsm=1.0
#    if fsm <0�?
#        fsm=0
 #   return fsm

def CO2(kc,co2):
    fco2=co2/(kc+co2)
    return fco2

def FOLIAGE(m1,m2,m3,m4,Cv):
    down1=1.0+m4*Cv
    if down1==0:
        down1=0.000001
    fcv=(m3*Cv)/down1
    if fcv<0:
        fcv=0
    down2=1.0+m1*math.exp(m2*(fcv**0.5))
    if down2==0:
        down2=0.000001
    ffoliage=1.0/down2
    if ffoliage<0:
        ffoliage=0
    if ffoliage>1:
        ffoliage=1
    return ffoliage

#计算Rm=Kr*Cv*math.exp(0.0693T)和Rg,Lc
def rm(Kr,Cv,temp):
    frm=Kr*Cv*math.exp(0.0693*temp)
    return frm

def rg(gpp,rm):
    if gpp>rm:
        frg=0.2*(gpp-rm)
    else:
        frg=0
    return frg

def lc(Cv,KFALL):
    flc=Cv*KFALL
    return flc

#Cmax,ki,Tmax,Tmin,Topt,a,b,c,Min,Smax,Smin,Sopt,kc
f_space = open(r"./new param.txt","r")
line_space = f_space.readlines()
Cmax=line_space[1].split(",")[0]
#KI=line_space[1].split(",")[1]
#TMAX=line_space[1].split(",")[1]
#TMIN=line_space[1].split(",")[2]
#TOPT=line_space[1].split(",")[3]
Q=line_space[1].split(",")[1]
Tr=line_space[1].split(",")[2]
t3=line_space[1].split(",")[3]
t4=line_space[1].split(",")[4]
A=line_space[1].split(",")[5]
B=line_space[1].split(",")[6]
C=line_space[1].split(",")[7]
MIN=line_space[1].split(",")[8]
m1=line_space[1].split(",")[9]
m2=line_space[1].split(",")[10]
m3=line_space[1].split(",")[11]
m4=line_space[1].split(",")[12]
KC=line_space[1].split(",")[13]
Cv0=line_space[1].split(",")[14]
kr=line_space[1].split(",")[15]
kfall=line_space[1].split(",")[15]
p1=line_space[1].split(",")[17]
p2=line_space[1].split(",")[18]
p3=line_space[1].split(",")[19]
p4=line_space[1].split(",")[20]
f_space.close()

import pandas as pd
from pandas import Series
To=pd.read_csv("./month.csv",parse_dates=True,infer_datetime_format=True,index_col='datetime')
et=To['eet'].values
#Sm=To['SM'].values
temp=To['Temp'].values
par=To['par'].values
co2=To['CO2'].values
kleaf_final=Kleaf(float(A),float(B),float(C),float(MIN),et)
#for i in range(len(et)):
#    a=float(527.683052)*Par(float(0.002634061),par[i])*CO2(float(0.00264978),co2[i])*sm(float(0.438874992),float(0.081306655),float(0.200375378),Sm[i])*kleaf_final[i]*Temp(float(43.6920578),float(0.962789537),float(25.069114),temp[i])
#    print(a)
#    GPP.append(a)
#GPP
#print(GPP)
for i in range(len(par)):
    gpp_es=float(Cmax)*Par(float(p1),float(p2),float(p3),float(p4),par[i])*CO2(float(KC),co2[i])*FOLIAGE(float(m1),float(m2),float(m3),float(m4),float(Cv0))*kleaf_final[i]*Temp(float(Q),float(Tr),temp[i])
    Rm=rm(float(kr),float(Cv0),temp[i])
    Rg=rg(gpp_es,Rm)
    Lc=lc(float(Cv0),float(kfall))
    Cv1=float(gpp_es)-(float(Rm)+float(Rg))-float(Lc)+float(Cv0)
    Cv0=Cv1
    print(gpp_es)
 #   print(Cv1)

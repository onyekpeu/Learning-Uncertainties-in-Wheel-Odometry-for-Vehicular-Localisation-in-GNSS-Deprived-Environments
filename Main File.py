# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 22:03:11 2019

@author: onyekpeu
"""
import tensorflow.keras
import tensorflow as tf
import numpy as np
import time
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

from function_filesdispV4wsforqgrupaper import *
from IO_VNB_Dataset import *

#scipy.integrate.cumtrap
'Parameters'
#############################################################################
#############################################################################
#############################################################################
par=np.arange(1,2,1)#14
#par=[1, 10, 100, 1000, 10000]
#par=[160, 256, 320, 512, 720, 1024]
#par=[4, 8, 16, 32, 48, 64, 72, 96, 128, 160, 256, 320, 512, 720, 1024]
#par=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100]#,200,300,400,500,600,700,800,900]#,1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
#par=[4, 8, 16, 32, 48, 64, 72, 96, 128, 160, 192, 256, 512, 600, 720, 1024] #np.arange(0.01,0.11, 0.01)#14
#par=np.arange(416,1152,32)
opt_runsN=np.zeros((8,len(par),4))
#opt_runsE=np.zeros((len(par),4))
#opt_runs2=np.zeros((len(par),4))
for opt_ in range(len(par)):
    opt=par[opt_]
    dropout=0.25#*int(opt)

    input_dim = 2
    output_dim = 1
    num_epochs = 60
    layer_dim = 1
    learning_rate = 0.004
    batch_size =1024#int(opt)
    test_split =0# 0.0000001
    decay_rate=0.1#*int(opt)
    decay_steps=10000
    momentum=0.8
    samplefreq=10
    Ts=int(samplefreq*1*1)#*int(opt)
    seq_dim=int(10*(10/Ts))#
    seq_dim_=int(seq_dim*Ts)
    avg=1
    l1_=0#.01#*int(opt)#0.1#0.8
    l2_=0#.1#*int(opt)#0#.99#0.7
    h2 = 4#int(opt)
    Z=1
    outage=100

    number_of_runs=1
    mode='LSTM'

    
    #############################################################################
    #############################################################################
    #############################################################################
    'Dataloading and indexing'
    #############################################################################
    #############################################################################
    #############################################################################
    TrainDat=[V_Vta2, V_Vta1a, V_Vw5, V_Vta8, V_Vta10, V_Vta16, V_Vta17, V_Vta20, V_Vta21, V_Vta22, V_Vta27, V_Vta28, V_Vta29[:800], V_Vta29[1080:6780], V_Vta29[7220:], V_Vta30[:12900], V_Vta30[13180:], V_Vtb1, V_Vtb2, V_Vtb3, V_Vtb5[:1255], V_Vtb5[1267:3720], V_Vtb5[4160:4380], V_Vtb5[4860:6760], V_Vtb5[7220:],  V_Vw4[:4900], V_Vw4[5760:6220], V_Vw4[7420:33340], V_Vw4[33460:80660], V_Vw4[81000:116180], V_Vw4[117160:], V_Vw14b, V_Vw14c[:14060], V_Vw14c[15600:], V_Vfa01, V_Vfa02[:59860], V_Vfa02[59860:], V_Vfb01a[:1520], V_Vfb01a[1980:5360], V_Vfb01a[5740:9360], V_Vfb01a[11660:], V_Vfb01b, V_Vfb02b]

    Acc1_bias, Acc2_bias, gyro1_bias, Brkpr_bias=calib1(Bias)

    RAdat=[V_Vta11, V_Vfb02d] 
    CIAdat=[V_Vfb02e,V_Vta12]   
    HBdat=[V_Vw16b,V_Vw17,V_Vta9, V_Vta13]
    SLRdat=[V_Vw6, V_Vw8, V_Vw7]
    HRdat=[V_Vw12]
    WRdat=[V_Vtb8, V_Vtb11, V_Vtb13]
#    ra1, ra2, dxmx, dxmn, dymx, dymn= maxmin_wheelspd(locPred42,Ts, gyro1_bias)

    amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn= maxmin17(V_Vw12,Ts, Acc1_bias, gyro1_bias)
    gtr,itr,x, y=data_process13tr(TrainDat, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode)


    gthr,ithr,xthr, ythr=data_process13t( HRdat, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode)
    gtra,itra,xtra, ytra=data_process13t(RAdat, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode)
    gtcia,itcia,xtcia, ytcia=data_process13t(CIAdat, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode)
    gthb,ithb,xthb, ythb=data_process13t(HBdat, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn,Z, mode)
    gtslr,itslr,xtslr, ytslr=data_process13t(SLRdat, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode)
    gtwr,itwr,xtwr, ytwr=data_process13t(WRdat, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode)

    cm_runshr=np.zeros((int(number_of_runs),4))
    cm_runsra=np.zeros((int(number_of_runs),4))
    cm_runscia=np.zeros((int(number_of_runs),4))
    cm_runshb=np.zeros((int(number_of_runs),4))

    cm_runsslr=np.zeros((int(number_of_runs),4)) 
    cm_runswr=np.zeros((int(number_of_runs),4))


    'array creation to store  maximum INS physical model error for each scenario after each full training. '
    cm_runshrdr=np.zeros((int(number_of_runs),4))
    cm_runsradr=np.zeros((int(number_of_runs),4))
    cm_runsciadr=np.zeros((int(number_of_runs),4))
    cm_runshbdr=np.zeros((int(number_of_runs),4))

    cm_runsslrdr=np.zeros((int(number_of_runs),4)) 
    cm_runswrdr=np.zeros((int(number_of_runs),4))

    
    
    newPpredhr=[]
    newPpredcia=[]
    newPpredhb=[] 
    newPpredra=[]     

    newPpredslr=[]  
    newPpredwr=[]

    for nfr in range(number_of_runs):
        print('full training run: '+ str(nfr))
        print('optimisation run: '+ str(opt))
        #############################################################################
        #############################################################################
        #############################################################################
        'GRU TRAINING'
        #############################################################################
        #############################################################################
        #############################################################################

        Run_time, regress=GRU_model(np.array(x),np.array(y), input_dim,output_dim, seq_dim, batch_size, num_epochs, dropout, h2, learning_rate, l1_, l2_, nfr, decay_rate, momentum, decay_steps)
        
  
        dist_travldhr, perf_metrhr_crsep, perf_metrhr_crsedr, perf_metrhr_caep, perf_metrhr_caedr, perf_metrhr_aepsp, perf_metrhr_aepsdr,perf_metrhr_aeirp, perf_metrhr_aeirdr,newPpredshr, inshr, gpshr=predictcs(xthr,ythr, ithr, regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Motorway Scenario',outage)
        dist_travldra, perf_metrra_crsep, perf_metrra_crsedr, perf_metrra_caep, perf_metrra_caedr,perf_metrra_aepsp, perf_metrra_aepsdr,perf_metrra_aeirp, perf_metrra_aeirdr,newPpredsra,  insra, gpsra=predictcs(xtra,ytra, itra, regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Roundabout Scenario',outage)
        dist_travldcia, perf_metrcia_crsep, perf_metrcia_crsedr,perf_metrcia_caep, perf_metrcia_caedr,perf_metrcia_aepsp, perf_metrcia_aepsdr,perf_metrcia_aeirp, perf_metrcia_aeirdr,newPpredscia,  inscia, gpscia=predictcs(xtcia,ytcia, itcia, regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Quick Changes in \n Acceleration Scenario',outage)
        dist_travldhb, perf_metrhb_crsep, perf_metrhb_crsedr,perf_metrhb_caep, perf_metrhb_caedr,perf_metrhb_aepsp, perf_metrhb_aepsdr,perf_metrhb_aeirp, perf_metrhb_aeirdr,newPpredshb,  inshb, gpshb=predictcs(xthb,ythb, ithb, regress, seq_dim, input_dim, mode,Ts, dgmx, dgmn, Z, 'Hard Brake Scenario',outage)
        dist_travldslr, perf_metrslr_crsep, perf_metrslr_crsedr,perf_metrslr_caep, perf_metrslr_caedr,perf_metrslr_aepsp, perf_metrslr_aepsdr,perf_metrslr_aeirp, perf_metrslr_aeirdr,newPpredsslr, insslr, gpsslr=predictcs(xtslr,ytslr, itslr, regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Sharp Cornering and \n Successive Left and Right Turns Scenario',outage)
        dist_travldwr, perf_metrwr_crsep, perf_metrwr_crsedr,perf_metrwr_caep, perf_metrwrp,perf_metrwr_aepsp, perf_metrwr_aepsdr,perf_metrwr_aeirp, perf_metrwr_aeirdr, newPpredswr,  inswr, gpswr=predictcs(xtwr,ytwr, itwr, regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Wet Road Scenario',outage)

        newPpredhr.append(newPpredshr)
        newPpredra.append(newPpredsra)   
        newPpredcia.append(newPpredscia)
        newPpredhb.append(newPpredshb)      
        newPpredslr.append(newPpredsslr)  
        newPpredwr.append(newPpredswr)
 

        'indexes the maximum prediction crse across each 10 seconds array'
        cm_runshr[nfr]=perf_metrhr_crsep[:]
        cm_runsra[nfr]=perf_metrra_crsep[:]    
        cm_runscia[nfr]=perf_metrcia_crsep[:]
        cm_runshb[nfr]=perf_metrhb_crsep[:]

        cm_runsslr[nfr]=perf_metrslr_crsep[:]       
        cm_runswr[nfr]=perf_metrwr_crsep[:]
     
        
        'indexes the maximum prediction crse across each 10 seconds array'
        cm_runshrdr[nfr]=perf_metrhr_crsedr[:]
        cm_runsradr[nfr]=perf_metrra_crsedr[:]     
        cm_runsciadr[nfr]=perf_metrcia_crsedr[:]
        cm_runshbdr[nfr]=perf_metrhb_crsedr[:]

        cm_runsslrdr[nfr]=perf_metrslr_crsedr[:]       
        cm_runswrdr[nfr]=perf_metrwr_crsedr[:]


    'indexes the best results across the optimisation runs'       
    a10hr=np.amin(cm_runshr,axis=0)
    a10ra=np.amin(cm_runsra,axis=0)
    a10cia=np.amin(cm_runscia,axis=0)
    
    a10hb=np.amin(cm_runshb,axis=0)
    a10slr=np.amin(cm_runsslr,axis=0)
    a10swr=np.amin(cm_runswr,axis=0)



    a10hrp=np.amin(cm_runshrdr,axis=0)
    a10rap=np.amin(cm_runsradr,axis=0)
    a10ciap=np.amin(cm_runsciadr,axis=0)
    
    a10hbp=np.amin(cm_runshbdr,axis=0)
    a10slrp=np.amin(cm_runsslrdr,axis=0)
    a10swrp=np.amin(cm_runswrdr,axis=0)

    
    opt_runsN[0,opt_,:4]=a10hr
    opt_runsN[1,opt_,:4]=a10ra
    opt_runsN[2,opt_,:4]=a10cia
    opt_runsN[3,opt_,:4]=a10hb
    opt_runsN[4,opt_,:4]=a10slr     
    opt_runsN[5,opt_,:4]=a10swr

    
   


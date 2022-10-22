import math
import cv2
import numpy as np
import functions as fun
from EadgeAwareFilter import filtring
import numba as nb




class eltm_tmo:
    """Implementation of Ehanced Local Tone Mapping (ELTM). For more details visit this
    paper link https://www.sciencedirect.com/science/article/abs/pii/S1047320318300555.
    """
    
    
    def __init__(self,data,scale,width,height):
        self.data, self.scale = data, scale
        self.width, self.height = width, height
    
    
    
    def tmo(self):
        
        EPSILON, LAMDA_F, R_S, M =0.000001, 0.02, 3, -2.7
        BPC_MAX, GEMA, TAU_R, ETA_C =0.9, 2.2, 5, 1.5
    
        EPSILON_S = EPSILON_L = BPC_MIN = 0.1
        LAMDA_C = ETA_F = P = K = S = 1
        
        R_L= int(self.width/10 if self.width<self.height else self.height/10)  #the large guided filter's radius (rL) was calculated as 10% of the min (height, width)
        
        """***********************************************************************
	                        LOG DOMAIN PROCESSING                         
	    ***********************************************************************"""
        
        #------------Exact luminance channel--------------
        size=self.width*self.height
        
        ycbcr=cv2.cvtColor(self.data,cv2.COLOR_RGB2YCrCb)
        y=ycbcr[:,:,0]
        
        Ylog=np.zeros((self.height,self.width))
        #Ylog=math.log2(y+EPSILON)
        for i in range(self.height):
           for j in range(self.width):
               Ylog[i, j]=math.log2(y[i, j]+EPSILON)
               #print('{} \n'.format(Ylog[i][j]))
        
        #----------------3.2. Decomposition----------------
        #Ylog=Ylog.reshape((self.height,self.width,1))
     
        #test= math.log(Ylog[i][j])
        
        flterS=filtring(Ylog,self.height,self.width,R_S,EPSILON_S)
        edgfilterS=flterS.EAF()
        DPFlog=fun.clip((Ylog-edgfilterS),self.height,self.width, LAMDA_F)
        BPFlog=Ylog-DPFlog
        
        
        flterL=filtring(BPFlog,self.height,self.width ,R_L,EPSILON_L)
        edgfilterL=flterL.EAF()
        DPClog=fun.clip((BPFlog-edgfilterL),self.height,self.width, LAMDA_C)
        BPlog=BPFlog-DPClog
        
        #-----------3.3. Logarithm domain contrast reduction------------
        
        maxBPlog=np.max(BPlog)
        minBPlog=np.min(BPlog)
        beta=-maxBPlog
        alpha=TAU_R/(maxBPlog-minBPlog)
        BPlog=(BPlog+beta)*alpha #BP'log (5)
        
        #------------------3.4. Detail enhancement--------------------
        minBPlog=(minBPlog+beta)*alpha
        maxBPlog=(maxBPlog+beta)*alpha
        
        
        """***********************************************************************
	                       LINEAR DOMAIN PROCESSING                       *
	    ***********************************************************************"""

        #Calculate BPmin and BPmax for function (9). Because y = 2^x is an increasing function, so
        
        BPmin=pow(2,minBPlog)
        BPmax=pow(2,maxBPlog)
        
        
        #--------------5. ELTM brightness control-------------------
        P_=P*pow(10,K*(np.average(BPlog)-M))
        
        out =np.zeros((self.height,self.width,3))
        #out =np.zeros(self.height*self.width*3)
        for i in range(self.height):
            for j in range(self.width):
                #Function (6)
                SG=max((-0.4*BPlog[i, j]),1)
                DPFlog_=ETA_F*SG*DPFlog[i, j]
                DPClog_=ETA_C*SG*DPClog[i, j]
            
            
                #Function (7)
                BP=pow(2,BPlog[i, j])
                DP=pow(2,(DPFlog_+DPClog_))
                
                #--------------3.5. Tone compression---------------------
                BPC=(BPC_MAX-BPC_MIN)*((math.log((BP-BPmin)/(BPmax-BPmin)+P_)-math.log(P_))/(math.log(1+P_)-math.log(P_)))+BPC_MIN
                YC=BPC*DP
                
                RIn=self.data[:,:,0]
                GIn=self.data[:,:,1]
                BIn=self.data[:,:,2]
                
                R=round(YC*pow(RIn[i, j]/y[i, j],S/GEMA)*255)
                G=round(YC*pow(GIn[i, j]/y[i, j],S/GEMA)*255)
                B=round(YC*pow(BIn[i, j]/y[i, j],S/GEMA)*255)
                
                ROut= 255 if R>255 else R
                GOut= 255 if G>255 else G
                BOut= 255 if B>255 else B
                ROut= 0 if R<0 else R
                GOut= 0 if G<0 else G
                BOut= 0 if B<0 else B

            
                out[i,j,0]=ROut
                out[i,j,1]=GOut
                out[i,j,2]=BOut
            
        return out
            

            
     
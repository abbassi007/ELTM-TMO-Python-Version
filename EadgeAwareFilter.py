import functions as fun

class filtring:
    """Filtring is for all type of filters however currently,
    we are using eadge aware filter for Enhanced Local Tone 
    Mapping (ELTM TMO).
    """
    
    def __init__(self,data, height, width, radius, epsilon):
        self.data=data
        self.width=width
        self.height=height
        self.radius=radius
        self.epsilon=epsilon
    
    
    def EAF(self):
        meanI=fun.mean_filter(self.data, self.height, self.width, self.radius)
        corrI=fun.mean_filter(self.data*self.data, self.height, self.width, self.radius)
        
        varI=corrI-(meanI*meanI)
        a=varI/(varI+self.epsilon)
        
        meanA=fun.mean_filter(a, self.height, self.width, self.radius)
        meanB=fun.mean_filter((meanI-(a*meanI)), self.height, self.width, self.radius)
        
        q=(meanA*self.data)+meanB
        
        return q
        

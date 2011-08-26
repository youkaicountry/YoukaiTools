import math

#The base interpolation functions. The interpolation happens
#between y1 and y2. y0 and y3 are extra values
#Tension: 1 is high, 0 normal, -1 is low
#Bias: 0 is even,bpositive is towards first segment,
#negative towards the other

def linear(mu, y1, y2):
    return (y1*(1-mu)+y2*mu)
    
def cosine(mu, y1, y2):
    mu2 = (1-math.cos(mu*math.pi))/2;
    return(y1*(1-mu2)+y2*mu2);

def quadratic(mu, y1, y2):
    if mu <= .5:
        mu *= mu;
    else:
        mu = 1.0 - mu;
        mu *= mu;
        mu = 0.5 - mu;
        mu += mu;
    return y1*(1.0-mu) + y2*mu;

def cubic(mu, y0, y1, y2, y3, tension, bias):
    mu2 = mu*mu;
    a0 = y3 - y2 - y0 + y1;
    a1 = y0 - y1 - a0;
    a2 = y2 - y0;
    a3 = y1;
    return(a0*mu*mu2+a1*mu2+a2*mu+a3);

def catmullRom(mu, y0, y1, y2, y3, tension, bias):
    mu2 = mu*mu;
    a0 = -0.5*y0 + 1.5*y1 - 1.5*y2 + 0.5*y3;
    a1 = y0 - 2.5*y1 + 2*y2 - 0.5*y3;
    a2 = -0.5*y0 + 0.5*y2;
    a3 = y1;
    return(a0*mu*mu2+a1*mu2+a2*mu+a3);

def hermite(mu, y0, y1, y2, y3, tension, bias):
    mu2 = mu * mu;
    mu3 = mu2 * mu;
    m0  = (y1-y0)*(1+bias)*(1-tension)/2;
    m0 += (y2-y1)*(1-bias)*(1-tension)/2;
    m1  = (y2-y1)*(1+bias)*(1-tension)/2;
    m1 += (y3-y2)*(1-bias)*(1-tension)/2;
    
    a0 =  2*mu3 - 3*mu2 + 1;
    a1 =    mu3 - 2*mu2 + mu;
    a2 =    mu3 -   mu2;
    a3 = -2*mu3 + 3*mu2;
    
    return(a0*y1+a1*m0+a2*m1+a3*y2);

#linear
#cubic
#cubic spline

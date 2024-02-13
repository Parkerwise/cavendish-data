#libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
plt.rcParams['text.usetex'] = True
plt.rcParams.update({'font.size': 12})
#plots data
columns=["time","pos"]
df=pd.read_csv("data.csv",usecols=columns)
f=plt.figure()
f.set_figwidth(6)
f.set_figheight(3.5)
plt.ylabel("Position (cm)")
plt.xlabel("Time (s)")
plt.axhline(0,0,2500,color="black",linestyle="dashed",lw=1)
plt.xlim(0,2500)


#fits data
def Damped(x,A,T,W,phi):
    return A*np.exp(-x/T)*np.cos(W*x+phi)
guess=[35,1000,0.01,10]
parameters, covariance= curve_fit(Damped, df.time, (df.pos-216.5),p0=guess)

#plots fit
A=parameters[0]
T=parameters[1]
W=parameters[2]
phi=parameters[3]
time=[t for t in range(2500)]
fit_pos=[A*np.exp(-t/T)*np.cos(W*t+phi) for t in range(2500)]
decay=[A*np.exp(-t/T) for t in range(2500)]
plt.plot(time, decay,label=r"$Ae^{-\frac{t}{\tau}}$",color="green",lw=1)
plt.plot(time, fit_pos, color="red",label=r"$Ae^{-\frac{t}{\tau}}\cos\left(\omega t +\phi \right)$",lw=1)

plt.errorbar(df.time,df.pos-216.5, xerr=0.1, yerr=1, fmt=".",label="Data",markersize="3",lw=1,color="blue")

plt.text(1900,20,f'$A$ = {round(A,5)}')
plt.text(1900,30,f'$\omega$ = {round(W,5)}')
plt.text(1900,25,f'$\\tau$ = {round(T,5)}')
plt.text(1900,15,f'$\phi$ = {round(phi,5)}')
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig("osc.pdf")


D=4.8
r=0.6
L=522
half_box_width=1.4
def Gcalc(s,R,m):
    b=half_box_width+R
    return ((D**2+(2/5)*r**2)*(W**2-(1/(T**2)))*s*b**2)/(4*L*m*D)*10**(-3)

s_tungsten=30.9
radius_tungsten=3.49
m_tungsten=3050
s_steel=208.2-195.9
radius_steel=3.17
m_steel=1044
s_lead=210.6-192.8
radius_lead=3.17
m_lead=1507

print(Gcalc(s_tungsten,radius_tungsten,m_tungsten))
print(Gcalc(s_steel,radius_steel,m_steel))
print(Gcalc(s_lead,radius_lead,m_lead))


# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 12:24:24 2018


     C _____________  D
       |           |
       |           |
     B |___________|  A
________O_________O____________


"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from scipy.interpolate import interp1d
from matplotlib import animation

l=0.2
h=0.2
g=9.81
C=0.8
m=4. #masa vlaka
f=0.42 #faktor trenja

def f_y(x):
    #return 100-x
    return 3+x**2*(-7+1.2*x**2)/6
    #return (x*(x-10)*(x+2)*(x-10))/35
    
x=np.linspace(-3,3,1000)
y=f_y(x)

#plt.plot(x,y)

s=[0.0]
alfa=[]
for i in range (len(x)-1):
    s.append(s[-1]+np.sqrt((x[i]-x[i+1])**2+(y[i]-y[i+1])**2))
    alfa.append((1)*np.rad2deg(np.arctan((y[i]-y[i+1])/(x[i]-x[i+1]))))
print (s)

f_xs=interp1d(x,s)
f_sx=interp1d(s,x)
f_sy=interp1d(s,y)
f_alfa=interp1d(s[0:-1],alfa)

def dsdt(S,t):
    s,v=S
    a=-g*np.sin(np.deg2rad(f_alfa(s)))-C/m*v-f*g*np.cos(np.deg2rad(f_alfa(s)))*np.sign(v)
    return [v,a]

s0=f_xs(-2.8)
print (s0)
t=np.linspace(0.,5.5,100)
pocetni_uvijeti=[s0,0.0]

S=integrate.odeint(dsdt,pocetni_uvijeti,t)
put=S[:,0]
brzine=S[:,1]
width = 10
plt.figure(figsize=(width, width))
plt.plot(t, brzine, label = 'brzine' )
plt.plot(t, put, label = 'put' )
#plt.axis('scaled', adjustable='box')
#plt.xlim(-0.1, l_stola + 0.1)
#plt.ylim(-0.1, h_stola + 0.1)
plt.legend()

xevi=f_sx(put)
yloni=f_sy(put)
alfe=f_alfa(put)

def Plot(i):
    fig_num=i
    A=[xevi[i]+l/2*np.cos((np.deg2rad(alfe[i]))),yloni[i]+l/2*np.sin((np.deg2rad(alfe[i])))]
    B=[xevi[i]-l/2*np.cos((np.deg2rad(alfe[i]))),yloni[i]-l/2*np.sin((np.deg2rad(alfe[i])))]
    fig = plt.figure()
    plt.plot([A[0],B[0]],[A[1],B[1]],'ro')
    plt.plot(x,y)
    plt.axis('scaled', adjustable='box')
    plt.title('2D prikaz')
    fig_name= '%06d' % fig_num
    plt.savefig('./2D_plot/'+fig_name+'.png')
    plt.close()

#for i in range (len(t)):
#    Plot(i)
        

max_x=max(x)
min_x=min(x)
max_y=max(y)
min_y=min(y)

#plt.plot(xevi,yloni)
# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
plt.axis('scaled', adjustable='box')
ax = plt.axes(xlim=(min_x, max_x), ylim=(min_y, max_y))
point, = ax.plot([], [], 'ro')
line, = ax.plot([], [],)
vagon,= ax.plot([], [],)

# initialization function: plot the background of each frame
def init():
    point.set_data([], [])
    line.set_data([], [])
    vagon.set_data([],[])
    return point, line, vagon

# animation function.  This is called sequentially
def animate(i):
    A=[xevi[i]+l/2*np.cos((np.deg2rad(alfe[i]))),yloni[i]+l/2*np.sin((np.deg2rad(alfe[i])))]
    B=[xevi[i]-l/2*np.cos((np.deg2rad(alfe[i]))),yloni[i]-l/2*np.sin((np.deg2rad(alfe[i])))]
    #C=[B[0]+h*np.sin((np.deg2rad(alfe[i]))),B[1]+h*np.cos((np.deg2rad(alfe[i])))]
    #D=[A[0]+h*np.sin((np.deg2rad(alfe[i]))),A[1]+h*np.cos((np.deg2rad(alfe[i])))]
    
    point.set_data([A[0],B[0]], [A[1],B[1]])
    line.set_data(x,y)
    #vagon.set_data([A[0],B[0],C[0],D[0]],[A[1],B[1],C[1],D[1]])
    return point, line#, vagon

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=100, interval=100, blit=True)


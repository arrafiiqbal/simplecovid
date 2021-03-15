import numpy as np
import random
from itertools import combinations
from sklearn.neighbors import KDTree


#sunflower method
def init_pos(space,N):
    num_pts = N
    indices = np.arange(0,num_pts,dtype=float)+0.5
    
    r=np.sqrt(indices/num_pts)
    theta = np.pi * (1 + 5**0.5) * indices
    x=(space/2)*r*np.cos(theta)+space/2+30#kalo bentuk rectangle + constant harus liat dulu
    y=(space/2)*r*np.sin(theta)+space/2
    
    return np.column_stack((x, y))

#random init velo average m/s=0.07m/s ---> 6km/day
def init_velo(N):
    desired_avg=0.07
    vel_generator=np.random.rand(N)*desired_avg
    
    vel_x=np.zeros(N)
    vel_y=np.zeros(N)
    
    for i in range(N):
        vel_x[i]=random.choice([-1,1])*vel_generator[i]
        vel_y[i]=random.choice([-1,1])*np.sqrt(desired_avg**2-vel_generator[i]**2)
    
    return np.column_stack((vel_x,vel_y))


def change(vel,i):
    if i>0 and i%3600==0:
        #print("works")
        desired_avg=0.07
        vel_generator=np.random.rand(100)*desired_avg
        for i in range(len(vel)):
            vel[i][0]= random.choice([-1,1])*vel_generator[i]#vel[i][0]+(2*np.random.rand(1)-1)
            vel[i][1]= random.choice([-1,1])*np.sqrt(desired_avg**2-vel_generator[i]**2)#vel[i][1]+(2*np.random.rand(1)-1)
    
    else:
        pass
        
    return vel
    
    
#velocity affected by boundary space
def barrier(pos,vel,space,dt):
    limx=[0,space[0]]
    limy=[0,space[1]]
    
    for i in range(len(pos)):
        if pos[i][0]+vel[i][0]*dt<=limx[0]+1e-02 or pos[i][0]+vel[i][0]*dt>=limx[1]-1e-02 :
            vel[i][0]=-vel[i][0]
        elif pos[i][1]+vel[i][1]*dt<=limy[0]+1e-02  or pos[i][1]+vel[i][1]*dt>=limy[1]-1e-02 :
            vel[i][1]=-vel[i][1]
    
    return vel

#velocity affected by wall
def wall(pos,vel,space,dt):
    walpos=[[80,60],[80,40],[100,60],[100,40]]
    
    for i in range(len(pos)):
        #wallpoint 1
        if (pos[i][0]+vel[i][0]*dt>=walpos[0][0]-0.25 and pos[i][0]+vel[i][0]*dt<walpos[2][0]) and pos[i][1]+vel[i][1]*dt>=walpos[0][1]:
            vel[i][0]=-vel[i][0]
            vel[i][1]=-abs(vel[i][1])#+np.random.rand(1)[0]
        elif (pos[i][0]+vel[i][0]*dt>=walpos[0][0] and pos[i][0]+vel[i][0]*dt<=walpos[2][0]) and pos[i][1]+vel[i][1]*dt>=walpos[0][1]-0.25:
            vel[i][1]=-vel[i][1]
    
        #corner 1
        elif (pos[i][0]+vel[i][0]*dt>=walpos[0][0]-0.25 and pos[i][0]+vel[i][0]*dt<walpos[0][0]) and (pos[i][1]+vel[i][1]*dt>=walpos[0][1]-0.25 and pos[i][1]+vel[i][1]*dt<walpos[0][1]):
            vel[i][0]=-vel[i][0]
            vel[i][1]=-abs(vel[i][1])#+np.random.rand(1)[0]
        
        
        #wallpoint2
        elif (pos[i][0]+vel[i][0]*dt>=walpos[1][0]-0.25 and pos[i][0]+vel[i][0]*dt<walpos[3][0]) and pos[i][1]+vel[i][1]*dt<=walpos[1][1]:
            vel[i][0]=-vel[i][0]
            vel[i][1]=abs(vel[i][1])#+np.random.rand(1)[0]
        elif (pos[i][0]+vel[i][0]*dt>=walpos[1][0] and pos[i][0]<=walpos[3][0]) and pos[i][1]+vel[i][1]*dt<=walpos[1][1]+0.25:
            vel[i][1]=-vel[i][1]
            
        
        #corner 2
        elif (pos[i][0]+vel[i][0]*dt>=walpos[1][0]-0.25 and pos[i][0]+vel[i][0]*dt<walpos[1][0]) and (pos[i][1]+vel[i][1]*dt<=walpos[1][1]+0.25 and pos[i][1]+vel[i][1]*dt>walpos[1][1]):
            vel[i][0]=-vel[i][0]
            vel[i][1]=abs(vel[i][1])#+np.random.rand(1)[0]
        
        #wallpoint 3
        elif (pos[i][0]+vel[i][0]*dt<=walpos[2][0]+0.25 and pos[i][0]+vel[i][0]*dt>walpos[0][0])and pos[i][1]+vel[i][1]*dt>=walpos[2][1]:
            vel[i][0]=-vel[i][0]
        
        #wallpoint 4
        elif (pos[i][0]+vel[i][0]*dt<=walpos[3][0]+0.25 and pos[i][0]+vel[i][0]*dt>walpos[1][0])and pos[i][1]+vel[i][1]*dt<=walpos[3][1]:
            vel[i][0]=-vel[i][0]
       
    return vel

#velocity affected by collision
def collission(pos,vel,dt):
    #global socializing_time
    
    combi=list(combinations(range(len(pos)),2))
    cr=0.8
    #stime=np.copy(socializing_time)
    for i,j in combi:
        dis_x=(pos[i][0]+vel[i][0]*dt)-(pos[j][0]+vel[j][0]*dt)
        dis_y=(pos[i][1]+vel[i][1]*dt)-(pos[j][1]+vel[j][1]*dt)
        r=np.sqrt(dis_x**2+dis_y**2)
        if r<=0.5:
            '''
            indices=np.where((stime[:,0]==i)&(stime[:,1]==j))[0][0]
            stime[indices,2]=stime[indices,2]+0.01
            if stime[indices,2]<=0.05:
                cons=init_velo(1)[0]
                vel[i]=cons
                vel[j]=cons
            
            else:
            '''
            va_init=np.copy(vel[i])
            vb_init=np.copy(vel[j])
            #x_axis
            vbx_after=(cr*(va_init[0]-vb_init[0])+va_init[0]+vb_init[0])/2
            vax_after=va_init[0]+vb_init[0]-vbx_after
            
            #y_axis
            vby_after=(cr*(va_init[1]-vb_init[1])+va_init[1]+vb_init[1])/2
            vay_after=va_init[1]+vb_init[1]-vby_after
            
            vel[i]=[vax_after,vay_after]
            vel[j]=[vbx_after,vby_after]
                
            
        else:
            pass        
    
    return vel


def collission2(pos,velo,dt):
    vel=velo
    cr=0.08
    points=pos+vel*dt
    tree = KDTree(points)
    nn_indices=tree.query_radius(points, r=0.5)
    
    for i in range(len(nn_indices)):
        for j in range(len(nn_indices[i])):
            if nn_indices[i][j]==i:
                pass
            else:
                a=i
                b=nn_indices[i][j]
                
                va_init=np.copy(vel[a])
                vb_init=np.copy(vel[b])
                #x_axis
                vbx_after=(cr*(va_init[0]-vb_init[0])+va_init[0]+vb_init[0])/2
                vax_after=va_init[0]+vb_init[0]-vbx_after
                
                #y_axis
                vby_after=(cr*(va_init[1]-vb_init[1])+va_init[1]+vb_init[1])/2
                vay_after=va_init[1]+vb_init[1]-vby_after
                
                vel[a]=[vax_after,vay_after]
                vel[b]=[vbx_after,vby_after]
        
    return vel


#velocity affected by attraction force/source
def attract(pos,vel,dt):
    source=[140,50]
    #c=0.5
    #d=0.1
    gm=1#307.2 #source 25 -> gmm = 120 keep constant effect F on point (x,y)
    m=1
    for i in range(len(pos)):
        dis_x=pos[i][0]-source[0]
        dis_y=pos[i][1]-source[1]
        r=np.sqrt((dis_x**2)+(dis_y**2))
        
        if pos[i][0]<=100:
            if r<=1: #ini awalnya buat mantulin kalo terlalu deket sama source tapi gajadi
                fx=gm*(source[0]-pos[i][0])/r**3
                fy=gm*(source[1]-pos[i][1])/r**3
                vel[i][0]=-np.sqrt(2*gm/r)*(source[0]-pos[i][0])/r#-(fx/m)
                vel[i][1]=-np.sqrt(2*gm/r)*(source[1]-pos[i][1])/r#-(fy/m)
                #vel[i][0]=(source[0]-pos[i][0])/r
            elif r>1 and r<=150:
                fx=gm*(source[0]-pos[i][0])/r**3
                fy=gm*(source[1]-pos[i][1])/r**3
                vel[i][0]=vel[i][0]+(fx/m)*dt
                vel[i][1]=vel[i][1]+(fy/m)*dt
            else :
                pass
        else:
            pass
        
    return vel

def attract2(pos,vel,dt):
    source=[40,50]
    #c=0.5
    #d=0.1
    gm=1#307.2 #source 25 -> gmm = 120 keep constant effect F on point (x,y)
    m=1
    for i in range(len(pos)):
        dis_x=pos[i][0]-source[0]
        dis_y=pos[i][1]-source[1]
        r=np.sqrt((dis_x**2)+(dis_y**2))
        
        if pos[i][0]>=80:
            if r<=1: #ini awalnya buat mantulin kalo terlalu deket sama source tapi gajadi
                fx=gm*(source[0]-pos[i][0])/r**3
                fy=gm*(source[1]-pos[i][1])/r**3
                vel[i][0]=-np.sqrt(2*gm/r)*(source[0]-pos[i][0])/r#-(fx/m)
                vel[i][1]=-np.sqrt(2*gm/r)*(source[1]-pos[i][1])/r#-(fy/m)
                #vel[i][0]=(source[0]-pos[i][0])/r
            elif r>1 and r<=150:
                fx=gm*(source[0]-pos[i][0])/r**3
                fy=gm*(source[1]-pos[i][1])/r**3
                vel[i][0]=vel[i][0]+(fx/m)*dt
                vel[i][1]=vel[i][1]+(fy/m)*dt
            else :
                pass
        else:
            pass
        
    return vel

#update movement for next time step #free
def update_movementa(pos,vel,dt,space,i):
    
    vel=barrier(pos,vel,space,dt)
    vel=collission(pos,vel,dt)
    vel=change(vel,i)
    
    pos=pos+vel*dt
    return pos

 #with wall
def update_movementb(pos,vel,dt,space,i,flow):
    f=flow
    if f==1:
        vel=attract(pos,vel,dt) #move to right
        vel=barrier(pos,vel,space,dt)
        vel=wall(pos,vel,space,dt)
        vel=collission(pos,vel,dt)
        vel=change(vel,i)
        
        pos=pos+vel*dt
        
        if np.sum(pos[:,0]>80)>=90:
            f=0
        else:
            pass
        
    elif f==0:
        vel=attract2(pos,vel,dt) #move toleft
        vel=barrier(pos,vel,space,dt)
        vel=wall(pos,vel,space,dt)
        vel=collission(pos,vel,dt)
        vel=change(vel,i)
        
        pos=pos+vel*dt
        
        if np.sum(pos[:,0]<100)>=90:
            f=1
        else:
            pass
        
        '''
        if np.min(pos[:,0])>165:
            vel=attract2(pos,vel,dt) #move to left
            vel=barrier(pos,vel,space,dt)
            vel=wall(pos,vel,space,dt)
            vel=collission(pos,vel,dt)
            vel=change(vel,i)
            
            pos=pos+vel*dt
        
        else:
            vel=attract2(pos,vel,dt) #move toleft
            vel=barrier(pos,vel,space,dt)
            vel=wall(pos,vel,space,dt)
            vel=collission(pos,vel,dt)
            vel=change(vel,i)
            
            pos=pos+vel*dt
        '''

    return pos,f
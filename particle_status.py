import numpy as np
import random
import scipy.spatial as spatial


#initialization of particles' status at t=0
def init_status(N):
    status=np.zeros(N,dtype=str)
    infected_indices=[round(np.random.rand(1)[0]*100)] #only 1 I0
    for i in range(N):
        if i in infected_indices:
            status[i]="I"
        else:
            status[i]="S"
    
    return status,infected_indices

#check whether recovered or not
def check_time(status,infected_time,dt):
    infected=np.where(status=="I")[0]
    time=np.copy(infected_time)
    
    for i in infected:
        time[i]=time[i]+dt
    
    return time

#update status of the particle at time frame ndt
def update_status(status,pos,tinfected,tinfects,det,inf_id,total_inf):
    pid=inf_id
    c=total_inf
    statuta=np.copy(status)
    tinfecting=np.copy(tinfects)
    determine=np.copy(det)
    #infp=50
    infected=np.where(statuta=="I")[0]
    other=np.delete(np.arange(len(statuta)),infected)
    
    for i in infected:
        if tinfected[i]>=604800:#7 days in seconds
            statuta[i]="R"
            
    infected=np.where(statuta=="I")[0]
    inf_mat=[]
    for i in infected:
        arr=[]
        for j in other:
            dis_x=pos[i][0]-pos[j][0]
            dis_y=pos[i][1]-pos[j][1]
            r=np.sqrt((dis_x**2)+(dis_y**2))
            arr.append(r)
            if r<=1:
                if statuta[j]=="R":
                    pass
                else:
                    tinfecting[j]=tinfecting[j]+1 #dt
                    if tinfecting[j]>=30:#60 : #for time thresh in s
                        coin=np.random.rand(1)[0]*100
                        
                        #OUTDOOR/indoor
                        if pos[j][0]<10:
                            infp=100 #infp=10 outdoor 10
                            if coin >=100-infp and determine[i][j]=="N": #ini dia buat case inf prob
                                statuta[j]="I"
                                determine[i][j]="Y"
                                if i==pid:
                                    c=c+1
                                    #print("gotcha!!!")
                                    
                            elif coin<100-infp and determine[i][j]=="N":
                                statuta[j]="S"
                                determine[i][j]="Y"
                            else:
                                pass
                        
                        #INDOOR
                        else:
                            infp=100
                            if coin >=100-infp and determine[i][j]=="N": #ini dia buat case inf prob
                                statuta[j]="I"
                                determine[i][j]="Y"
                                if i==pid:
                                    c=c+1
                                    #print("gotcha!!!")
                            elif coin<100-infp and determine[i][j]=="N":
                                statuta[j]="S"
                                determine[i][j]="Y"
                            else:
                                pass
            else:
                determine[i][j]="N"
                #tinfecting[j]=0 #awalnya ga pake
                
        arr=np.array(arr)
        inf_mat.append(np.median(arr))
    
    inf_mat=np.array(inf_mat)
    medval=np.median(inf_mat)
    
    return statuta,tinfecting,determine,c,medval

def update_status2(status,pos,tinfected,tinfects,det,inf_id,total_inf):
    pid=inf_id
    c=total_inf
    statuta=np.copy(status)
    tinfecting=np.copy(tinfects)
    determine=np.copy(det)
    #infp=50
    infected=np.where(statuta=="I")[0]
    avg_den=0
    
    for i in infected:
        if tinfected[i]>=604800:#7 days in seconds
            statuta[i]="R"
            
    infected=np.where(statuta=="I")[0]
    suspected=np.where(statuta=="S")[0]
    #inf_mat=[]
    centendency=[]
    sus_pos=pos[suspected]
    
    if suspected.size==0 :
        pass
    else:
        tree=spatial.cKDTree(sus_pos)
        for i in range(len(infected)):
            center=pos[infected[i]]
            #raw_near=np.array(tree.query_ball_point(center,1)) #radius 1 meter
            raw_index=tree.query_ball_point(center,1)
            near_index=suspected[raw_index]
            avg_den=avg_den+(len(near_index)+1)
            centendency.append(len(near_index))
            
            for j in range(len(near_index)):
                tinfecting[near_index[j]]=tinfecting[near_index[j]]+1 #dt
                if statuta[near_index[j]]=="R":
                    pass
                
                else:
                    if tinfecting[near_index[j]]>=30: #time threshold
                        infp=100 #inf prob
                        coin=np.random.rand(1)[0]*100
                        if coin >=100-infp and determine[infected[i]][near_index[j]]=="N": #ini dia buat case inf prob
                            statuta[near_index[j]]="I"
                            determine[infected[i]][near_index[j]]="Y"
                            if infected[i]==pid:
                                c=c+1
                                #print("gotcha!!!")
                                
                        elif coin<100-infp and determine[i][j]=="N":
                            statuta[near_index[j]]="S"
                            determine[infected[i]][near_index[j]]="Y"
                        else:
                            pass
    
    avg_den=avg_den/len(infected)
    med=np.median(centendency)
    
    return statuta,tinfecting,determine,c,avg_den,med


#count S I R at time ndt respectively
def sir_count(statust):
    unique_elements, counts_elements = np.unique(statust, return_counts=True)
    data=np.asarray((unique_elements, counts_elements))
    
    sir=np.zeros(3)
    sus=0
    inf=0
    rec=0
    for i in range(len(data[0])):
        if data[0][i]=="S":
            sus=int(data[1][i])
        elif data[0][i]=="I":
            inf=int(data[1][i])
        elif data[0][i]=="R":
            rec=int(data[1][i])
    sir[0]=sus
    sir[1]=inf
    sir[2]=rec
    
    return sir
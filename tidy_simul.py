for file in range(10):
    import particle_motion
    import particle_status
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from datetime import datetime
    startTime = datetime.now()
    
    #settings=pd.read_excel(r'E:\Epidemic Math\init_cond3.xlsx').to_numpy()
    #density=6200/km2 
    N=100 #worth of 1600m2 space
    space=[160,100]
    pos=pd.read_excel(r'/home/omata-lab-3/Epidemic Math/initpos_free.xlsx').to_numpy() # init_pos(space,N)
    vel=pd.read_excel(r'/home/omata-lab-3/Epidemic Math/control_vel.xlsx').to_numpy() #particle_motion.init_velo(N)
    dt=1 #0.01
    
    determine=np.zeros((N,N),dtype=str)
    for i in range(N):
        for j in range(N):
            determine[i][j]="N"
            
    status,inf_id=particle_status.init_status(N)
    tsince_infected=np.zeros(N)
    infecting_time=np.zeros(N)
    
    SIR_data=np.zeros((86400,3))
    avg_deninf=np.zeros(86400)
    total_idinf=0
    second_infect=np.zeros(86400)
    
    med_deninf=np.zeros(86400)
    
    fig = plt.figure()
    fig.set_dpi(100)
    ax1 = fig.add_subplot(1,1,1)
    
    flow=1
    
    for i in range(86400):
        pos=particle_motion.update_movementa(pos, vel, dt, space,i) #pos,flow=update_movementb for wall
        status,infecting_time,determine,total_idinf,avg_deninf[i],med_deninf[i]=particle_status.update_status2(status,pos,tsince_infected,infecting_time,determine,inf_id,total_idinf)
        tsince_infected=particle_status.check_time(status, tsince_infected, dt)
        
        SIR_data[i][0]=particle_status.sir_count(status)[0]
        SIR_data[i][1]=particle_status.sir_count(status)[1]
        SIR_data[i][2]=particle_status.sir_count(status)[2]
        second_infect[i]=total_idinf
        
        '''
        if i%10==0:
            ax1.clear()
            
            #ax1.xaxis.set_ticks([0,100,200,300,400,500,600,700,800])
            #ax1.yaxis.set_ticks([0,20])
            ax1.xaxis.set_ticks([0,20,40,60,80,100,120,140,160,180])
            ax1.yaxis.set_ticks([0,20,40,60,80,100])
            ax1.set_aspect('equal')
            #ax1.set_aspect(2)
            ax1.grid()
            
            ax1.add_patch(
                plt.Rectangle((0,0),90,100,color="red",alpha=0.1)
                )
            ax1.add_patch(
                plt.Rectangle((90,0),90,100,color="red",alpha=0.1)
                )
            
            
            ax1.add_patch(
                plt.Rectangle((80,0),20,40,color="black")
                )
            ax1.add_patch(
                plt.Rectangle((80,60),20,40,color="black")
                )
            
            
            #long tunnel
            ax1.add_patch(
                plt.Rectangle((0,0),400,20,color="red",alpha=0.1)
                )
            ax1.add_patch(
                plt.Rectangle((400,0),400,20,color="red",alpha=0.1)
                )
            #long tunnel
            
            
            plt.xlim([0.0, space[0]])
            plt.ylim([0.0, space[1]]) 
            
            colors=[]
            for j in range(len(status)):
                if status[j]=="I":
                    colors.append("red")
                elif status[j]=="R":
                    colors.append("green")
                else:
                     colors.append("blue")
            ax1.scatter(pos[:,0],pos[:,1],s=10*2**0.2,c=colors)
            #ax1.scatter(pos[:,0],pos[:,1],s=20*2**0.2,facecolors='none',edgecolors='blue',linestyle='--')
            plt.savefig(f'/home/omata-lab-3/Epidemic Math/gate100_60/pic_0{i+1}.png')
               
            #if i%10000==0:
             #   print("10000 s passed")
          '''
        
        
    print(datetime.now() - startTime)
    
   
    np.save(f'/home/omata-lab-3/Epidemic Math/free(100,30) trial results/fttt{file+1}.npy',SIR_data)
    np.save(f'/home/omata-lab-3/Epidemic Math/free(100,30) trial results/fttt{file+1}_second.npy',second_infect)
    np.save(f'/home/omata-lab-3/Epidemic Math/free(100,30) trial results/fttt{file+1}_density.npy',avg_deninf)
    np.save(f'/home/omata-lab-3/Epidemic Math/free(100,30) trial results/fttt{file+1}_meden.npy',med_deninf)


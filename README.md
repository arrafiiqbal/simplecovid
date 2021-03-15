# simplecovid

## simplecovid is a particle simulation to model the spread of epidemic within a city.

The simulation contains two main scripts. The first one is *particle_motion.py* which describe how each particle moves and their behaviors, and the second one is *particle_status.py* which describe how the virus spread will occur from one particle to another. 

### Particle Motion
The motion of the particle is described using newton equation. With following assumptions:
- All particle is assumed to be identical with (*m=1, r=1*)
- Collision between particles is assumed to be inelastic with *coefficient of restitution*
- For every *t* where *t mod 3600 = 0*. New initial velocity for each particle is randomly generated with *|v_i|=0.07*

### Particle Status
Using the information gathered from WHO and any other health organization. The following assumptions on virus spread are decided:
- Infectee has radius of infection *r=1*
- *Threshold time* and *Infection probability* are parameters used to decide whether or not new infection occur

Threshold time
: For non-infected person, if spend time within the radius of infection >= this time, then he/she has probability to be infected. 
Infection probability
: The probability of non-infectee to be infected. The decision occur only once.



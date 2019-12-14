import meep as mp
from meep import mpb
import numpy as np
import matplotlib.pyplot as plt

resolution = 20   # pixels/um

eps = 12          # dielectric constant of holes
r = 0.2           # radius of holes
d = 1.4           # defect spacing (ordinary spacing = 1)
N = 21

sy = N          
sx = N
pad = 2           
dpml = 1          

end_disk = int(N/2)


cell = mp.Vector3(sx,sy,0)

geometry = []
for i in range(N):
	for j in range(N):
		geometry.append(mp.Cylinder(radius=r,center=mp.Vector3(-end_disk+i,-end_disk+j),height=mp.inf,material=mp.Medium(epsilon=eps)))

for i in range(N):
	geometry.append(mp.Cylinder(radius=r,center=mp.Vector3(-end_disk+i,0),height=mp.inf,material=mp.Medium(epsilon=1)))


sources = [mp.Source(mp.ContinuousSource(wavelength=2.5),
                     component=mp.Ez,
                     center=mp.Vector3(-end_disk+1,0))]

pml_layers = [mp.PML(dpml)]
resolution = 20

sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)

animate = mp.Animate2D(sim,
                       fields=mp.Ez,
                       realtime=True,
                       field_parameters={'alpha':0.5, 'cmap':'RdBu', 'interpolation':'none'},
                       boundary_parameters={'hatch':'o', 'linewidth':1.5, 'facecolor':'y', 'edgecolor':'b', 'alpha':0.0})

sim.run(mp.at_every(1,animate),until=50)
animate.to_gif(fps=2,filename='photonicwaveguide.gif')
# sim.run(mp.at_beginning(mp.output_epsilon),
#         mp.to_appended("ez", mp.at_every(0.25, mp.output_efield_z)),
#         until=50)

# eps_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Dielectric)
# plt.figure()
# plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
# plt.axis('off')
# plt.show()

# ez_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
# plt.figure()
# plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
# plt.imshow(ez_data.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.9)
# plt.axis('off')
# plt.show()



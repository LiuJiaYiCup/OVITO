from ovito.modifiers import *
from ovito.io import *
import numpy as np

num_bins = 100
cutoff = 9.5

node = import_file("C:/work/Bottom_result1_H2O.dump")
node.add_to_scene()

create_bonds_modifier = CreateBondsModifier(cutoff=cutoff, mode=CreateBondsModifier.Mode.Pairwise)
create_bonds_modifier.set_pairwise_cutoff('Type 4', 'Type 4', cutoff)
node.modifiers.append(create_bonds_modifier)
node.modifiers.append(ComputeBondLengthsModifier())

output = node.compute()
hist, bin_edges = np.histogram(output.bond_properties.length.array, bins=num_bins)

rho = output.number_of_particles / output.cell.volume
factor = 4./3. * np.pi * rho * output.number_of_particles

radii = bin_edges[:-1]
radii_right = bin_edges[1:]
rdf = hist / (factor * (radii_right**3 - radii**3))

result = np.column_stack((radii,rdf))

print(result)
np.savetxt("C:\work\partial_Bottom_result1_H2O.dat", result)
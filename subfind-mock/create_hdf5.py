import h5py
import pandas as pd
import numpy as np
import sys 

n_files = int(sys.argv[1]) #n_files = 1
n_particles = int(sys.argv[2]) #
p_dir = sys.argv[3] # p_dir = './particle-dir'
hdf5_dir = sys.argv[4]
snapNum = int(sys.argv[5])

print('snapshot:', snapNum)
print('chunks:', n_files, '\n') 

halos_keys = ['ID', 'Np', 'Np_child', 'Mvir', 'Rvir', 
              'X', 'Y', 'Z', 'Vx', 'Vy', 'Vz', 'Jx', 'Jy', 'Jz', 
              'A[x]', 'A[y]', 'A[z]', 'A[x](500c)', 'A[y](500c)', 'A[z](500c)', 
              'M200b', 'M200c', 'M500c', 'M2500c', 
              'b_to_a', 'c_to_a', 'b_to_a(500c)', 'c_to_a(500c)', 'Xoff', 'Voff',
              'T/|U|', 'M_pe_Behroozi', 'M_pe_Diemer', 'Spin', 'spin_bullock', 
              'Rs', 'rs_klypin', 'Vmax', 'Vrms', 'DescID', 'Mvir_all', 'Halfmass_Radius']

header_keys = ['snap', 'chunk', 'Om', 'Ol', 'H0', 
               'num_halos', 'num_particles', 'particle_mass', 'box_size']

p_sum = 0

df_total_halos = pd.DataFrame(columns=halos_keys)

# create group files
for i in range(0, n_files):
    print('chunk:', i);
    # open header file for gen file information 
    f_header = p_dir + '/header_%d.%d.list'%(snapNum, i)
    df_header = pd.read_csv(f_header, delimiter=" ", header=None, names=header_keys, skiprows=[0])

    print('# particles in chunk:', df_header['num_particles'].values) 
  
    # load particles into a Nx1 numpy array
    f_particles = p_dir + '/particles_%d.%d.list'%(snapNum, i)
 
    # create snapshot hdf5 file
    snap = h5py.File(hdf5_dir + "/snapdir_%03d/snap_%03d.%d.hdf5"%(snapNum, snapNum, i), 'w')
    
    # create group Header
    header = snap.create_group("Header")
    # header attributes
    header.attrs.create('NumFilesPerSnapshot', data=n_files, dtype='int32') # how many files per snapshot 
    header.attrs.create('NumPart_Total', data=[0, n_particles**3 % 2**32, 0, 0, 0, 0], dtype='uint32') # how many particles total in the simulation run 
    header.attrs.create('NumPart_Total_HighWord', data=[0, np.floor(n_particles**3 / 2**32), 0, 0, 0, 0], dtype='uint32')
    header.attrs.create('NumPart_ThisFile', data=[0, df_header['num_particles'].values, 0, 0, 0, 0], dtype='int32') # how many particles in this file

    df_particles = pd.DataFrame()

    # if num_particles < 1, there are no halos thus we can skip this file
    if (df_header['num_particles'].values == 0):
        print('writing empty snap chunk file...')
    else:
        print('reading chunk file...') 
        df_particles = pd.read_csv(f_particles, header=None)[0].values

    # create group PartType1
    PartType1 = snap.create_group("PartType1")
    # PartType1 
    particleIDs = PartType1.create_dataset("ParticleIDs", df_particles.shape, dtype='<u8', data = df_particles)
    p_sum = p_sum + (df_particles.shape[0])
    snap.close()
    
    # open respective halo file and append to total halo dataframe
    f_halos = p_dir + '/halos_%d.%d.list'%(snapNum, i) 
    df_halos = pd.read_csv(f_halos, delimiter=" ", index_col = False)
    df_total_halos = df_total_halos.append(df_halos).reset_index(drop=True)
    print('chunk finished\n\n')     

print('snapdir finished') 
print('n_particles:', p_sum) 

df_total_halos['0'] = 0

print('n_halos:', df_total_halos.shape[0])

group = h5py.File(hdf5_dir + "/groups_%03d/fof_subhalo_tab_%03d.0.hdf5"%(snapNum, snapNum), "w")

# create group Header
header = group.create_group("Header")
# header attributes
header.attrs.create('Ngroups_Total', data=df_total_halos.shape[0], dtype='uint32') # how many total parent halos (fof groups) there are
header.attrs.create('Nsubgroups_Total', data=df_total_halos.shape[0], dtype='uint32')  # how many total subhalos there are
header.attrs.create('Ngroups_ThisFile', data=df_total_halos.shape[0], dtype='uint32')  # how many parent halos (fof groups) in this file
header.attrs.create('Nsubgroups_ThisFile', data=df_total_halos.shape[0], dtype='uint32')  # how many subhalos there are in this file 
header.attrs.create('NumFiles', data=1, dtype='int32') # how many files 

# create group groups
groups = group.create_group("Group")

if df_total_halos.shape[0] < 1:
    print('writing empty group fof file...')
    group.close()
    exit()

# groups datasets 
groupnsubs = groups.create_dataset("GroupNsubs", (df_total_halos.shape[0],), dtype='int32',
                                  data=np.ones(df_total_halos.shape[0])) #
grouplentype = groups.create_dataset("GroupLenType", (df_total_halos.shape[0], 6), dtype='int32',
                                    data=df_total_halos[['0', 'Np', '0', '0', '0', '0']].values.astype(float))

# create group subhalos
subhalos = group.create_group("Subhalo")
# subhalos datasets
subhalogrnr = subhalos.create_dataset("SubhaloGrNr", (df_total_halos.shape[0],), 
                                        dtype='int32', data = np.linspace(0, df_total_halos.shape[0] - 1, df_total_halos.shape[0]).astype(float)) # ID of parent halo of each subhalo 
subhalolentype = subhalos.create_dataset("SubhaloLenType", (df_total_halos.shape[0], 6), 
                                         dtype='int32', data = df_total_halos[['0', 'Np', '0', '0', '0', '0']].values.astype(float)) # num DM particles of each subhalo in col 2
subhalomasstype = subhalos.create_dataset("SubhaloMassType", (df_total_halos.shape[0], 6), 
                                          dtype='<f4', data = df_total_halos[['0', 'Mvir', '0', '0', '0', '0']].values) # DM mass of each subhalo in col 2

# additional quantities for reformatting 
subhalo_id = subhalos.create_dataset("Subhalo_ID", (df_total_halos.shape[0],), 
                                           dtype='uint32', data = df_total_halos['ID'].values.astype(float))

subhalovel = subhalos.create_dataset("SubhaloVel", (df_total_halos.shape[0], 3), 
                                          dtype='<f4', data = df_total_halos[['Vx', 'Vy', 'Vz']].values)
subhalopos = subhalos.create_dataset("SubhaloPos", (df_total_halos.shape[0], 3), 
                                          dtype='<f4', data = df_total_halos[['X', 'Y', 'Z']].values)
subhaloangmom = subhalos.create_dataset("SubhaloAngMom", (df_total_halos.shape[0], 3), 
                                          dtype='<f4', data = df_total_halos[['Jx', 'Jy', 'Jz']].values)
subhaloaxis = subhalos.create_dataset("SubhaloAxis", (df_total_halos.shape[0], 3), 
                                          dtype='<f4', data = df_total_halos[['A[x]', 'A[y]', 'A[z]']].values)
subhaloaxis_500c = subhalos.create_dataset("SubhaloAxis_500c", (df_total_halos.shape[0], 3), 
                                          dtype='<f4', data = df_total_halos[['A[x](500c)', 'A[y](500c)', 'A[z](500c)']].values)

subhalo_M200b = subhalos.create_dataset("Subhalo_M200b", (df_total_halos.shape[0], ), 
                                          dtype='<f4', data = df_total_halos['M200b'].values)
subhalo_M200c = subhalos.create_dataset("Subhalo_M200c", (df_total_halos.shape[0], ), 
                                          dtype='<f4', data = df_total_halos['M200c'].values)
subhalo_M500c = subhalos.create_dataset("Subhalo_M500c", (df_total_halos.shape[0], ), 
                                          dtype='<f4', data = df_total_halos['M500c'].values)
subhalo_M2500c = subhalos.create_dataset("Subhalo_M2500c", (df_total_halos.shape[0], ), 
                                          dtype='<f4', data = df_total_halos['M2500c'].values)
subhalo_Mvir_all = subhalos.create_dataset("Subhalo_Mvir_all", (df_total_halos.shape[0], ), 
                                          dtype='<f4', data = df_total_halos['Mvir_all'].values)
subhalo_Mpe_Behroozi = subhalos.create_dataset("Subhalo_Mpe_Behroozi", (df_total_halos.shape[0], ), 
                                          dtype='<f4', data = df_total_halos['M_pe_Behroozi'].values)
subhalo_Mpe_Diemer = subhalos.create_dataset("Subhalo_Mpe_Diemer", (df_total_halos.shape[0], ), 
                                          dtype='<f4', data = df_total_halos['M_pe_Diemer'].values)

subhalo_b_to_a = subhalos.create_dataset("Subhalo_b_to_a", (df_total_halos.shape[0], ), 
                                          dtype='<f4', data = df_total_halos['b_to_a'].values)
subhalo_c_to_a = subhalos.create_dataset("Subhalo_c_to_a", (df_total_halos.shape[0], ), 
                                          dtype='<f4', data = df_total_halos['c_to_a'].values)
subhalo_b_to_a_500c = subhalos.create_dataset("Subhalo_b_to_a_500c", (df_total_halos.shape[0], ), 
                                          dtype='<f4', data = df_total_halos['b_to_a(500c)'].values)
subhalo_c_to_a_500c = subhalos.create_dataset("Subhalo_c_to_a_500c", (df_total_halos.shape[0], ), 
                                          dtype='<f4', data = df_total_halos['c_to_a(500c)'].values)

subhalo_xoff = subhalos.create_dataset("Subhalo_Xoff", (df_total_halos.shape[0], ), 
                                          dtype='<f4', data = df_total_halos['Xoff'].values)
subhalo_voff = subhalos.create_dataset("Subhalo_Voff", (df_total_halos.shape[0], ), 
                                          dtype='<f4', data = df_total_halos['Voff'].values)

subhalo_spin = subhalos.create_dataset("Subhalo_Spin", (df_total_halos.shape[0], ), 
                                          dtype='<f4', data = df_total_halos['Spin'].values)
subhalo_spin_bullock = subhalos.create_dataset("Subhalo_Spin_bullock", (df_total_halos.shape[0], ), 
                                          dtype='<f4', data = df_total_halos['spin_bullock'].values)

subhalo_vmax = subhalos.create_dataset("Subhalo_Vmax", (df_total_halos.shape[0], ), 
                                          dtype='<f4', data = df_total_halos['Vmax'].values)
subhalo_vrms = subhalos.create_dataset("Subhalo_Vrms", (df_total_halos.shape[0], ), 
                                          dtype='<f4', data = df_total_halos['Vrms'].values)

subhalo_rvir = subhalos.create_dataset("Subhalo_Rvir", (df_total_halos.shape[0], ), 
                                          dtype='<f4', data = df_total_halos['Rvir'].values)
subhalo_rs = subhalos.create_dataset("Subhalo_Rscale", (df_total_halos.shape[0], ), 
                                          dtype='<f4', data = df_total_halos['Rs'].values)
subhalo_rs_klypin = subhalos.create_dataset("Subhalo_Rscale_Klypin", (df_total_halos.shape[0], ), 
                                          dtype='<f4', data = df_total_halos['rs_klypin'].values)
subhalo_rhalfmass = subhalos.create_dataset("Subhalo_Rhalfmass", (df_total_halos.shape[0], ), 
                                          dtype='<f4', data = df_total_halos['Halfmass_Radius'].values)

subhalo_energy_ratio = subhalos.create_dataset("Subhalo_Energy_Ratio", (df_total_halos.shape[0], ), 
                                          dtype='<f4', data = df_total_halos['T/|U|'].values)

group.close()

print('group finished')

df_total_halos.to_hdf(hdf5_dir + "/groups_%03d/out_%03d.hdf5"%(snapNum, snapNum), key='df', mode='w')

print('out.list finished')

#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <inttypes.h>

#include "/home/agabrielpillai/scripts/rockstar-bin-reader/rockstar/check_syscalls.c"
#include "/home/agabrielpillai/scripts/rockstar-bin-reader/rockstar/halo.h"
#include "/home/agabrielpillai/scripts/rockstar-bin-reader/rockstar/io/io_internal.h" 

int currSnap; 

void printHalo(int num, struct binary_output_header *bh, struct halo *halos, int64_t *part_ids){
	// print binary halo header information 
	char headname[] = "header_";
	char intbuff[100];
	sprintf(intbuff, "%d", currSnap);
        strcat(headname, intbuff);
        strcat(headname, ".");	

	sprintf(intbuff, "%d", num); 
	strcat(headname, intbuff);
	strcat(headname, ".list");

	// open header file for writing 
	freopen(headname, "w", stdout);
	printf("#snap chunk Om Ol H0 num_halos num_particles particle_mass box_size \n");
	printf("%" PRId64 " ", bh->snap);
        printf("%" PRId64 " ", bh->chunk);
        printf("%f ", bh->Om);
        printf("%f ", bh->Ol);
        printf("%f ", bh->h0);
        printf("%" PRId64 " ", bh->num_halos);
        printf("%" PRId64 " ", bh->num_particles);
        printf("%f ", bh->particle_mass);
        printf("%f", bh->box_size);
	printf("\n"); 

	int nhalos = bh->num_halos;
//	nhalos = 10; 
		
	// create filename based on part
	char fname[] = "halos_";
	sprintf(intbuff, "%d", currSnap);
	strcat(fname, intbuff);
	strcat(fname, ".");

	sprintf(intbuff, "%d", num);
	strcat(fname, intbuff);
	strcat(fname, ".list");

	// create file for halo information 
        freopen(fname, "w", stdout);

	// comment top line for attributes 
	printf("ID Np Np_child Mvir Rvir X Y Z Vx Vy Vz Jx Jy Jz A[x] A[y] A[z] A[x](500c) A[y](500c) A[z](500c) M200b M200c M500c M2500c b_to_a c_to_a b_to_a(500c) c_to_a(500c) Xoff Voff T/|U| M_pe_Behroozi M_pe_Diemer Spin spin_bullock Rs rs_klypin Vmax Vrms DescID Mvir_all Halfmass_Radius\n"); 	

	// declare i before c99 compilier 
	int i;	

	// iterate through all halos in the file
	for (i = 0; i < nhalos; i++){
		// halo information 
		printf("%" PRId64 " ", halos[i].id); // halo id
		printf("%" PRId64 " ", halos[i].num_p); // how many particles
		printf("%" PRId64 " ", halos[i].num_child_particles); //how many child particles    
               
	        printf("%f ", halos[i].mgrav); // halo mass (mvir)
                printf("%f ", halos[i].r); // halo radius (rvir)
           
                printf("%f %f %f ", halos[i].pos[0], halos[i].pos[1], halos[i].pos[2]); // position components
		printf("%f %f %f ", halos[i].pos[3], halos[i].pos[4], halos[i].pos[5]); // veloctiy components 
		printf("%f %f %f ", halos[i].J[0], halos[i].J[1], halos[i].J[2]); // angular momentum components
	
		printf("%f %f %f ", halos[i].A[0], halos[i].A[1], halos[i].A[2]); //A components for 200c
		printf("%f %f %f ", halos[i].A2[0], halos[i].A2[1], halos[i].A[2]); //A components for 500c
		
		printf("%f %f %f %f ", halos[i].alt_m[0], halos[i].alt_m[1], halos[i].alt_m[1], halos[i].alt_m[2]); //alt m defs
		
		printf("%f %f %f %f ", halos[i].b_to_a, halos[i].c_to_a, halos[i].b_to_a2, halos[i].c_to_a2); // unsure, ratios?

		printf("%f %f ", halos[i].Xoff, halos[i].Voff); // error offsets? 

		printf("%f %f %f ", halos[i].kin_to_pot, halos[i].m_pe_b, halos[i].m_pe_d); // energy quantities

		printf("%f %f ", halos[i].spin, halos[i].bullock_spin); // spin quantities  

		printf("%f %f ", halos[i].rs, halos[i].klypin_rs); //scale radius quantities

                printf("%f %f ", halos[i].vmax, halos[i].vrms); //other velocity quantitiesi

		printf("%" PRId64 " ", halos[i].desc); //descendent id
		printf("%f ", halos[i].m); //alt mass def
		printf("%f\n", halos[i].halfmass_radius); // halfmass radius
	}


	// file for particle ids 
	char partname[] = "particles_";
	sprintf(intbuff, "%d", currSnap);
	strcat(partname, intbuff);
	strcat(partname, "."); 

        sprintf(intbuff, "%d", num);
	strcat(partname, intbuff);  
        strcat(partname, ".list");
	freopen(partname, "w", stdout);

	int max = nhalos;
	for (i = 0; i < max; i++){
		// index of where the particles should start in part_ids
		int p_start = halos[i].p_start;
		// how many particles in this halo
		int num_p = halos[i].num_p;
		int j;
		for (j = p_start; j < p_start + num_p; j++){
			printf("%" PRId64 "\n", part_ids[j]);
		}
		 printf("\n");
	}	
	
	return;
}

int main(int argc, char *argv[]){
	int64_t *part_ids = NULL;
	struct halo *halos = NULL;
	struct binary_output_header bh;
	
	int k = 0;  

	int z = atoi(argv[1]);
	int z_end = atoi(argv[2]);
	int n_files = atoi(argv[3]);

	
	for (; z < z_end + 1; z++){
		for (; k < n_files; k++){
			// call function from 
			currSnap = z; 

			load_binary_halos(z, k, &bh, &halos, &part_ids, 0);
			printf("\n");
	
			printHalo(k, &bh, halos, part_ids);	
			printf("\n");
		}
	}

	return 0;
}


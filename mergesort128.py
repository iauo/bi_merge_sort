import numpy as np
minimum_data = -1000
maximum_data =  1000
top_sort_direction = bool(1)# 0:decrease, 1:increase

def cmp128(datai, mode, cmp_distance, sub_seqlen):#process 128 data at a time
	data=datai.copy()
	for sub_seq_idx in range(int(len(data)/sub_seqlen)):
		subdata = data[sub_seq_idx*sub_seqlen:sub_seq_idx*sub_seqlen+sub_seqlen ]
		if(mode==0 or mode==1):sort_direction=mode 
		elif(mode==2):sort_direction=sub_seq_idx%2
		elif(mode==3):sort_direction=(sub_seq_idx+1)%2
		half_dis = int(len(subdata)/2)
		jump_times = int(half_dis/cmp_distance)
		for jump_times_idx in range(jump_times):
			for cmp_distance_idx in range(cmp_distance):
				i = jump_times_idx * (2*cmp_distance) + cmp_distance_idx 
				# print(jump_times_idx, cmp_distance_idx, i)
				if(sort_direction):#1,increase 
					if(subdata[i] > subdata[i + cmp_distance]):
						subdata[i] ,  subdata[i + cmp_distance] =  subdata[i + cmp_distance], subdata[i] 
				else:#decrease
					if(subdata[i] < subdata[i + cmp_distance]):
						subdata[i] ,  subdata[i + cmp_distance] =  subdata[i + cmp_distance], subdata[i] 
		data[sub_seq_idx*sub_seqlen:sub_seq_idx*sub_seqlen+sub_seqlen ] = subdata
	return data

def bi_merge_sort_top(input):
	top_seqlen = len(input)
	top_value_each_step = input.copy()
	# step0, sort each seq128
	assigned_direction = top_sort_direction 
	for i in range(int(top_seqlen/128)):
		seq128 = top_value_each_step[i*128:i*128+128]
		sub_seqlen=1
		for j in range(7):
			sub_seqlen = sub_seqlen*2 
			sub_seq_steps = j+1
			cmp_distance = sub_seqlen
			for sub_seq_step_idx in range(sub_seq_steps):
				cmp_distance=int(cmp_distance/2)
				seq128 = cmp128(seq128, 2 + assigned_direction, cmp_distance, sub_seqlen )
				# print(i,j,sub_seq_step_idx,assigned_direction,cmp_distance, "\n",seq128)
		top_value_each_step[i*128:i*128+128] = seq128
		assigned_direction = not assigned_direction
	#step1,step2,... bi sort, based on sorted seq128 series
	top_steps = len(bin(int(top_seqlen/128))) - 2# log2(seqlen/128)
	for top_step_idx in range(top_steps):
		assigned_direction = top_sort_direction 
		sub_steps = top_step_idx + 1
		sub_seqlen = pow(2, sub_steps)*128
		for sub_seq_idx in range(int(top_seqlen/sub_seqlen)):
			seqmulti128=  top_value_each_step[i*sub_seqlen:i*sub_seqlen+sub_seqlen] 
			cmp_distance = int(sub_seqlen/2)
			for sub_step_idx in range(sub_steps + 7):
				cmp_distance = int(cmp_distance/2)
				seqmulti128 = cmp128(seqmulti128, assigned_direction, cmp_distance)
			assigned_direction = not assigned_direction
			top_value_each_step[i*sub_seqlen:i*sub_seqlen+sub_seqlen]=seqmulti128 
		# print(top_value_each_step)
	return top_value_each_step

def preprocess(a):#pad data into length of 2^n
	alen = len(a)
	if((alen & (alen-1)) != 0) :#if not 2^n
		actual_len = len(bin(alen))  - 2 
		pow2_len = pow(2, actual_len)
		ending_value = np.empty([pow2_len - alen],dtype=int)
		if(top_sort_direction):ending_value[:] =maximum_data
		else:ending_value[:] =minimum_data 
		a = np.append(a, ending_value)
	return a

# alen = 10000#np.random.randint(1,pow(2,14))
# for i in range(1):
np.random.seed(0)	
alen = 122#np.random.randint(1,pow(2,4))
original_input = np.random.randint(minimum_data,maximum_data,[alen])
pre_input = preprocess(original_input )
dut = bi_merge_sort_top(pre_input)
golden = np.sort(pre_input)
if(top_sort_direction==False):
	golden=golden[::-1]
if((golden==dut).all()):
	print("PASS...")
else:
	print("FAIL")
	np.savetxt("golden.txt",golden, fmt="%d",delimiter=" ")
	np.savetxt("dut.txt",dut,fmt="%d",delimiter=" ")
	exit(0)	

# test = np.array(
# [-441,-316,653,216,731,383,-237,-165,33,-723,778,747,496,828
# ,-401,94,-400,-686,-295,420,-449,510,-826,-913,-151,-463,701,624
# ,940,-155,-928,-223,-885,-245,733,-24,455,871,-150,-552,-901,-245
# ,-203,201,-90,171,-341,-577,289,-303,312,985,-286,-361,-456,-457
# ,-849,-756,-325,-490,207,483,-118,-972,-872,-872,956,-198,574,925
# ,77,512,-727,-665,-612,-244,466,641,66,-457,-743,-112,961,345
# ,894,143,-943,-709,-570,-909,106,-221,589,920,-602,-389,-367,-916
# ,962,-92,-36,-226,-797,-676,-361,-28,155,71,870,204,-132,167
# ,-46,-209,251,684,877,-91,-281,-627,-440,329,1000,1000,1000,1000
# ,1000,1000])
# temp = cmp128(test,3,1,4 )
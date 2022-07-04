from filecmp import cmp
from subprocess import call
import numpy as np
minimum_data = -1000
maximum_data =  1000
top_sort_direction = bool(1)# 0:decrease, 1:increase

def halfcomp(data, cmp_distance, sort_direction):#data 1 False
	half_dis = int(len(data)/2)
	jump_times = int(half_dis/cmp_distance)
	for jump_times_idx in range(jump_times):
		for cmp_distance_idx in range(cmp_distance):
			i = jump_times_idx * (2*cmp_distance) + cmp_distance_idx 
			# print(jump_times_idx, cmp_distance_idx, i)
			if(sort_direction):#1,increase 
				if(data[i] > data[i + cmp_distance]):
					temp = data[i]
					data[i] =  data[i + cmp_distance]
					data[i + cmp_distance] = temp
			else:#decrease
				if(data[i] < data[i + cmp_distance]):
					temp = data[i]
					data[i] =  data[i + cmp_distance]
					data[i + cmp_distance] = temp
	return data
def sub_seq_gen(sub_seq,  sort_direction):
	sub_seqlen = int(len(sub_seq))
	sub_steps  = len(bin(sub_seqlen)) - 2 -1 
	sub_div2_seqlen = int( sub_seqlen/2 )
	# seq0 = sub_seq[0:sub_div2_seqlen]
	# seq1 = sub_seq[sub_div2_seqlen:2*sub_div2_seqlen]
	for sub_step_idx in range(sub_steps): 
		cmp_distance = int(sub_div2_seqlen/(pow(2, sub_step_idx)))
		sub_seq = halfcomp(sub_seq,  cmp_distance , sort_direction)
		# print(sub_step_idx,sub_seq, cmp_distance, sort_direction)
	return sub_seq

def top_step_process(top_value_each_step,call_subseq_times, sub_seqlen ):
	for sub_seq_index in range(call_subseq_times):
		the_sub_seq_to_be_processed =top_value_each_step[sub_seqlen*sub_seq_index:sub_seqlen*(sub_seq_index+1)] 
		if(sub_seq_index%2==0):#even seq index, same with top direction
			top_value_each_step[sub_seqlen*sub_seq_index:sub_seqlen*(sub_seq_index+1)] = sub_seq_gen(the_sub_seq_to_be_processed, top_sort_direction )
		else:#odd seq index, inverse with top direction
			top_value_each_step[sub_seqlen*sub_seq_index:sub_seqlen*(sub_seq_index+1)] = sub_seq_gen(the_sub_seq_to_be_processed, not top_sort_direction )
	return top_value_each_step

def bit_merge_sort_top(input):
	top_seqlen = len(input)
	top_steps = len(bin(top_seqlen)) - 2
	top_value_each_step = input.copy()
	# print(input)
	for top_step_idx in range(top_steps):
		sub_steps = top_step_idx + 1
		sub_seqlen = pow(2, sub_steps)
		call_subseq_times = int(top_seqlen/sub_seqlen) 
		top_value_each_step = top_step_process(top_value_each_step,call_subseq_times, sub_seqlen)
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
for i in range(1000):
	np.random.seed(i)	
	alen = np.random.randint(1,pow(2,14))
	original_input = np.random.randint(minimum_data,maximum_data,[alen])
	pre_input = preprocess(original_input )
	dut= bit_merge_sort_top(pre_input)

	# top_sort_direction = bool(0)# 0:decrease, 1:increase
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

# test = np.array([534, 406, 346, 389])
# temp = halfcomp(test,1, False)
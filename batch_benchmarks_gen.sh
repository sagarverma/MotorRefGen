python motorrefgen/gen_custom_pkls.py \
--save_dir=../../datasets/Data_11052020_exponential_dist_ramps/benchmarks \
--speed_time=0,1,2,5 --torque_time=0,1,2,5 \
--reference_speed=0,0,50,50 --reference_torque=0,0,0,0 \
--sim_rate=0.004 --benchmark_name=bench1

python motorrefgen/gen_custom_pkls.py \
--save_dir=../../datasets/Data_11052020_exponential_dist_ramps/benchmarks \
--speed_time=0,1,2,3,4,5,6,7,8 --torque_time=0,1,2,3,4,5,6,7,8 \
--reference_speed=0,0,5,5,5,5,5,50,50 --reference_torque=0,0,0,0,50,50,50,50,50 \
--sim_rate=0.004 --benchmark_name=bench2

python motorrefgen/gen_custom_pkls.py \
--save_dir=../../datasets/Data_11052020_exponential_dist_ramps/benchmarks \
--speed_time=0,1,2,3,4,5,6,7,8 --torque_time=0,1,2,3,4,5,6,7,8 \
--reference_speed=0,0,5,5,5,50,50,-50,-50 --reference_torque=0,0,0,0,50,50,50,50,50 \
--sim_rate=0.004 --benchmark_name=bench3

python motorrefgen/gen_custom_pkls.py \
--save_dir=../../datasets/Data_11052020_exponential_dist_ramps/benchmarks \
--speed_time=0,1,2,3,3.004,5 --torque_time=0,1,2,3,3.004,5 \
--reference_speed=0,0,25,25,25,25 --reference_torque=0,0,0,0,100,100 \
--sim_rate=0.004 --benchmark_name=bench4

python motorrefgen/gen_custom_pkls.py \
--save_dir=../../datasets/Data_11052020_exponential_dist_ramps/benchmarks \
--speed_time=0,1,1.004,5,55,60 --torque_time=0,1,1.004,5,55,60 \
--reference_speed=0,0,70,70,-70,-70 --reference_torque=0,0,0,0,0,0 \
--sim_rate=0.004 --benchmark_name=bench5


python motorrefgen/gen_custom_pkls.py \
--save_dir=../../datasets/Data_11052020_exponential_dist_ramps/benchmarks \
--speed_time=0,1,1.004,5,55,60 --torque_time=0,1,1.004,5,55,60 \
--reference_speed=0,0,70,70,-70,-70 --reference_torque=0,0,0,0,0,0 \
--sim_rate=0.004 --benchmark_name=bench5

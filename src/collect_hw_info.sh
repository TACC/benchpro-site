#!/bin/bash 

if [ -z $1 ]
then
	echo "1. Provide util dir"
	exit 1
fi

if [ -z $2 ]
then
	echo "2. Provide dest dir"
	exit 1
fi

utils_dir=$1
output_dir=$2

mkdir -p ${output_dir}

label=(	cpuid.all.raw 
		cpuid.core0 
		lshw 
		TACC_HWP_set 
		lspci 
		rdmsr_all 
		rpm 
		ml 
		lscpu
		) 

cmd=(	"${utils_dir}/cpuid -r"
		"${utils_dir}/cpuid -1"
		"${utils_dir}/lshw"
		"${utils_dir}/TACC_HWP_set -v -s"
		"${utils_dir}/lspci -xxx"
		"${utils_dir}/rdmsr_all"
		"rpm -qa"
		"ml"
		"lscpu"
		)

for ((i=0;i<${#label[@]};++i)); do
	echo "Running ${label[i]}"
	${cmd[i]} &> ${output_dir}/${label[i]}
done
echo "Done."
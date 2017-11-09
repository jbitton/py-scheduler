#!/bin/bash

OUTDIR=${1:-.}

RFILE=../inputs/rfile
INS="0 1 2 3 4 5 6"

SCHPAR="F L S R2 R5 P2 P5"
for f in ${INS}; do
	for s in ${SCHPAR}; do 
		echo "python3.6 ../../scheduler.py -s${s} ../inputs/input${f} ${RFILE}"
		python3.6 ../../scheduler.py -s${s} ../inputs/input${f} ${RFILE} > ${OUTDIR}/output${f}_${s}
	done
done

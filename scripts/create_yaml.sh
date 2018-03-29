#!/bin/bash

# init yaml
echo -e 'seqname: nEDM-test\n\njobs:' > nedm-test.yaml

readlink -f /ccs/proj/nph118/scripts/MDC_Captures/capture_{0..4}{0..9}.pbs | while read f; do 
	if [ ! -e "$f" ]; then continue; fi
	NODES=$(grep -oP 'nodes=\d+' $f | sed 's/nodes=//')
	WALLTIME=$(grep -oP 'walltime=[^,]+' $f | sed 's/walltime=//')
	JOBNAME=$(basename "$f")
	echo -e "  ${JOBNAME}:\n    nodes: ${NODES}\n    walltime: \"${WALLTIME}\"\n    command: |+\n" >> nedm-test.yaml
	grep -vE '^#' $f | grep -v '^$' | sed 's/^/      /' >> nedm-test.yaml
	echo >> nedm-test.yaml
done
echo >> nedm-test.yaml
echo -e 'sequence:' >> nedm-test.yaml

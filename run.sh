qsub job -l nodes=$1:meltemi:ppn=$2 -v NODES=$1,PPN=$2
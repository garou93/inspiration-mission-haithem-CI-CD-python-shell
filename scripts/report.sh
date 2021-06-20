#!/bin/bash
#/ generate report of all results for a specific project
#/ Usage:
#/ ./report.sh -p <project> -h <help> -o <open> -r <radar>
#/        p|project    = name of the project
#/        b|build      = specify the local BO under it tests are running
#/        o|open       = if set, generated page index.html will be opened
#/        r|radar      = if set, a radar will be generated
#/        h|help       = to dispaly this message :-)

usage() { grep '^#/' "$0" | cut -c4-; }

STBTSDIR=/home/STBTSuite
OUTPUT=$STBTSDIR/Results
RADAR=radar

collect_results() {
	echo -e "\n--- COLLECT RESULTS ---"
	for f in *; do
		if [ "$f" != "radar" ]; then
			cd $f
			for g in *; do
				if [ -d "$g" ]; then
					if [ ! -L "$g" ]; then
						#[[ -z $first_result ]] && first_result=${g}
						local_path=`pwd`
						ln -s $local_path/${g} ../$runtime/${g}
					fi
				fi
			done
			cd ..
		fi
	done
}

generate_report() {
	stbt batch report *
}

build_radar() {
	echo -e "\n--- GET RESULTS AND BUILD RADAR ---"
	# call to parsing_result.py
	runtime_path=${OUTPUT}/${project}/${runtime}
	RESULT_SCRIPT_DIR=${build}/projects/trunk/scripts/get_result
	$RESULT_SCRIPT_DIR/parsing_result.py $runtime_path
	# copy the report directory in $radar
	if [ -d $RESULT_SCRIPT_DIR/html_report/report ]; then
		echo "  * cp -r $RESULT_SCRIPT_DIR/html_report/report $runtime_path"
		cp -r $RESULT_SCRIPT_DIR/html_report/report $runtime_path
	else
		echo "  * $RESULT_SCRIPT_DIR/html_report/report not found !!!"
	fi

}

main() {
	runtime=`date +%Y-%m-%d_%H-%M-%S`
	cd ${OUTPUT}/${project}
	mkdir ${runtime}
	collect_results
	cd ${runtime}
	generate_report
	cd ..
	if [ ! -d "$RADAR" ]; then
	  mkdir $RADAR
	fi
	[[ "$radar" = true ]] && build_radar
	mv ${runtime} ${RADAR}

	if [ $open = true ]; then
		firefox ${RADAR}/${runtime}/index.html 
		if [ $radar = true ]; then
			firefox ${RADAR}/${runtime}/report/report.html 
		fi
	fi
}


while getopts "horp:b:" OPT
do
    case $OPT in
        h)    usage >&2; exit 0    ;;
        p)    project=$OPTARG      ;;
		b)	  build=$OPTARG		   ;;
        o)    open=true            ;;
        r)    radar=true           ;;
        *)    usage >&2; exit 1    ;;
    esac
done

main


#!/bin/sh

bold() { tput bold; printf "%s" "$*"; tput sgr0; echo ""; }
green() { tput setaf 2; printf "%s" "$*"; tput sgr0; echo "";}
red() { tput setaf 1; printf "%s" "$*"; tput sgr0; echo "";}
yellow() { tput setaf 3; printf "%s" "$*"; tput sgr0; echo "";}

fail() { echo "$(red [FAILED] : $*)"; exit 1; }
skip() { echo "$(yellow [SKIPPED] : $*)"; exit 77; }
Done() { echo "$(green [INFO] : $*)"; }


set_config() {
	python - "$@" <<-EOF
	import stbt
	import sys, _stbt.config
	section, name = sys.argv[1].split('.')
	_stbt.config.set_config(section, name, sys.argv[2])
	EOF
}

set_control() {
	sed -i \
	-e 's,^control =.*,control = '$1',' \
	${STBT_CONFIG_FILE_CUSTOM}
}

set_stbt_conf() {
   #echo "sed -i -e 's,^'$1' =.*,'$1' = '$2' '$3' '$4' '$5' '$6',' ${STBT_CONFIG_FILE_CUSTOM}"
   if [ $6 == "!" ]; then
   sed -i -e 's,^'$1' =.*,'$1' = '$2' '$3' '$4' '$5' '$6' '$7' '$8' '$9' '${10}' '${11}' '${12}' '${13}' '${14}' '${15}' '${16}',' \
   ${STBT_CONFIG_FILE_CUSTOM}
   else
   sed -i -e 's,^'$1' =.*,'$1' = '$2' '$3' '$4' '$5' '$6',' \
   ${STBT_CONFIG_FILE_CUSTOM}
   fi
}

killtree() {
    local parent=$1 child
    for child in $(ps -o ppid= -o pid= | awk "\$1==$parent {print \$2}"); do
		#echo "$child"
        killtree $child
    done
    kill -9 $parent
}

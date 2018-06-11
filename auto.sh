#Creator of script: SirJosh3917
#Creator of anime-dl: Xonshiz
#May (5) 5th, 2018 - Updated June (6) 10th, 2018

#check if root
#https://askubuntu.com/questions/15853/how-can-a-script-check-if-its-being-run-as-root
is_root() {
	if ! [ $(id -u) = 0 ]; then
		echo "Please run this script as root."
		echo "Running \'sudo\' on this script..."

		SCRIPT_NAME=$(basename "$0")
		
		CMD="sudo ./${SCRIPT_NAME}"
		eval ${CMD}
		exit $?
	fi
}

#shamelessly stolen/modified from https://install.pi-hole.net
distro_check() {
	DISTRO_OS=""
	DISTRO_DEBIAN="debian"
	
	PKG_MANAGER=""
	PKG_INSTALL=""

	if command -v apt-get &> /dev/null; then
		DISTRO_OS=(${DISTRO_DEBIAN})
		PKG_MANAGER="apt-get"
		PKG_INSTALL="${PKG_MANAGER} --yes --no-install-recommends install"
#	elif command -v rpm &> /dev/null; then
#		if command -v dnf &> /dev/null; then
#			PKG_MANAGER="dnf"
#		elif
#			PKG_MANAGER="yum"
#		fi
	else
		echo "Your linux distro is not supporeted."
		exit
	fi

	if [ ${DISTRO_OS} == ${DISTRO_DEBIAN} ]; then
		return 0;
	else
		echo "Your linux distro either isn\'t supported, or somebody didn\'t finish coding the distro_check..."
		exit
	fi
	
	return 0;
}

get_distro() {
	DISTRO_DEBIAN_7=0
	DISTRO_DEBIAN_8=1
	DISTRO_DEBIAN_9=2
	RETURN=-1

	if [ ${DISTRO_OS} == ${DISTRO_DEBIAN} ]; then
		lsb_release -a > tmp_distro
		if grep "stretch" tmp_distro; then
			RETURN=${DISTRO_DEBIAN_9}
		elif grep "jessie" tmp_distro; then
                        RETURN=${DISTRO_DEBIAN_8}
                elif grep "wheezy" tmp_distro; then
                        RETURN=${DISTRO_DEBIAN_7}
		else
			echo "Version of debian not supported."
			RETURN=-1;
		fi
	fi

	rm tmp_distro
	return ${RETURN}
}

install_ffmpeg() {
	${PKG_INSTALL} ffmpeg
}

install_mkvmerge() {
	wget -q -O - https://mkvtoolnix.download/gpg-pub-moritzbunkus.txt | sudo apt-key add -

	get_distro
	DISTRO=$?
	
	if [ ${DISTRO} == ${DISTRO_DEBIAN_9} ]; then
		deb https://mkvtoolnix.download/debian/ stretch main
		deb-src https://mkvtoolnix.download/debian/ stretch main 
	elif [ ${DISTRO} == ${DISTRO_DEBIAN_8} ]; then
		deb https://mkvtoolnix.download/debian/ jessie main
		deb-src https://mkvtoolnix.download/debian/ jessie main 
	elif [ ${DISTRO} == ${DISTRO_DEBIAN_7} ]; then
                deb https://mkvtoolnix.download/debian/ wheezy main
                deb-src https://mkvtoolnix.download/debian/ wheezy main
        else echo "Distro unsupported."; return 1; fi

	apt update
	${PKG_INSTALL} mkvtoolnix
}

install_nodejs() {
	curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
	${PKG_INSTALL} nodejs
}

install_animedl() {
	wget https://github.com/Xonshiz/anime-dl/archive/master.tar.gz
	tar -xzf master.tar.gz
	mv anime-dl-master anime-dl #rename to anime-dl
	rm master.tar.gz
	
	SCRIPTS_DIR="anime-dl/anime_dl/"

	#make it runnable
	chmod -R +x ${SCRIPTS_DIR}
	chmod -R 755 ${SCRIPTS_DIR}
}

install_curl() {
	${PKG_INSTALL} curl
}

install_pip() {
	curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
	python get-pip.py
	rm get-pip.py
}

install_dependencies() {
	pip install cfscrape
	pip install tqdm
	pip install bs4
}

ensure_animedl_installed() {
	#find "Anime_DL downloads anime from" in the --help

	FIND="Anime_DL downloads anime from"
	SCRIPTS_DIR="anime-dl/anime_dl/"
	RETURN=1
	
	cd ${SCRIPTS_DIR}
	./__main__.py --help > ../../tmp_help
	cd ..; cd ..

	if grep "${FIND}" tmp_help; then
		echo "anime-dl installed!";
		RETURN=0
	else
		echo "anime-dl not installed...";
		RETURN=1
	fi

	rm tmp_help
	return ${RETURN}
}

#make sure we're root so we can install packages

is_root

distro_check

if [ $? == 0 ]; then
	install_ffmpeg
	install_mkvmerge
	install_nodejs
	install_curl
	install_pip
	install_dependencies
	install_animedl
	ensure_animedl_installed
	exit $?
else
	echo "no"
	exit
fi

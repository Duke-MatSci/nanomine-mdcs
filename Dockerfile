FROM centos:7.4.1708
run yum -y install epel-release
run yum -y update
run yum -y install git
run yum -y install python-pip
run yum -y install python-devel
run yum -y install libxml2-devel
run yum -y install libxslt-devel
workdir nanomine
add nanomine.tgz ./
run pip install -r /nanomine/docs/requirements.txt



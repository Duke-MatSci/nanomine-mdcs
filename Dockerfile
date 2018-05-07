FROM centos:7.4.1708
run yum -y install epel-release
run yum -y update
run yum -y groupinstall "Development Tools"
run yum -y install git
run yum -y install python-pip
run yum -y install python-devel
run yum -y install libxml2-devel
run yum -y install libxslt-devel
workdir nanomine
add nanomine.tgz ./ #do not do this for development
run pip install -r /nanomine/docs/requirements.txt
# need to:
#   expose vol for dev tree
#   handle db migrate vs server run
#   when running server, do not use --noreload
#   WIP -- not done yet



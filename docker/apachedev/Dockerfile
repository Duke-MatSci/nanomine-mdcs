FROM httpd:2.4
run apt-get update
#run apt-get install -y libapache2-mod-wsgi
run apt-get install -y vim
copy ./nanomine-httpd-vhosts.conf /usr/local/apache2/conf/extra/httpd-vhosts.conf
copy ./nanomine-httpd.conf /usr/local/apache2/conf/httpd.conf
#now, the key and crt can go into /usr/local/apache2/conf/certs
#which can be externalized via docker -v /PATH/mycertsdir:/usr/local/apache2/conf/certs




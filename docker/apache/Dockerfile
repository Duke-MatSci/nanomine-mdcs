FROM httpd:2.4
copy ./nanomine-httpd-ssl.conf /usr/local/apache2/conf/extra/httpd-ssl.conf
copy ./nanomine-httpd.conf /usr/local/apache2/conf/httpd.conf
#now, the key and crt can go into /usr/local/apache2/conf/certs
#which can be externalized via docker -v /PATH/mycertsdir:/usr/local/apache2/conf/certs




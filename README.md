OpenSuSE-RPI-Snort
==================

        OpenSuSE-RPI-Snort- Build Project for Snort 2.9.x with :
        SAM 0.8.x  
        daq 2.x 
        iptables 1.4.x  
        barnyard2 2.x  
        BASE 1.4.x 
        oinkmaster 2.x

Our Build are done on Rasberry PI opensuse .

Oss Snort RPi Build with  RPMS , SRPM , Tarballs & SPEC are stored
at Our dropbox url https://www.dropbox.com/sh/mxkqkagwc1qy9s1/sU3B0w8os-

Snort  rpm structure keept same way as the opensuSE Snort RPMs this makes it simple to update existing opensuse pkgs

Our build based mostly on http://download.opensuse.org/repositories/server:/monitoring SRPMS to keep i.e dependecies simple.


    Important NOTE : 
    Snort after 2.9.3 has no more DB suport into the snort-core - 
    As same as bevor 1999 you must use barnyard2 to bridge data to i.e Mysql .
    This HowTo descibe the usage & install : 
    http://gsxbinary.blogspot.de/2010/07/snort-barnyard2-mysql-base-intro.html


BUG reports please via mail to support@remsnet.de or raise an Issuie.

Changelog - 25.03.2014 - Horst dot venzke at remsnet dot de

    daq 2.02 spec : completed
    snort 2.9.0.5.specc : completed
    barnyard2-2.13git    : updated

depend software builds extras on RPI ARM oss 13.1

    iptables 1.4.21 : completed
    adodb5-518a     : completed
    base-1.4.5      : completed
    oinkmaster-2.0  : completed
    suse-sam        : completed


Extra system software required by BASE pkg:

    PEAR-Image_Canvas-0.3.5 : completed
    PEAR-Image_Color2-0.1.5 : completed
    PEAR-Image_Graph-0.8.0  : completed
 
 

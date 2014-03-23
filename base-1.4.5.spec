
# Remsnet  Spec file for package BASE ( for snort 2.9 build )
#
# Copyright (c) 1995-2008 Remsnet Netzwerk Service OhG , D-73630 Remshalden
# Copyright (c) 2008-2014 Remsnet Consullting & Internet Services LTD , D-40476 Duesseldorf


# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://github.com/remsnet/OpenSuSE-RPI-Snort
#

Name: base
Version: 1.4.5
Release: 1.2_rcis

Summary: BASE - Basic Analysis and Security Engine
License: GPLv2
Group: Networking/Other
Url: http://secureideas.sourceforge.net/
Source0: %name-%version.tar.gz
Source1: %{name}-nginx.conf
Source2: %{name}-apache2.conf
Source3: %{name}-base_sample_config.php

# dejavu-font patch from mandriva
Patch1: base-1.4.5-alt-font-path.patch

BuildArch: noarch

Requires: adodb5
Requires: php5-pear
Requires: php5-gd
Requires: pear-Image_Graph
Requires: pear-Image_Color2
Requires: pear-Image_Canvas
Requires: dejavu-fonts
Requires: pcre-tools libpcre1
BuildRequires: php5 coreutils


%description
BASE is the Basic Analysis and Security Engine.  It is based on the code
from the Analysis Console for Intrusion Databases (ACID) project.  This
application provides a web front-end to query and analyze the alerts
coming from a SNORT IDS system.

BASE is a web interface to perform analysis of intrusions that SNORT
has detected on your network.  It uses a user authentication and
role-based system, so that you as the security admin can decide
which and how much information each user can see.  It also has a
simple to use, web-based setup program for people who feel not
comfortable with editing files directly.

BASE is supported by a group of volunteers.  They are available to answer
any questions you may have or help you out in setting up your system.
They are also skilled in intrusion detection systems and make use of
that knowledge in the development of BASE. You can contact them
through the website http://secureideas.sourceforge.net/ or by
emailing them at base@secureideas.net

%prep
%setup



%build

%install
# At first, establish all the directories
test "%{buildroot}" != "/" && %__rm -rf %{buildroot}
#
%{__install} -d -m0755 %{buildroot}/%{_datadir}/%{name}/
%{__install} -d -m0755 %{buildroot}/%{_datadir}/%{name}/{admin,help,images,includes,languages,setup,sql,styles}/
%{__install} -d -m0755 %{buildroot}/%{_datadir}/%{name}/includes/templates/default
%{__install} -d -m0755 %{buildroot}/%{_datadir}/php5/PEAR/Image/Graph/Images/Maps
%{__install} -d -m0755 %{buildroot}/%{_sysconfdir}/apache2/conf.d/
%{__install} -d -m0755 %{buildroot}/%{_sysconfdir}/nginx/
%{__install} -d -m0755 %{buildroot}/%{_docdir}/%{name}
%{__install} -d -m0755 %{buildroot}/%{_docdir}/%{name}/contrib


# Install the sub directories INCLUDING the files inside
for i in `ls admin/*.php`
do
%{__install} -p -m0644 $i %{buildroot}/%{_datadir}/%{name}/$i
done

for i in `ls help/*.php`
do
%{__install} -p -m0644 $i %{buildroot}/%{_datadir}/%{name}/$i
done

for i in `ls images/*`
do
%{__install} -p -m0644 $i %{buildroot}/%{_datadir}/%{name}/$i
done

for i in `ls languages/*.php`
do
%{__install} -p -m0644 $i %{buildroot}/%{_datadir}/%{name}/$i
done

for i in `ls setup/*.php`
do
%{__install} -p -m0644 $i %{buildroot}/%{_datadir}/%{name}/$i
done

for i in `ls sql/*.sql`
do
%{__install} -p -m0644 $i %{buildroot}/%{_datadir}/%{name}/$i
done

for i in `ls styles/*.css`
do
%{__install} -p -m0644 $i %{buildroot}/%{_datadir}/%{name}/$i
done
for i in `ls includes/*.php`
do
%{__install} -p -m0644 $i %{buildroot}/%{_datadir}/%{name}/$i
done


# Install the files in the top level directory
for i in `ls *.php`
do
%{__install} -p -m0644 $i %{buildroot}/%{_datadir}/%{name}/$i
done


for i in `ls *.map`
do
%{__install} -p -m0644 $i %{buildroot}/%{_datadir}/%{name}/$i
done

for i in `ls base_conf.*`
do
%{__install} -p -m0644 $i %{buildroot}/%{_datadir}/%{name}/$i
done



# These two files have to go in a PEAR specific direction
for i in `ls  world_map6.*`
do
%{__install} -p -m0644 $i %{buildroot}/%{_datadir}/php5/PEAR/Image/Graph/Images/Maps/$i
done


# The docs go to a doc-specific location
# And this particular document HAS TO be enclosed by quotation marks
# because of the multibyte inside.

cd docs
for i in `find ./ -type f | grep -v pdf`
do
%{__install} -p -m0644 $i %{buildroot}%{_docdir}/%{name}/$i
done
cd ..


%{__cp} -rp docs/contrib %{buildroot}%{_docdir}/%{name}/

%{__install} -pm 644 %SOURCE1 %buildroot/%_sysconfdir/nginx/base.conf
%{__install} -pm 644 %SOURCE2 %buildroot/%_sysconfdir/apache2/conf.d/base.conf
%{__install} -pm 644 %SOURCE3 %buildroot/%_datadir/%name/base_conf.php.dist
%{__install} -pm 644 %SOURCE3 %buildroot/%_datadir/%name/base_conf.php



#---------------------------------------
%package nginx
Summary: BASE with configuration for nginx
Group: Networking/Other
BuildArch: noarch
Packager: Horst Venzke <horst.venzke@remsnet.de>
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php5
Requires: php5
Requires: nginx

%description nginx
BASE with nginx support.
Group: Applications/System
Requires: %{name}

%files nginx
%defattr(0644,root,root)
%config(noreplace) %_sysconfdir/nginx/%{name}.conf

#---------------------------------------

%package apache
Summary:  BASE with configuration for  apache2
Group: Networking/Other
BuildArch: noarch
Packager: Horst Venzke <horst.venzke@remsnet.de>
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php5
Requires: php5
Requires: %{name}

%description apache
apache config for  BASE - Basic Analysis and Security Engine

%files apache
%defattr(0644,root,root)
%config(noreplace) %{_sysconfdir}/apache2/conf.d/%{name}.conf

#---------------------------------------

%files
%dir %_datadir/%name
%dir %_datadir/%name/setup
%dir %_datadir/%name/styles
%dir %_datadir/%name/languages
%dir %_datadir/%name/includes
%dir %_datadir/%name/includes/templates
%dir %_datadir/%name/includes/templates/default
%dir %_datadir/%name/admin
%dir %_datadir/%name/images
%dir %_datadir/%name/help
%dir %_datadir/php5/PEAR/Image/Graph/Images/Maps/
%config(noreplace) %_datadir/%name/base_conf.php
%_datadir/%name/*.php
%_datadir/%name/base_conf.php.dist
%_datadir/%name/base_mac_prefixes.map
%_datadir/%name/setup/*.php
%_datadir/%name/styles/*.css
%_datadir/%name/includes/*.php
%_datadir/%name/admin/*.php
%_datadir/%name/languages/*php
%_datadir/%name/images/*.gif
%_datadir/%name/images/*.png
%_datadir/%name/help/*.php
%_datadir/php5/PEAR/Image/Graph/Images/Maps/world_map6.*



#---------------------------------------

%package doc
Summary:  BASE documentation
Group: Networking/Other
BuildArch: noarch
Packager: Horst Venzke <horst.venzke@remsnet.de>
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php5
Requires: man
Requires: %{name}

%description doc
 BASE - Basic Analysis and Security Engine

%files doc
%defattr(0644,root,root)
%_docdir/*

##---------------------------------------

%package sql
Summary:  BASE sql Setup
Group: Networking/Other
BuildArch: noarch
Packager: Horst Venzke <horst.venzke@remsnet.de>
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php5
Requires: php5
Requires: adodb5
Requires: libmysqlclient18
Requires: %{name}

%description sql
 BASE - Basic Analysis and Security Engine

%files sql
%defattr(0644,root,root)
%dir %{_datadir}/%{name}/sql
%{_datadir}/%{name}/sql/*.sql
%{_datadir}/%{name}/base_conf.php.dist


%post sql
echo " BASE sample setup for Mysql"
echo " sql files installed at /usr/share/base/sql"
echo " BASE base_config.php at /usr/share/base/"
echo " to setup BASE mysql DB  use i.e:"
echo " mysql -u root -p snort < /usr/share/base/sql/create_base_tbls_mysql.sql"



%post apache
echo ""
echo " you can now open snort BASE web gui at http://localhost/base"
echo " BASE for apache config file stored at /etc/apache2/conf.d/base.conf"
echo ""
echo " BASE Configuration SAMPLE for localhost stored at /usr/share/base/base_conf.php.dist"
echo ""

%post nginx
echo ""
echo " you can now open snort BASE web gui at http://localhost/base"
echo " BASE for nginx config file stored at /etc/nginx/base.conf"
echo "
echo " BASE Configuration SAMPLE for localhost stored at /usr/share/base/base_conf.php.dist"
echo ""


%postun
echo " cleanup yourself the BASE  webserver conf using rm on /etc/apache2/conf.d/base.conf or /etc/nginx/base.conf"
echo " and /usr/share/base "

%preun


%changelog
* Sun Mar 23 2014 support@remsnet.de
- build iptables for RPI on OSS 13.1
- updated pkg depenencies,  removed iptables-devel
- added /updated required options for snort 2.9.x Build
- added webserver config sub packlages for nginx , apache2 ,sql, doc

* Mon Feb 18 2013 Timur Aitov <timonbl4 at altlinux.org> 1.4.5-alt5
- add Requires for build graphs

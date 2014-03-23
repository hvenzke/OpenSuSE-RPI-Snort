#
# Remsnet  Spec file for package adodb5 ( for snort 2.9 build )
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

%define real_name adodb

Summary: Portable Database Library for PHP
Name: adodb5
%define real_version 481
Version: 518a
Release: 1.2_rcis
License: BSD or LGPL
Group: Development/Languages
URL: http://adodb.sourceforge.net/

Source: adodb518a.zip
Source1: adodb5-apache2.conf
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch: noarch
BuildRequires: php5 >= 5.1.0
Requires:  apache2
Requires:  php5 >= 5.1.0
Requires:  php5-mysql >= 5.1.0
Requires:  php5-odbc >= 5.1.0
Obsoletes: adodb <= 4.70
Provides: adodb php-adodb php5-adodb

%description
ADOdb stands for Active Data Objects Data Base. It currently support MySQL,
PostgreSQL, Interbase, Informix, Oracle, MS SQL 7, Foxpro, Access, ADO,
Sybase, DB2 and generic ODBC.

%prep

# precleaup required
test -d /usr/src/packages/BUILD/adodb5 && rm -rf  /usr/src/packages/BUILD/adodb5

%setup -q -n %{name}


%build

cp   %SOURCE1 .

%install
%{__rm} -rf %{buildroot}
%{__install} -d -m0755 %{buildroot}%{_datadir}/%{name}/{datadict,drivers,lang,perf,session,tests,xsl}/
%{__install} -p -m0644 *.php *.dtd %{buildroot}%{_datadir}/%{name}/
%{__install} -p -m0644 datadict/*.php %{buildroot}%{_datadir}/%{name}/datadict/
%{__install} -p -m0644 drivers/*.php %{buildroot}%{_datadir}/%{name}/drivers/
%{__install} -p -m0644 lang/*.php %{buildroot}%{_datadir}/%{name}/lang/
%{__install} -p -m0644 perf/*.php %{buildroot}%{_datadir}/%{name}/perf/
%{__install} -p -m0644 session/*.php %{buildroot}%{_datadir}/%{name}/session/
%{__install} -p -m0644 tests/*.php %{buildroot}%{_datadir}/%{name}/tests/
%{__install} -p -m0644 xsl/*.xsl %{buildroot}%{_datadir}/%{name}/xsl/
%{__mkdir_p} -m0755 %{buildroot}/%{_sysconfdir}/apache2/conf.d/
%{__install} -p -m0644 adodb5-apache2.conf %{buildroot}/%{_sysconfdir}/apache2/conf.d/adodb5.conf


%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/*


%defattr(0644, root, root)
%{_sysconfdir}/apache2/conf.d/adodb5.conf
%doc *.txt cute_icons_for_site/ docs/*.htm tests/

%changelog
* Fri Mar 21 2014 inital rebuild on oss 13.1 RPI
- rebuild on oss 13.1 RPI
- updated Requires and BuildRequires
- Updated to release 5.18a

* Mon May 08 2006 Dag Wieers <dag@wieers.com> - 4.81-1
- Updated to release 4.81.



# Remsnet  Spec file for package tmda
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

# Please submit bugfixes or comments  https://github.com/remsnet/DJB-Tools/tree/master


################################################################
# rpmbuild Package Options
# ========================
#       --with mysql
#               Builds a binary/package with support for MySQL.
#
#       --with postgresql
#               Builds a binary/package with support for PostgreSQL.
#
#       --with oracle
#               Builds a binary/package with support for Oracle.
#
# See pg 399 of _Red_Hat_RPM_Guide_ for rpmbuild --with and --without options.
################################################################

# Other useful bits
%define OracleHome /opt/oracle/OraHome1
%define SnortRulesDir %{_sysconfdir}/snort/rules
%define noShell /bin/false

# Default of no MySQL, but --with mysql will enable it
%define mysql 1
%{?_with_mysql:%define mysql 1}
# Default of no PostgreSQL, but --with postgresql will enable it
%define postgresql 0
%{?_with_postgresql:%define postgresql 1}

# Default of no Oracle, but --with oracle will enable it
%define oracle 0
%{?_with_oracle:%define oracle 1}

%define realname barnyard2


Summary: Snort Log Backend
Name: barnyard2
Version: 1.13
Release: 1.1
License: GPL-2.0
Group: System/Monitoring
Source0: http://www.securixlive.com/download/barnyard2/%{name}-2-%{version}.zip
Source2: %{name}.config
Source3: %{name}.init
Url: http://www.securixlive.com/barnyard2/
BuildRoot: %{_tmppath}/%{name}-%{version}-root

BuildRequires: libpcap-devel unzip libtool autoconf

%description
Barnyard has 3 modes of operation:
One-shot, continual, continual w/ checkpoint.  In one-shot mode,
barnyard will process the specified file and exit.  In continual mode,
barnyard will start with the specified file and continue to process
new data (and new spool files) as it appears.  Continual mode w/
checkpointing will also use a checkpoint file (or waldo file in the
snort world) to track where it is.  In the event the barnyard process
ends while a waldo file is in use, barnyard will resume processing at
the last entry as listed in the waldo file.


%package mysql
Summary: barnyard2 with MySQL support
Group: Applications/Internet
Requires: %{name} = %{epoch}:%{version}-%{release}
%if %{mysql}
Requires: mysql
BuildRequires: mysql-devel
%endif
%description mysql
barnyard2 binary compiled with mysql support.

%package postgresql
Summary: barnyard2 with PostgreSQL support
Group: Applications/Internet
Requires: %{name} = %{epoch}:%{version}-%{release}
%if %{postgresql}
Requires: postgresql
BuildRequires: postgresql-devel
%endif
%description postgresql
barnyard2 binary compiled with postgresql support.

%package oracle
Summary: barnyard2 with Oracle support
Group: Applications/Internet
Requires: %{name} = %{epoch}:%{version}-%{release}
%description oracle
barnyard2 binary compiled with Oracle support.

EXPERIMENTAL!!  I don't have a way to test this, so let me know if it works!
ORACLE_HOME=%{OracleHome}

%prep
%setup -q -n %{name}-2-%{version}


%build
./autogen.sh
%configure --sysconfdir=%{_sysconfdir}/snort  \
   %if %{postgresql}
        --with-postgresql \
   %endif
   %if %{oracle}
        --with-oracle \
   %endif
   %if %{mysql}
        --with-mysql-libraries=/usr/%{_lib} \
   %endif
make

%preun
%stop_on_removal

%postun
%restart_on_update
%insserv_cleanup

%post
%fillup_and_insserv

%install
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/snort/
make -i install DESTDIR=$RPM_BUILD_ROOT
%{__install} -d -p $RPM_BUILD_ROOT%{_sysconfdir}/{sysconfig,init.d,snort}
%{__install} -d -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/contrib
%{__install} -d -p $RPM_BUILD_ROOT%{_mandir}/man8
%{__install} -d -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/doc
%{__install} -d -p $RPM_BUILD_ROOT%{_sbindir}
%{__install} -m 644 etc/barnyard2.conf $RPM_BUILD_ROOT%{_sysconfdir}/snort/
%{__install} -D -m 0644 %{S:2} %{buildroot}%{_localstatedir}/adm/fillup-templates/sysconfig.%{name}
%{__install} -m 755 %{S:3} $RPM_BUILD_ROOT%{_sysconfdir}/init.d/barnyard2
%__ln_s ../../etc/init.d/%{name} "%{buildroot}/usr/sbin/rc%{name}"
rm doc/Makefile* doc/INSTALL

%clean
if [ -d $RPM_BUILD_ROOT ] && [ "$RPM_BUILD_ROOT" != "/"  ] ; then
        rm -rf $RPM_BUILD_ROOT
fi

%files
%defattr(-,root,root)
%doc LICENSE doc/* schemas/create_*
%attr(755,root,root) %{_bindir}/barnyard2
%attr(755,root,root) %{_sbindir}/rcbarnyard2
%attr(755,root,root) %config %{_sysconfdir}/snort
%attr(640,root,root) %config %{_sysconfdir}/snort/barnyard2.conf
%attr(755,root,root) %{_initrddir}/barnyard2
%attr(644,root,root) /var/adm/fillup-templates/sysconfig.%{name}

%changelog
* Sat Mar 22 2014 support@remsnet.de
- rebuild & on Opensuse 13.1 RPI arm
- updated BUILD based on https://github.com/remsnet/DJB-Tools

* Wed Feb  8 2012 stoppe@gmx.de
- Initial release

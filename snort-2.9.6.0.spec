# Remsnet  Spec file for package snort  ( for snort 2.9 build )
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
# norootforbuild

%define SnortRulesDir %{_sysconfdir}/snort/rules
%define mysql 1
%define postgresql 1
# odbc support removed cause it doesn't find the libs on x86_64
%define unixODBC 0
# --enable-targetbased conflicts with --enable-ipv6
# --enable-inline needs libnet 1.0.x
# --enable-react needs libnet 1.0.2a
%define SNORT_BASE_CONFIG --disable-static --enable-maintainer-mode --enable-pthread --enable-prelude --enable-sourcefire \
--enable-stream4udp --enable-memory-cleanup --enable-decoder-preprocessor-rules --enable-targetbased --enable-dynamicplugin \
--enable-timestats --enable-ruleperf --enable-ppm --enable-perfprofiling --enable-linux-smp-stats --enable-ipfw \
--enable-inline-init-failopen --enable-flexresp2 --enable-aruba --enable-gre --enable-mpls --enable-inline \
--enable-react --enable-ipv6 --enable-zlib


Name:           snort
Version:        2.9.6.0
Release:        0
License:        GPLv2
Group:          Productivity/Networking/Security
URL:            http://www.snort.org/
Source:         %{name}-%{version}.tar.gz
Source1:            snort.init.d
Source2:        snort.logrotate
Source3:        snort-rpmlintrc
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  autoconf
BuildRequires:  bison
BuildRequires:  findutils
%if 0%{?suse_version} > 1020
BuildRequires:  fdupes
%endif
BuildRequires:  flex
Requires:       iptables >= 1.4.21
Requires:       libdnet >= 1.12
Requires:       libipq0 >= 1.4.20
Requires:       libiptc0 >= 1.4.20
Requires:       libxtables10 >= 1.4.20
Requires:       xtables-plugins >= 1.4.20
Requires:       libpcap >= 1.3.0
Requires:       libnetfilter_conntrack3 >= 1.0.4
Requires:       libnetfilter_queue1 >= 1.0.2
BuildRequires:  libgnutls-devel
BuildRequires:  libmysqlclient-devel
BuildRequires:  libnet1  >= 1.1.6
BuildRequires:  libpcap-devel  >= 1.3.0
BuildRequires:  libprelude-devel
BuildRequires:  pcre-devel
BuildRequires:  pkg-config
BuildRequires:  postgresql-devel
BuildRequires:  zlib-devel
#to solve conflict raised by libpcap-mmap
BuildRequires:  libpcap-devel >= 1.3.0
BuildRequires:  libdaq-devel >= 2.0.2
BuildRequires:  libnetfilter_queue-devel  >= 1.0.2
PreReq:         glibc pwdutils update-alternatives %insserv_prereq %fillup_prereq
Requires:       logrotate
Summary:        Network intrusion prevention and detection system

%package devel
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}
Summary:        Development files for Snort

%package mysql
Summary:        Snort with MySQL support
Group:          Productivity/Networking/Security
Requires:       %{name} = %{version}-%{release}
PreReq:         update-alternatives
%if %{mysql}
BuildRequires:  libmysqlclient-devel
%endif

%package postgresql
Summary:        Snort with PostgreSQL support
Group:          Productivity/Networking/Security
Requires:       %{name} = %{version}-%{release}
PreReq:         update-alternatives
%if %{postgresql}
BuildRequires:  postgresql-devel
%endif

%package unixODBC
Summary:        Snort with unixODBC support
Group:          Productivity/Networking/Security
Requires:       %{name} = %{version}-%{release}
PreReq:         update-alternatives
%if %{unixODBC}
BuildRequires:  unixODBC-devel
%endif

%description
SNORT® is an open source network intrusion prevention and detection system utilizing a rule-driven language, which combines the benefits of signature, protocol and anomaly based inspection methods. With millions of downloads to date, Snort is the most widely deployed intrusion detection and prevention technology worldwide and has become the de facto standard for the industry.

%description devel
This package contains the development files (mainly C header files) for Snort

%description mysql
Snort binary compiled with MySQL support.

%description postgresql
Snort binary compiled with PostgreSQL support.

%description unixODBC
Snort binary compiled with unixODBC support.


%prep
%setup -q

%build
autoreconf -fi
SNORT_BASE_CONFIG="%{expand:%{SNORT_BASE_CONFIG}}"
%ifarch x86_64
SNORT_BASE_CONFIG="$SNORT_BASE_CONFIG --enable-64bit-gcc"
%endif
BuildSnort() {
        %__mkdir "$1"
        cd "$1"
        %__ln_s ../configure ./configure

        if [ "$1" = "plain" ] ; then
                SNORT_BASE_CONFIG="$SNORT_BASE_CONFIG --without-mysql --without-postgresql --without-oracle --without-odbc"
        fi
        if [ "$1" = "mysql" ]; then
                SNORT_BASE_CONFIG="$SNORT_BASE_CONFIG --with-mysql --with-mysql-libraries=%{_libdir} --without-postgresql --without-oracle --without-odbc"
        fi
        if [ "$1" = "postgresql" ]; then
                SNORT_BASE_CONFIG="$SNORT_BASE_CONFIG --without-mysql --with-postgresql --without-oracle --without-odbc"
        fi
        if [ "$1" = "unixODBC" ]; then
                SNORT_BASE_CONFIG="$SNORT_BASE_CONFIG --without-mysql --without-postgresql --without-oracle --with-odbc"
        fi
        %configure $SNORT_BASE_CONFIG
        # parallel compilation fails
        %__make
        %__mv src/snort ../%{name}-"$1"
        cd ..
}

# Always build snort-plain
BuildSnort plain
# Maybe build the others
%if %{mysql}
  BuildSnort mysql
%endif
%if %{postgresql}
  BuildSnort postgresql
%endif
%if %{unixODBC}
  BuildSnort unixODBC
%endif

%check
CheckSnort() {
        cd "$1"
        %__make check
        cd ..
}
CheckSnort plain
# Maybe check the others
%if %{mysql}
  CheckSnort mysql
%endif
%if %{postgresql}
  CheckSnort postgresql
%endif
%if %{unixODBC}
  CheckSnort unixODBC
%endif

%install
InstallSnort() {
        if [ "$1" = "mysql" ]; then
                %__install -p -m 0755 %{name}-mysql %{buildroot}%{_sbindir}/%{name}-mysql
        fi

        if [ "$1" = "postgresql" ]; then
                %__install -p -m 0755 %{name}-postgresql %{buildroot}%{_sbindir}/%{name}-postgresql
        fi

        if [ "$1" = "unixODBC" ]; then
                %__install -p -m 0755 %{name}-unixODBC %{buildroot}%{_sbindir}/%{name}-unixODBC
        fi

        if [ "$1" = "plain" ]; then
                cd "$1"
                %makeinstall
                cd ..
                find %{buildroot} -name "*.la" -exec %__rm -f {} \;
                %__install -D -p -m 0755 %{name}-plain %{buildroot}%{_sbindir}/%{name}-plain
                %__rm %{buildroot}%{_bindir}/%{name}
                %__mkdir_p %{buildroot}%{_docdir}
                %__mv %{buildroot}%{_datadir}/doc/snort %{buildroot}%{_docdir}
                %__mkdir_p %{buildroot}%{_includedir}/snort
                %__mv %{buildroot}/usr/src/snort_dynamicsrc/ %{buildroot}%{_includedir}/snort
                %__mkdir_p %{buildroot}%{_libdir}/snort
                %__mv %{buildroot}/usr/lib/snort_dynamic* %{buildroot}%{_libdir}/snort
                %__rm %{buildroot}%{_docdir}/snort/README.WIN32
                %__mkdir_p -m 0755 %{buildroot}%{SnortRulesDir}
                %__mkdir_p -m 0755 %{buildroot}%{_var}/log/snort
                %__install -D -p -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/snortd
                %__ln_s %{_initrddir}/snortd %{buildroot}%{_sbindir}/rcsnortd
                %__install -D -p -m 0644 rpm/snort.sysconfig %{buildroot}%{_var}/adm/fillup-templates/sysconfig.snort
                %__install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/snort

                # missing schema
                %__mkdir_p %{buildroot}%{_docdir}/snort/schemas
                #%__install -D -p -m 0644 schemas/create_* %{buildroot}%{_docdir}/snort/schemas

                #fix paths in snort.conf
                %__sed -i -e 's;var RULE_PATH ../rules;var RULE_PATH %{SnortRulesDir};' etc/snort.conf
                %__sed -i -e 's;\/usr\/local\/lib;%{_libdir}\/snort;' etc/snort.conf

                %__install -p -m 0644 etc/reference.config etc/classification.config etc/unicode.map etc/gen-msg.map etc/threshold.conf etc/snort.conf %{buildroot}%{_sysconfdir}/snort
        fi
}
# Always install snort-plain
InstallSnort plain
# Maybe install the others
%if %{mysql}
        InstallSnort mysql
%endif
%if %{postgresql}
        InstallSnort postgresql
%endif
%if %{unixODBC}
        InstallSnort unixODBC
%endif

touch %{buildroot}%{_sbindir}/snort
chmod 0755 %{buildroot}%{_sbindir}/snort

# make rpmlint happy
%if 0%{?suse_version} > 1020
%fdupes %{buildroot}%{_includedir}/snort
%endif

%pre
# Don't do all this stuff if we are upgrading
if [ $1 = 1 ] ; then
        /usr/sbin/groupadd snort 2> /dev/null || true
        /usr/sbin/useradd -r -d %{_var}/log/snort -s /bin/false -c "Snort" -g snort snort 2>/dev/null || true
fi

%post
/sbin/ldconfig
%{_sbindir}/update-alternatives --install %{_sbindir}/snort snort %{_sbindir}/%{name}-plain 10
#fillup_and_insserv snortd
%fillup_only

%post mysql
%{_sbindir}/update-alternatives --install %{_sbindir}/snort snort %{_sbindir}/%{name}-mysql 11

%post postgresql
%{_sbindir}/update-alternatives --install %{_sbindir}/snort snort %{_sbindir}/%{name}-postgresql 11

%post unixODBC
%{_sbindir}/update-alternatives --install %{_sbindir}/snort snort %{_sbindir}/%{name}-unixODBC 11

%preun
%stop_on_removal snortd
if [ "$1" = 0 ] ; then
        %{_sbindir}/update-alternatives --remove snort %{_sbindir}/%{name}-plain
fi

%preun mysql
if [ "$1" = 0 ] ; then
        %{_sbindir}/update-alternatives --remove snort %{_sbindir}/%{name}-mysql
fi

%preun postgresql
if [ "$1" = 0 ] ; then
        %{_sbindir}/update-alternatives --remove snort %{_sbindir}/%{name}-postgresql
fi

%preun unixODBC
if [ "$1" = 0 ] ; then
        %{_sbindir}/update-alternatives --remove snort %{_sbindir}/%{name}-unixODBC
fi

%postun
/sbin/ldconfig
%restart_on_update snortd
%insserv_cleanup

%clean
test "%{buildroot}" != "/" && %__rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc %{_docdir}/snort
%ghost %{_sbindir}/snort
%{_sbindir}/rcsnortd
%{_sbindir}/snort-plain
%{_bindir}/u2boat
%{_bindir}/u2spewfoo
%config(noreplace) %{_initrddir}/snortd
%config(noreplace) %{_sysconfdir}/logrotate.d/snort
%config(noreplace) %{_sysconfdir}/snort
%{_var}/adm/fillup-templates/sysconfig.snort
%{_libdir}/snort
%{_mandir}/man8/snort.8*
%attr(0700,snort,snort) %dir %{_var}/log/snort

%files devel
%defattr(-,root,root)
%{_includedir}/snort
%{_libdir}/pkgconfig/snort.pc
%{_libdir}/pkgconfig/snort_preproc.pc
%{_libdir}/pkgconfig/snort_output.pc

%if %{mysql}
%files mysql
%defattr(-,root,root)
%ghost %{_sbindir}/snort
%attr(0755,root,root) %{_sbindir}/%{name}-mysql
%endif

%if %{postgresql}
%files postgresql
%defattr(-,root,root)
%ghost %{_sbindir}/snort
%attr(0755,root,root) %{_sbindir}/%{name}-postgresql
%endif

%if %{unixODBC}
%files unixODBC
%defattr(-,root,root)
%ghost %{_sbindir}/snort
%attr(0755,root,root) %{_sbindir}/%{name}-unixODBC
%endif

%changelog
* Fri Mar 21 2014 inital rebuild on oss 13.1 RPI
- rebuild on oss 13.1 RPI
- updated Requires and BuildRequires

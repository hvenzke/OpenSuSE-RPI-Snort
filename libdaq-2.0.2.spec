#
# Remsnet  Spec file for package libdaq-2.0  ( for snort 2.9 build )
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


%define soname 1

Name:           libdaq
Version:        2.0.2
Release:        1.0rcis
Url:            http://www.snort.org/snort-downloads
Source:         daq-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  iptables >= 1.4.20
BuildRequires:  libiptc-devel >= 1.4.20
BuildRequires:  libxtables-devel >= 1.4.20
BuildRequires:  libdnet-devel >= 1.12
BuildRequires:  libpcap-devel >= 1.3.0
BuildRequires:  pkg-config pkgconfig
%if 0%{?suse_version} > 1210
BuildRequires:  libipq-devel >= 1.4.21
BuildRequires:  libnetfilter_queue-devel >= 1.0.2
%endif
Requires:       libdnet >= 1.12
Requires:       libipq0 >= 1.4.20
Requires:       libiptc0 >= 1.4.20
Requires:       libxtables10 >= 1.4.20
Requires:       xtables-plugins >= 1.4.20
Requires:       libpcap >= 1.3.0
Requires:       libnetfilter_conntrack3 >= 1.0.4
Requires:       libnetfilter_queue1 >= 1.0.2

Summary:        Data Acquisition library, for packet I/O
License:        GPL-2.0
Group:          Productivity/Networking/System

%description
Data Acquisition library, for packet I/O.  The
DAQ replaces direct calls to PCAP functions with an abstraction layer that
facilitates operation on a variety of hardware and software interfaces without
requiring changes to Snort.  It is possible to select the DAQ type and mode
when invoking Snort to perform PCAP readback or inline operation, etc.  The
DAQ library may be useful for other packet processing applications and the
modular nature allows you to build new modules for other platforms.

%package -n %{name}%{soname}
Summary:        Data Acquisition library, for packet I/O
Group:          System/Libraries

%description -n %{name}%{soname}
Data Acquisition library, for packet I/O.  The
DAQ replaces direct calls to PCAP functions with an abstraction layer that
facilitates operation on a variety of hardware and software interfaces without
requiring changes to Snort.  It is possible to select the DAQ type and mode
when invoking Snort to perform PCAP readback or inline operation, etc.  The
DAQ library may be useful for other packet processing applications and the
modular nature allows you to build new modules for other platforms.

%package devel
Requires:       %{name}%{soname} = %{version}
Requires:       daq-modules = %{version}

%if 0%{?suse_version} > 1120
Requires:  libiptc-devel >= 1.4.20
Requires:  libxtables-devel >= 1.4.20
Requires:  libdnet-devel >= 1.12
Requires:  libpcap-devel >= 1.0.0
Requires:  libnetfilter_queue-devel >= 1.0.2
%endif

Summary:        Data Acquisition library, for packet I/O
Group:          Development/Libraries/C and C++

%description devel
Data Acquisition library, for packet I/O.  The
DAQ replaces direct calls to PCAP functions with an abstraction layer that
facilitates operation on a variety of hardware and software interfaces without
requiring changes to Snort.  It is possible to select the DAQ type and mode
when invoking Snort to perform PCAP readback or inline operation, etc.  The
DAQ library may be useful for other packet processing applications and the
modular nature allows you to build new modules for other platforms.

%package -n daq-modules
Summary:        Bundled DAQ modules
Group:          System/Libraries

%description -n daq-modules
Contains the DAQ modules that come bundled with the base LibDAQ distribution.



%prep
%setup -qn daq-%{version}

%build
export CPPFLAGS="$CPPFLAGS $(pkg-config --libs --cflags libipq) $(pkg-config --libs --cflags libnetfilter_queue)"
%configure --disable-static
make %{?_smp_mflags}

%install
%makeinstall
find %{buildroot} -name "*.la" -delete

%post -n %{name}%{soname} -p /sbin/ldconfig

%postun -n %{name}%{soname} -p /sbin/ldconfig

%clean
test "%{buildroot}" != "/" && %__rm -rf "%{buildroot}"

%files -n %{name}%{soname}
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_bindir}/daq-modules-config
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a

%files -n daq-modules
%defattr(-,root,root)
%{_libdir}/daq

%changelog
* Sat Mar 2 2014  support@remsnet.de
- snort 2.9.0.5 Build on RPI . see https://github.com/remsnet/OpenSuSE-RPI-Snort
- updated dependencyes

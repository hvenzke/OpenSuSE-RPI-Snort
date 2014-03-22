
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


Name:           iptables
%define lname_ipq       libipq0
%define lname_iptc      libiptc0
%define lname_xt        libxtables10
Version:        1.4.21
Release:        1.1rcis
Summary:        IP Packet Filter Administration utilities
License:        GPL-2.0 and Artistic-2.0
Group:          Productivity/Networking/Security
Url:            http://netfilter.org/projects/iptables/

#Freecode-URL:  http://freecode.com/projects/iptables/
#Git-Web:       http://git.netfilter.org/
#Git-Clone:     git://git.netfilter.org/iptables
#DL-URL:        http://netfilter.org/projects/iptables/files/
Source:         http://netfilter.org/projects/iptables/files/%name-%version.tar.bz2
Source2:        http://netfilter.org/projects/iptables/files/%name-%version.tar.bz2.sig
Source3:        %name.keyring
Patch3:         iptables-batch.patch
Patch4:         iptables-apply-mktemp-fix.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  sgmltool
BuildRequires:  libtool
BuildRequires:  pkg-config >= 0.21
BuildRequires:  fdupes
BuildRequires:  gpg-offline
BuildRequires:  libnetfilter_conntrack3
BuildRequires:  libnfnetlink0
BuildRequires:  libnetfilter_conntrack-devel
BuildRequires:  libnfnetlink-devel
Requires:       xtables-plugins = %version

%description
iptables is used to set up, maintain, and inspect the tables of IP
packet filter rules in the Linux kernel. This version requires kernel
3.0 or newer.

%package -n xtables-plugins
Summary:        Match and Target Extension plugins for iptables
Group:          Productivity/Networking/Security
Conflicts:      iptables < 1.4.18

%description -n xtables-plugins
Match and Target Extension plugins for iptables.

%package -n %lname_ipq
Summary:        Library to interface with the (old) ip_queue kernel mechanism
Group:          System/Libraries

%description -n %lname_ipq
The Netfilter project provides a mechanism (ip_queue) for passing
packets out of the stack for queueing to userspace, then receiving
these packets back into the kernel with a verdict specifying what to
do with the packets (such as ACCEPT or DROP). These packets may also
be modified in userspace prior to reinjection back into the kernel.

ip_queue/libipq is obsoleted by nf_queue/libnetfilter_queue!

%package -n libipq-devel
Summary:        Development files for the ip_queue kernel mechanism
Group:          Development/Libraries/C and C++
Requires:       %lname_ipq = %version

%description -n libipq-devel
The Netfilter project provides a mechanism (ip_queue) for passing
packets out of the stack for queueing to userspace, then receiving
these packets back into the kernel with a verdict specifying what to
do with the packets (such as ACCEPT or DROP). These packets may also
be modified in userspace prior to reinjection back into the kernel.

ip_queue/libipq is obsoleted by nf_queue/libnetfilter_queue!

%package -n %lname_iptc
Summary:        Library for low-level ruleset generation and parsing
Group:          System/Libraries

%description -n %lname_iptc
libiptc ("iptables cache") is used to retrieve from the kernel, parse,
construct, and load new rulesets into the kernel.

%package -n libiptc-devel
Summary:        Development files for libiptc, a packet filter ruleset library
Group:          Development/Libraries/C and C++
Requires:       %lname_iptc = %version

%description -n libiptc-devel
libiptc ("iptables cache") is used to retrieve from the kernel, parse,
construct, and load new rulesets into the kernel.

%package -n %lname_xt
Summary:        iptables extension interface
Group:          System/Libraries

%description -n %lname_xt
This library contains all the iptables code shared between iptables,
ip6tables, their extensions, and for external integration for e.g.
iproute2's m_xt.

%package -n libxtables-devel
Summary:        Libraries, Headers and Development Man Pages for iptables
Group:          Development/Libraries/C and C++
Requires:       %lname_xt = %version

%description -n libxtables-devel
This library contains all the iptables code shared between iptables,
ip6tables, their extensions, and for external integration for e.g.

Link your extension (iptables plugins) with $(pkg-config xtables
--libs) and place the plugin in the directory given by $(pkg-config
xtables --variable=xtlibdir).

%prep
%{?gpg_verify: %gpg_verify %{S:2}}
%setup -q
%patch -P 3 -P 4 -p1

%build
# We have the iptables-batch patch, so always regenerate.
if true || [ ! -e configure ]; then
        ./autogen.sh;
fi
# bnc#561793 - do not include unclean module in iptables manpage
rm -f extensions/libipt_unclean.man
# includedir is overriden on purpose to detect projects that
# fail to include libxtables_CFLAGS
%configure --includedir="%_includedir/pkg/%name" --enable-libipq
make %{?_smp_mflags}

%install
make DESTDIR=%buildroot install
# iptables-apply is not installed by upstream Makefile
install -m0755 iptables/iptables-apply %buildroot%_sbindir/
install -m0644 iptables/iptables-apply.8 %buildroot%_mandir/man8/
rm -f "%buildroot/%_libdir"/*.la;
%if 0%{?suse_version}
%fdupes %buildroot/%_prefix
%endif

%post   -n %lname_ipq -p /sbin/ldconfig
%postun -n %lname_ipq -p /sbin/ldconfig
%post   -n %lname_iptc -p /sbin/ldconfig
%postun -n %lname_iptc -p /sbin/ldconfig
%post   -n %lname_xt -p /sbin/ldconfig
%postun -n %lname_xt -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc COPYING
%doc %_mandir/man1/ip*
%doc %_mandir/man8/ip*
%_bindir/iptables-xml
%_sbindir/iptables
%_sbindir/iptables-apply
%_sbindir/iptables-batch
%_sbindir/iptables-restore
%_sbindir/iptables-save
%_sbindir/ip6tables
%_sbindir/ip6tables-batch
%_sbindir/ip6tables-restore
%_sbindir/ip6tables-save
%_sbindir/xtables-multi

%files -n xtables-plugins
%defattr(-,root,root)
%_libdir/xtables/
%_sbindir/nfnl_osf
%_datadir/xtables/

%files -n %lname_ipq
%defattr(-,root,root)
%_libdir/libipq.so.0*

%files -n libipq-devel
%defattr(-,root,root)
%doc %_mandir/man3/libipq*
%doc %_mandir/man3/ipq*
%dir %_includedir/pkg/%name/
%_includedir/pkg/%name/libipq*
%_libdir/libipq.so
%_libdir/pkgconfig/libipq.pc

%files -n %lname_iptc
%defattr(-,root,root)
%_libdir/libiptc.so.0*
%_libdir/libip4tc.so.0*
%_libdir/libip6tc.so.0*

%files -n libiptc-devel
%defattr(-,root,root)
%dir %_includedir/pkg/
%dir %_includedir/pkg/%name/
%_includedir/pkg/%name/libiptc*
%_libdir/libip*tc.so
%_libdir/pkgconfig/libip*tc.pc

%files -n %lname_xt
%defattr(-,root,root)
%_libdir/libxtables.so.10*

%files -n libxtables-devel
%defattr(-,root,root)
%dir %_includedir/pkg/
%dir %_includedir/pkg/%name/
%_includedir/pkg/%name/xtables.h
%_includedir/pkg/%name/xtables-version.h
%_libdir/libxtables.so
%_libdir/pkgconfig/xtables.pc

%changelog
* Sat Mar 22 2014 support@remsnet.de
- cleanup changelog due move of < 1.4.20
- build iptables for RPI on OSS 13.1
- updated pkg depenencies,  removed iptables-devel
- added /updated required options for snort 2.9.x Build ( libiptc, libxtables, ...)

* Sat Nov 23 2013 jengelh@inai.de
- Update to new upstream release 1.4.21
  * --nowildcard option for xt_socket, available since Linux kernel 3.11
  * SYNPROXY support, available since Linux kernel 3.12

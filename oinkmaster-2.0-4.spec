

# Remsnet  Spec file for package oinkmaster ( for snort 2.9 build )
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


Summary: Tool for updating Snort rulesets
Name: oinkmaster
Version: 2.0
Release: 1.4_rcis
License: BSD
Group: Applications/Internet
URL: http://oinkmaster.sourceforge.net/
Packager: Horst Venzke <horst.venzke@remsnet.de>
Source: http://oinkmaster.sourceforge.net/oinkmaster/oinkmaster-%{version}.tar.gz
Source1:  %{name}-conf
Source2:  %{name}-rsyncd-cron-daily
Source3:  %{name}-rsync.secrets
Source4:  %{name}-rsyncd.conf
Source5:  %{name}-xinetd
Source6:  %{name}-logrotate
Source7:  %{name}-rsync.sh
Source8:  %{name}-rsync-cron-daily

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: perl >= 5.8
BuildRequires: perl >= 5.8
Requires: perl >= 5.8
Requires: snort

%description
Oinkmaster is simple but useful Perl script released under the BSD license
to help you update/manage your Snort rules and disable/enable/modify
certain rules after each update (among other things). It will tell you
exactly what had changed since the last update, so you'll have total
control of your rules.

Oinkmaster can be used to update to the latest official rules from
www.snort.org, but can just as well be used for managing your homemade
rules and distribute them between sensors. It may be useful in conjunction
with any program that can use Snort rules, like Snort (doh!) or
Prelude-NIDS. It will run on most UNIX systems and also on Windows.

%prep
%setup

%install
%{__rm} -rf %{buildroot}
%{__install} -d -m0755 %{buildroot}%{_bindir}
%{__install} -d -p $RPM_BUILD_ROOT%{_sysconfdir}/{sysconfig,snort,cron.hourly,cron.daily,logrotate.d}
%{__install} -d -m0755 %{buildroot}/usr/share/doc/packages/oinkmaster

# binarys
%{__install} -m0755 contrib/addmsg.pl %{buildroot}%{_bindir}
%{__install} -m0755 contrib/addsid.pl %{buildroot}%{_bindir}
%{__install} -m0755 contrib/create-sidmap.pl %{buildroot}%{_bindir}
%{__install} -m0755 contrib/makesidex.pl %{buildroot}%{_bindir}
%{__install} -m0755 oinkmaster.pl %{buildroot}%{_bindir}

%{__install} -D -m0644 oinkmaster.1 %{buildroot}%{_mandir}/man1/oinkmaster.1

# config
%{__install} -d -m0755 %{buildroot}%{_sysconfdir}
%{__install} -m0644 %{S:1} %{buildroot}%{_sysconfdir}/snort/oinkmaster.conf

# update cronjob
%{__install} -m0644 %{S:2} %{buildroot}%{_sysconfdir}/cron.daily/oinkmaster_update

# rsyncd setup
%{__install} -m0400 %{S:3} %{buildroot}/usr/share/doc/packages/oinkmaster/oinkmaster-rsyncd.secrets
%{__install} -m0644 %{S:4} %{buildroot}/usr/share/doc/packages/oinkmaster/oinkmaster-rsyncd.conf
%{__install} -m0644 %{S:5} %{buildroot}/usr/share/doc/packages/oinkmaster/oinkmaster-xinetd
%{__install} -m0644 %{S:6} %{buildroot}/usr/share/doc/packages/oinkmaster/oinkmaster-rsync.conf
%{__install} -d -m0755 %{buildroot}/var/lib/snort/rules.master
%{__install} -d -m0755 %{buildroot}/var/lib/snort/rules.tmp
%{__install} -d -m0755 %{buildroot}/var/lib/snort/rules.backup
%{__install} -m0644 %{S:5} %{buildroot}%{_sysconfdir}/logrotate.d/oinkmaster-rsyncd

# oinkmaster rsync client
%{__install} -m0755 %{S:5} %{buildroot}%{_sysconfdir}/cron.daily/oinkmaster-rsync
%{__install} -m0755 %{S:5} %{buildroot}%{_bindir}/oinkmaster-rsync.sh


%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc ChangeLog LICENSE README* template-examples.conf UPGRADING oinkmaster.conf
%doc %{_mandir}/man?/*
%config(noreplace) %{_sysconfdir}/snort/oinkmaster.conf
%{_bindir}/*
%dir /var/lib/snort/rules.master
%dir /var/lib/snort/rules.tmp


#------------------------------------------------------
%package cron
Summary:  oinkmaster cronjob
Group: Networking/Other
BuildArch: noarch
Packager: Horst Venzke <horst.venzke@remsnet.de>
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: perl
Requires: coreutils perl
Requires: %{name}

%description cron
 oinkmaster snort.org  RULES update daily cronjob

%files cron
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/cron.daily/oinkmaster_update
/var/lib/snort/rules.tmp

#------------------------------------------------------
%package rsyncd
Summary: oinkmaster rsyncd server
Group: Networking/Other
BuildArch: noarch
Packager: Horst Venzke <horst.venzke@remsnet.de>
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: perl
Requires: rsync xinetd perl coreutils
Requires: %{name}

%description rsyncd
        oinkmaster rsync server
        provide updated snort rules for local network via rsync


%files rsyncd
%defattr(-,root,root)
/usr/share/doc/packages/oinkmaster/oinkmaster-rsyncd.secrets
/usr/share/doc/packages/oinkmaster/oinkmaster-rsyncd.conf
/usr/share/doc/packages/oinkmaster/oinkmaster-xinetd
/usr/share/doc/packages/oinkmaster/oinkmaster-rsync.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/oinkmaster-rsyncd
/var/lib/snort/rules.master


##------------------------------------------------------
%package rsync
Summary: oinkmaster rsync client
Group: Networking/Other
BuildArch: noarch
Packager: Horst Venzke <horst.venzke@remsnet.de>
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: perl
Requires: rsync xinetd perl coreutils
Requires: %{name}

%description rsync
        oinkmaster rsync client
        provide updated snort rules for local network via rsync


%files rsync
%defattr(-,root,root)
%attr(755,root,root)
/var/lib/snort/rules.backup
%{_sysconfdir}/cron.daily/oinkmaster-rsync
%{_bindir}/oinkmaster-rsync.sh






%post cron
echo " setup oinkmaster cron update "

%post rsync
echo " setup oinkmaster rsyncd "
test -x /etc/xinetd.d/rsync || cp /usr/share/doc/packages/oinkmaster/rsync /etc/xinetd.d/rsync; chmod 755 /etc/xinetd.d/rsync
test
test -x /etc/xinetd.d/rsync &&  chkconfig rsync xinetd
test -f /etc//snort/oinkmaster-rsyncd.secrets || cp /usr/share/doc/packages/oinkmaster/oinkmaster-rsyncd.secrets /etc//snort/oinkmaster-rsyncd.secrets ; chown snort:snort /etc//snort/oinkmaster-rsyncd.secrets
test -x /etc/xinetd.d/rsync &&  rcxinetd restart

%changelog

* Mon Mar 24 2014 support@remsnet.de
- added cron update script
- added oinkmaster rsync server
- added sample oinkmasterc.conf for snort 2.9.x Build
- added /var/lib/snort/rules.master/, /var/lib/snort/rules.tmp for network rule managment base
- added rsync script + cron samples

* Sun Mar 23 2014 support@remsnet.de
- build iptables for RPI on OSS 13.1
- updated pkg depenencies,  removed iptables-devel
- added /updated required options for snort 2.9.x Build


* Sat Feb 18 2006 Harry Hoffman <hhoffman@ip-solutions.net> - 2.0-0
- Initial Packaging of 2.0.

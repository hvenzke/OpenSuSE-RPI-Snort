
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
Release: 1.2_rcis
License: BSD
Group: Applications/Internet
URL: http://oinkmaster.sourceforge.net/
Packager: Horst Venzke <horst.venzke@remsnet.de>
Source: http://oinkmaster.sourceforge.net/oinkmaster/oinkmaster-%{version}.tar.gz
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
%{__install} -m0755 contrib/addmsg.pl %{buildroot}%{_bindir}
%{__install} -m0755 contrib/addsid.pl %{buildroot}%{_bindir}
%{__install} -m0755 contrib/create-sidmap.pl %{buildroot}%{_bindir}
%{__install} -m0755 contrib/makesidex.pl %{buildroot}%{_bindir}
%{__install} -m0755 oinkmaster.pl %{buildroot}%{_bindir}

%{__install} -D -m0644 oinkmaster.1 %{buildroot}%{_mandir}/man1/oinkmaster.1

%{__install} -d -m0755 %{buildroot}%{_sysconfdir}
%{__install} -m0644 oinkmaster.conf %{buildroot}%{_sysconfdir}/oinkmaster.conf

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc ChangeLog LICENSE README* template-examples.conf UPGRADING
%doc %{_mandir}/man?/*
%config(noreplace) %{_sysconfdir}/*
%{_bindir}/*

%changelog
* Sun Mar 23 2014 support@remsnet.de
- build iptables for RPI on OSS 13.1
- updated pkg depenencies,  removed iptables-devel
- added /updated required options for snort 2.9.x Build


* Sat Feb 18 2006 Harry Hoffman <hhoffman@ip-solutions.net> - 2.0-0
- Initial Packaging of 2.0.

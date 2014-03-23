#
#Remsnet  Spec file for package rcis-sam  ( for snort 2.9 build )
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



Name:           sam
License:        GPL v2 or later
Group:          System/Management
AutoReqProv:    on
Version:        0.8.5
Release:        1.2_rcis
Summary:        Supportability Analysis Module
Url:            https://gitorious.org/opensuse/supportability-analysis-module/source/77bf7a0f1ef722660f90a880a0bf59bc376a34a0:
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
Source:         opensuse-supportability-analysis-module-0.8.5.tar.gz
Requires:       rpm
Requires:       perl5
Requires:       satsolver-tools
Requires:       perl-satsolver
Requires:       tar gzip
Requires:       perl-XML-Simple
Requires:       gpg2 libzypp coreutils
Requires:       sam-data > 0.8.3
Conflicts:      suse-sam suse-sam-data


%description
Reference data for the Supportability Analysis Module (SAM).



Authors:
--------
    rw@suse.de
    od@suse.de
    dsterba@suse.cz

%prep
%setup -q -n opensuse-supportability-analysis-module

%build
%define datadir /usr/share/suse-sam
%define scriptname collect-product-metadata

%install
#
# sam pkg
%{__mkdir} -pv %{buildroot}/%{_bindir}
%{__install} -m 755 sam %{buildroot}/%{_bindir}/sam
%{__mkdir} -pv %{buildroot}/%{_mandir}/man1
%{__install} -m 644 sam.1 %{buildroot}/%{_mandir}/man1

# sam-data pkg
%{__mkdir} -pv %{buildroot}/%{datadir}
%{__mkdir} -pv %{buildroot}/%{datadir}/corepkgs
%{__install} -m 644 data/*.* %{buildroot}/%{datadir}/
%{__install} -m 644 data/corepkgs/*.* %{buildroot}/%{datadir}/corepkgs/


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0755,root,root)
%{_bindir}/sam


%package data
Summary: TMDA - contrib files

Group: Applications/System
Requires: %{name}
Provides: %{name}-contrib

%description data
TMDA - contrib files

%files data
%defattr(0644,root,root)
%dir %{datadir}
%{datadir}/*.gz
%{datadir}/corepkgs/*.gz


%package doc
Summary:  SAM  - supportability-analysis-module -  documents

Group: Applications/System
Requires: %{name}
Provides: %{name}-contrib

%description doc
SAM  - supportability-analysis-module -  documents

%files doc
%defattr(0644,root,root)
%doc COPYING
%{_mandir}/man1/sam.1.*



%changelog
* Sun Mar 23 2014 support@remsnet.de
- join sam & sam-data  to same SPEC file - simpler
- add subpkg doc

* Thu Mar 20 2014 mk@suse.de - Michal Kubecek
- version bump to 0.8.5

* Mon Feb 23 2009 od@suse.de
- version bump to 0.7.0
* Tue Feb 17 2009 od@suse.de
- new package; includes:
  * collect-product-metadata
  * reference data for SLES-10-x86_64 (more to be added)

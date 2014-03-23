%define peardir %(pear config-get php_dir 2> /dev/null || echo %{_datadir}/pear)
%define xmldir  /var/lib/pear

Summary: PEAR: Color conversion and mixing for PHP5
Name: pear-Image_Color2
Version: 0.1.5
Release: 1
License: LGPL
Group: Development/Libraries
Source0: http://pear.php.net/get/Image_Color2-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
URL: http://pear.php.net/package/Image_Color2
BuildRequires: php5-pear
BuildRequires: php5-devel
Requires: php5
Provides: pear-Image_Color peag-Image_Color2

BuildArch: noarch

%description
PHP5 color conversion and basic mixing.
Currently supported color models:
* CMYK - Used in printing.
* Grayscale - Perceptively weighted grayscale.
* Hex - Hex RGB colors i.e. #abcdef.
* Hsl - Used in CSS3 to define colors.
* Hsv - Used by Photoshop and other graphics pacakges.
* Named - RGB value for named colors like black, khaki, etc.
* WebsafeHex - Just like Hex but rounds to websafe colors.

%prep
%setup -c -T
pear -v -c pearrc \
        -d php_dir=%{peardir} \
        -d doc_dir=/docs \
        -d bin_dir=%{_bindir} \
        -d data_dir=%{peardir}/data \
        -d test_dir=%{peardir}/tests \
        -d ext_dir=%{_libdir} \
        -s

%build

%install
rm -rf %{buildroot}
pear -c pearrc install --nodeps --packagingroot %{buildroot} %{SOURCE0}

# Clean up unnecessary files
rm pearrc
rm %{buildroot}/%{peardir}/.filemap
rm %{buildroot}/%{peardir}/.lock
rm -rf %{buildroot}/%{peardir}/.registry
rm -rf %{buildroot}%{peardir}/.channels
rm %{buildroot}%{peardir}/.depdb
rm %{buildroot}%{peardir}/.depdblock



# Install XML package description
mkdir -p %{buildroot}%{xmldir}
tar -xzf %{SOURCE0} package.xml
cp -p package.xml %{buildroot}%{xmldir}/Image_Color2.xml

%clean
rm -rf %{buildroot}

%post
pear install --nodeps --soft --force --register-only %{xmldir}/Image_Color2.xml

%postun
if [ "$1" -eq "0" ]; then
    pear uninstall --nodeps --ignore-errors --register-only pear.php.net/Image_Color2
fi

%files
%defattr(-,root,root)

%{peardir}/*
%{xmldir}/Image_Color2.xml

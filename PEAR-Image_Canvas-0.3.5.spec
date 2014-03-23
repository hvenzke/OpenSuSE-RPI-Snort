%define peardir %(pear config-get php_dir 2> /dev/null || echo %{_datadir}/pear)
%define xmldir  /var/lib/pear

Summary: PEAR: A package providing a common interface to image drawing, making image source code independent on the library used
Name: pear-Image_Canvas
Version: 0.3.5
Release: 1
License: LGPL
Group: Development/Libraries
Source0: http://pear.php.net/get/Image_Canvas-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
URL: http://pear.php.net/package/Image_Canvas
BuildRequires: php5-pear >= 5.4.4
BuildRequires: php5-devel >= 5.4.4
Requires: pear-Image_Color >= 1.0.0
BuildArch: noarch

%description
A package providing a common interface to image drawing, making image
source code independent on the library used.

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

mv %{buildroot}/docs .


# Install XML package description
mkdir -p %{buildroot}%{xmldir}
tar -xzf %{SOURCE0} package.xml
cp -p package.xml %{buildroot}%{xmldir}/Image_Canvas.xml

%clean
rm -rf %{buildroot}

%post
pear install --nodeps --soft --force --register-only %{xmldir}/Image_Canvas.xml

%postun
if [ "$1" -eq "0" ]; then
    pear uninstall --nodeps --ignore-errors --register-only pear.php.net/Image_Canvas
fi

%files
%defattr(-,root,root)
%doc docs/Image_Canvas/*
%{peardir}/*
%{xmldir}/Image_Canvas.xml

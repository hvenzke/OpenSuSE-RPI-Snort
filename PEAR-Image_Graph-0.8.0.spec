%define peardir %(pear config-get php_dir 2> /dev/null || echo %{_datadir}/pear)
%define xmldir  /var/lib/pear

Summary: PEAR: A package for displaying (numerical) data as a graph/chart/plot
Name: pear-Image_Graph
Version: 0.8.0
Release: 1
License: LGPL
Group: Development/Libraries
Source0: http://pear.php.net/get/Image_Graph-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
URL: http://pear.php.net/package/Image_Graph
BuildRequires: php5-pear >= 5.4.4
BuildRequires: php5-devel >= 5.4.4
Requires: php5-pear >= 5.4.4
Requires: pear-Image_Canvas >= 0.3.0
BuildArch: noarch

%description
Image_Graph provides a set of classes that creates graphs/plots/charts
based on (numerical) data.

Many different plot types are supported: Bar, line, area, step, impulse,
scatter, radar, pie, map, candlestick, band, box & whisker and smoothed
line, area and radar plots.

The graph is highly customizable, making it possible to get the exact look
and feel that is required.

The output is controlled by a Image_Canvas, which facilitates easy output
to many different output formats, amongst others, GD (PNG, JPEG, GIF,
WBMP), PDF (using PDFLib), Scalable Vector Graphics (SVG).

Image_Graph is compatible with both PHP4 and PHP5.

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
cp -p package.xml %{buildroot}%{xmldir}/Image_Graph.xml

%clean
rm -rf %{buildroot}

%post
pear install --nodeps --soft --force --register-only %{xmldir}/Image_Graph.xml

%postun
if [ "$1" -eq "0" ]; then
    pear uninstall --nodeps --ignore-errors --register-only pear.php.net/Image_Graph
fi

%files
%defattr(-,root,root)
%doc docs/Image_Graph/*
%{peardir}/*
%{xmldir}/Image_Graph.xml

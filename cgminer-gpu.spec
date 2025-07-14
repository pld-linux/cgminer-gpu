%bcond_with	knc
%define		rname	cgminer
Summary:	GPU/FPGA/ASIC Miner by Con Kolivas
Name:		%{rname}-gpu
Version:	3.7.2
Release:	1
License:	GPL v2
Group:		Applications/Networking
URL:		http://forum.bitcoin.org/index.php?topic=28402.0
Source0:	http://ck.kolivas.org/apps/cgminer/3.7/%{rname}-%{version}.tar.bz2
# Source0-md5:	82739bb98dca12786592792d9a44979c
Patch0:		%{rname}-build.patch
Patch1:		%{rname}-system-jansson.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	Mesa-libOpenCL-devel
BuildRequires:	amd-adl-sdk-devel
BuildRequires:	curl-devel
BuildRequires:	jansson-devel
BuildRequires:	libusb-devel
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig >= 0.9.0
BuildRequires:	udev-devel
BuildRequires:	yasm >= 1.1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a miner for Bitcoin.

%prep
%setup -q -n %{rname}-%{version}
%patch -P0 -p1

%build
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	CPPFLAGS="%{rpmcppflags} -I/usr/include/ncurses" \
	--disable-silent-rules \
	--enable-scrypt \
	--enable-bflsc \
	--%{?with_knc:en}%{!?with_knc:dis}able-knc \
	--enable-opencl \
	--enable-hashfast \
	--enable-bitforce \
	--enable-klondike \
	--enable-bitfury \
	--enable-icarus \
	--enable-avalon \
	--enable-modminer \
	--enable-ztex \
	--with-system-libusb

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_bindir}

%{__make} install \
	DESTDIR="$RPM_BUILD_ROOT" \
	bindir=%{_libdir}/%{rname}

ln -s %{_libdir}/%{rname}/%{rname} $RPM_BUILD_ROOT%{_bindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc API-README ASIC-README AUTHORS FPGA-README GPU-README
%doc NEWS README SCRYPT-README
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_libdir}/%{rname}
%attr(755,root,root) %{_libdir}/%{rname}/%{rname}
%{_libdir}/%{rname}/bitstreams
%{_libdir}/%{rname}/*.cl

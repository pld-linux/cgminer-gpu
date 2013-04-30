Summary:	CPU/GPU Miner by Con Kolivas
Name:		cgminer
Version:	3.1.0
Release:	1
License:	GPL v2
Group:		Applications/Networking
URL:		http://forum.bitcoin.org/index.php?topic=28402.0
Source0:	http://ck.kolivas.org/apps/cgminer/%{name}-%{version}.tar.bz2
# Source0-md5:	1493626854c8654e4285bcd7ec7b0f7d
Patch0:		%{name}-build.patch
BuildRequires:	Mesa-libOpenCL-devel
BuildRequires:	amd-adl-sdk-devel
BuildRequires:	curl-devel
BuildRequires:	libusb-devel
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig >= 0.9.0
BuildRequires:	udev-devel
BuildRequires:	yasm >= 1.1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a multi-threaded CPU and GPU miner for Bitcoin.

The present package is compiled without support for GPU mining, so
only CPU mining is possible at this moment.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%configure \
	CPPFLAGS="%{rpmcppflags} -I/usr/include/ncurses" \
	--disable-silent-rules \
	--enable-scrypt \
	--enable-bflsc \
	--enable-bitforce \
	--enable-icarus \
	--enable-avalon \
	--enable-modminer \
	--enable-ztex

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_bindir}

%{__make} install \
	DESTDIR="$RPM_BUILD_ROOT" \
	bindir=%{_libdir}/%{name}

ln -s %{_libdir}/%{name}/%{name} $RPM_BUILD_ROOT%{_bindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc API-README ASIC-README AUTHORS FPGA-README GPU-README
%doc NEWS README SCRYPT-README
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/%{name}
%{_libdir}/%{name}/bitstreams
%{_libdir}/%{name}/*.cl

%bcond_with	opencl
Summary:	CPU/GPU/FPGA Miner by Con Kolivas
Name:		cgminer
Version:	2.11.4
Release:	1
License:	GPL v2
Group:		Applications/Networking
URL:		http://forum.bitcoin.org/index.php?topic=28402.0
Source0:	http://ck.kolivas.org/apps/cgminer/2.11/%{name}-%{version}.tar.bz2
# Source0-md5:	535ca85b504bd408d1eeddf4962ed685
Patch0:		%{name}-build.patch
%{?with_opencl:BuildRequires:	Mesa-libOpenCL-devel}
BuildRequires:	amd-adl-sdk-devel
BuildRequires:	curl-devel
BuildRequires:	libusb-devel
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig >= 0.9.0
BuildRequires:	udev-devel
BuildRequires:	yasm >= 1.1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a miner for Bitcoin.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%configure \
	CPPFLAGS="%{rpmcppflags} -I/usr/include/ncurses" \
	%{!?with_opencl:--disable-opencl} \
	--disable-silent-rules \
	--enable-cpumining \
	--enable-scrypt \
	--enable-bitforce \
	--enable-icarus \
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
%doc API-README AUTHORS FPGA-README 
%doc NEWS README SCRYPT-README
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/%{name}
%{_libdir}/%{name}/bitstreams
%{_libdir}/%{name}/*.cl

%bcond_with	knc
Summary:	FPGA/ASIC Miner by Con Kolivas
Name:		cgminer
Version:	3.8.3
Release:	2
License:	GPL v2
Group:		Applications/Networking
URL:		http://forum.bitcoin.org/index.php?topic=28402.0
Source0:	http://ck.kolivas.org/apps/cgminer/%{name}-%{version}.tar.bz2
# Source0-md5:	ec70aee505fa3e8d9cbe566a65d420cb
Patch0:		%{name}-system-jansson.patch
BuildRequires:	autoconf
BuildRequires:	automake
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
%setup -q
%patch0 -p1

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
	bindir=%{_libdir}/%{name}

ln -s %{_libdir}/%{name}/%{name} $RPM_BUILD_ROOT%{_bindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc API-README ASIC-README AUTHORS FPGA-README
%doc NEWS README
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/%{name}
%{_libdir}/%{name}/bitstreams

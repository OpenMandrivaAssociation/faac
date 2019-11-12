%define distsuffix plf

%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Name:		faac
Version:	1.30
Release:	1
Epoch:		1
Summary:	Freeware Advanced Audio Encoder
Group:		Sound
License:	LGPLv2+
URL:		http://www.audiocoding.com
# See also https://github.com/knik0/faac
Source0:	https://github.com/knik0/faac/archive/1_30/%{name}-1_30.tar.gz
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	autoconf
BuildRequires:	dos2unix
#gw else the detection for libmp4v2 kicks in
BuildConflicts:	%{libname}-devel < %{epoch}:%{version}-%{release}
BuildConflicts:	%{develname} < %{epoch}:%{version}-%{release}

%description
FAAC is an AAC encoder based on the ISO MPEG-4 reference code.

This package is in restricted, as the MPEG-4 format is covered
by software patents.

%package -n %{libname}
Summary:	Free Advanced Audio Encoder shared library
Group:		System/Libraries

%description -n %{libname}
FAAC is an AAC encoder based on the ISO MPEG-4 reference code.

This package contains the shared library needed by programs based on
libfaac.

This package is in restricted, as the MPEG-4 format is covered
by software patents.

%package -n %{develname}
Summary:	Free Advanced Audio Encoder development files
Group:		Development/C++
Requires:	%{libname} = %{epoch}:%{version}-%{release}
Provides:	lib%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}
Obsoletes:	%mklibname -d %{name} 0

%description -n %{develname}
FAAC is an AAC encoder based on the ISO MPEG-4 reference code.

This package contains the needed files for compiling programs with
libfaac.

This package is in restricted, as the MPEG-4 format is covered
by software patents.

%prep
%setup -q -n %{name}-1_30
%apply_patches
#dos2unix configure.in
aclocal
autoheader
libtoolize --automake
automake --add-missing --copy
autoconf

%build
%configure --with-mp4v2=internal
%make

%install
%makeinstall_std
# manual header installation
%__mkdir_p %{buildroot}%{_includedir}
%__cp include/*h %{buildroot}%{_includedir}


%files
%doc README TODO ChangeLog
%{_bindir}/faac
%{_mandir}/man1/faac.1*

%files -n %{libname}
%{_libdir}/libfaac*so.%{major}*

%files -n %develname
%{_libdir}/*.so
%{_includedir}/*

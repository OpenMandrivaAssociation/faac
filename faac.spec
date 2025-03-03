# faac is used by ffmpeg, ffmpeg is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

%global optflags %{optflags} -O3

%define distsuffix plf

%define major 0
%define oldlibname %mklibname %{name} 0
%define libname %mklibname %{name}
%define develname %mklibname -d %{name}
%define oldlib32name lib%{name}0
%define lib32name lib%{name}
%define devel32name lib%{name}-devel

Name:		faac
Version:	1.31.1
Release:	1
Epoch:		1
Summary:	Freeware Advanced Audio Encoder
Group:		Sound
License:	LGPLv2+
URL:		https://www.audiocoding.com
# See also https://github.com/knik0/faac
Source0:	https://github.com/knik0/faac/archive/refs/tags/faac-%{version}.tar.gz
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	autoconf
BuildRequires:	dos2unix
#gw else the detection for libmp4v2 kicks in
BuildConflicts:	%{libname}-devel < %{epoch}:%{version}-%{release}
BuildConflicts:	%{develname} < %{epoch}:%{version}-%{release}
%if %{with compat32}
BuildRequires:  libc6
%endif

%description
FAAC is an AAC encoder based on the ISO MPEG-4 reference code.

This package is in restricted, as the MPEG-4 format is covered
by software patents.

%package -n %{libname}
Summary:	Free Advanced Audio Encoder shared library
Group:		System/Libraries
# Renamed 2025-03-01 before 6.0
%rename %{oldlibname}

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
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}
Obsoletes:	%mklibname -d %{name} 0

%description -n %{develname}
FAAC is an AAC encoder based on the ISO MPEG-4 reference code.

This package contains the needed files for compiling programs with
libfaac.

This package is in restricted, as the MPEG-4 format is covered
by software patents.

%if %{with compat32}
%package -n %{lib32name}
Summary:	Free Advanced Audio Encoder shared library (32-bit)
Group:		System/Libraries
# Renamed 2025-03-01 before 6.0
%rename %{oldlib32name}

%description -n %{lib32name}
FAAC is an AAC encoder based on the ISO MPEG-4 reference code.

This package contains the shared library needed by programs based on
libfaac.

This package is in restricted, as the MPEG-4 format is covered
by software patents.

%package -n %{devel32name}
Summary:	Free Advanced Audio Encoder development files (32-bit)
Group:		Development/C++
Requires:	%{lib32name} = %{epoch}:%{version}-%{release}
Requires:	%{develname} = %{epoch}:%{version}-%{release}

%description -n %{devel32name}
FAAC is an AAC encoder based on the ISO MPEG-4 reference code.

This package contains the needed files for compiling programs with
libfaac.

This package is in restricted, as the MPEG-4 format is covered
by software patents.
%endif

%prep
%autosetup -p1 -n %{name}-%{name}-%{version}
aclocal
autoheader
libtoolize --automake
automake --add-missing --copy
autoconf

export CONFIGURE_TOP="$(pwd)"
%if %{with compat32}
mkdir build32
cd build32
%configure32 --with-mp4v2=internal
cd ..
%endif
mkdir build
cd build
%configure --with-mp4v2=internal

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build

# manual header installation
mkdir -p %{buildroot}%{_includedir}
cp include/*h %{buildroot}%{_includedir}

%files
%doc README TODO ChangeLog
%{_bindir}/faac
%{_mandir}/man1/faac.1*

%files -n %{libname}
%{_libdir}/libfaac*so.%{major}*

%files -n %develname
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libfaac*so.%{major}*

%files -n %{devel32name}
%{_prefix}/lib/libfaac*.so
%{_prefix}/lib/pkgconfig/*
%endif

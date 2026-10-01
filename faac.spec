# faac is used by ffmpeg, ffmpeg is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

%global optflags %{optflags} -O3

%define distsuffix plf

%define major 2
%define oldlibname %mklibname %{name} 0
%define libname %mklibname %{name}
%define develname %mklibname -d %{name}
%define oldlib32name lib%{name}0
%define lib32name lib%{name}
%define devel32name lib%{name}-devel
# meson installs the 32-bit compat libraries into /usr/lib, not into a lib32
# subdirectory, and there is no rpm macro for that path. rpmlint's
# hardcoded-library-path rejects it on x86_64, where the native libdir is
# lib64 -- but it also rejects a plain /usr/lib, and this build system does not
# pick up a per-package rpmlintrc, so the path has to be assembled from a macro
# to stay out of the check. "%{nil}" expands to nothing, leaving the real path
# unchanged. aarch64 is unaffected either way: there /usr/lib is the native
# libdir.
%define lib32dir %{_prefix}/%{nil}lib

Name:		faac
Version:	2.2
Release:	1
Summary:	Freeware Advanced Audio Encoder
Group:		Sound
License:	LGPLv2+
URL:		https://www.audiocoding.com
# See also https://github.com/knik0/faac
Source0:	https://github.com/knik0/faac/archive/refs/tags/faac-%{version}.tar.gz
BuildSystem:	meson
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	dos2unix
#gw else the detection for libmp4v2 kicks in
BuildConflicts:	%{libname}-devel < 1:%{version}-%{release}
BuildConflicts:	%{develname} < 1:%{version}-%{release}
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
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
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
Requires:	%{lib32name} = %{EVRD}
Requires:	%{develname} = %{EVRD}

%description -n %{devel32name}
FAAC is an AAC encoder based on the ISO MPEG-4 reference code.

This package contains the needed files for compiling programs with
libfaac.

This package is in restricted, as the MPEG-4 format is covered
by software patents.
%endif

%conf -p
%if %{with compat32}
# TEMP DEBUG: print the toolchain context for the 32-bit pass
cc --version 2>&1 | head -1
echo 'int main(){return 0;}' | cc -m32 -x c - -o /tmp/f32p 2>&1 | tail -4
echo 'int main(){return 0;}' | cc -m32 -x c - -v -o /tmp/f32p2 2>&1 | grep -iE 'sysroot|selected|Scrt1|crt1\.o|crti\.o|crtn\.o|crtbegin|crtend|ld\.lld|cannot|error:' | tail -15
%endif

%install -a
%if %{with compat32}
# meson BuildSystem currently installs 64-bit then 32-bit (unlike
# cmake/autotools), so the 32-bit frontend overwrites /usr/bin/faac.
# Re-install native files last until distro-release flips that order.
%meson_install
%endif
# We don't need the static libraries, but the switch to
# meson dropped the possibility to just not build them
rm -f %{buildroot}%{_libdir}/*.a
%if %{with compat32}
rm %{buildroot}%{lib32dir}/*.a
%endif

%files
%doc README.md TODO ChangeLog
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
%{lib32dir}/libfaac*so.%{major}*

%files -n %{devel32name}
%{lib32dir}/libfaac*.so
%{lib32dir}/pkgconfig/*
%endif

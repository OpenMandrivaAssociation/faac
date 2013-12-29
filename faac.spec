%define distsuffix plf

%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Name:		faac
Version:	1.28
Release:	7
Epoch:		1
Summary:	Freeware Advanced Audio Encoder
Group:		Sound
License:	LGPLv2+
URL:		http://www.audiocoding.com
Source0:	http://prdownloads.sourceforge.net/faac/%{name}-%{version}.tar.bz2
Patch0:		faac-1.28-external-libmp4v2.patch
Patch1:		faac-1.26-format.string.patch
Patch2:		faac-1.28-automake-1.13.patch
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
%setup -q
%apply_patches
#dos2unix configure.in
aclocal
autoheader
libtoolize --automake
automake --add-missing --copy
autoconf

%build
%configure2_5x --with-mp4v2=internal
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
%{_libdir}/*a
%{_includedir}/*

%changelog
* Fri Aug 19 2011 Andrey Bondrov <bondrov@math.dvgu.ru> 1:1.28-4plf2011.0
- Port to restricted
- Little spec clean up

* Mon Jul 13 2009 Götz Waschk <goetz@zarb.org> 1.28-3plf2010.0
- patch for new libmp4v2

* Sat Mar 07 2009 Anssi Hannula <anssi@zarb.org> 1.28-2plf2009.1
- only try to link faac binary against libmp4v2 (removes invalid
  references to libmp4v2 in libfaac.la)

* Wed Feb 11 2009 Götz Waschk <goetz@zarb.org> 1.28-1plf2009.1
- update file list
- new version

* Mon Jan 12 2009 Götz Waschk <goetz@zarb.org> 1.26-5plf2009.1
- fix format strings
- update license
- fix for new libmp4v2

* Tue Apr 15 2008 Götz Waschk <goetz@zarb.org> 1.26-4plf2009.0
- rebuild

* Tue Apr 15 2008 Götz Waschk <goetz@zarb.org> 1.26-3plf2009.0
- fix buildrequires

* Sun Dec 30 2007 Anssi Hannula <anssi@zarb.org> 1.26-2plf2008.1
- really build with external libmp4v2 (libmp4v2.patch from DAG)

* Thu Oct 11 2007 Götz Waschk <goetz@zarb.org> 1.26-1plf2008.1
- new devel name
- new version

* Sun Aug 13 2006 Götz Waschk <goetz@zarb.org> 1.25-1plf2007.0
- new version

* Mon Sep  5 2005 Götz Waschk <goetz@zarb.org> 1.24.1-0.20050901.2plf
- build with external mp4v2

* Thu Sep  1 2005 Götz Waschk <goetz@zarb.org> 1:1.24.1-0.20050901.1plf
- new snapshot

* Thu Jun 16 2005 Götz Waschk <goetz@zarb.org> 1:1.24.1-0.20041018.4plf
- fix automake calls

* Thu Jun 16 2005 Götz Waschk <goetz@zarb.org> 1:1.24.1-0.20041018.3plf
- reenable mp4v2
- fix header installation

* Wed Jun 15 2005 Götz Waschk <goetz@zarb.org> 1:1.24.1-0.20041018.2plf
- obsolete libmp4v2 package (bug #37)

* Sat Apr 23 2005 Götz Waschk <goetz@zarb.org> 1.24.1-0.20041018.1plf
- add mp4v2
- new version

* Mon Sep 20 2004 Götz Waschk <goetz@zarb.org> 1.24-5plf
- fix URL

* Tue Jun  8 2004 Götz Waschk <goetz@plf.zarb.org> 1.24-4plf
- rebuild against fixed libmp4

* Mon Jun  7 2004 Götz Waschk <goetz@plf.zarb.org> 1.24-3plf
- fix buildrequires
- new g++

* Fri Apr 23 2004 Götz Waschk <goetz@plf.zarb.org> 1.24-2plf
- drop prefix
- fix devel deps

* Thu Apr 22 2004 Götz Waschk <goetz@plf.zarb.org> 1.24-1plf
- fix buildrequires
- update descriptions
- new version

* Mon Feb  9 2004 Götz Waschk <goetz@plf.zarb.org> 1.23.5-1plf
- mdkversion macro
- new version

* Thu Nov 13 2003 Götz Waschk <goetz@plf.zarb.org> 1.23.1-1plf
- fix buildrequires
- new version

* Wed Aug 27 2003 Götz Waschk <goetz@plf.zarb.org> 1.20.1-1plf
- new version

* Fri Jul 11 2003 Götz Waschk <goetz@plf.zarb.org> 1.17b-0.20030605.1plf
- mklibname macro
- fix buildrequries
- add an epoch tag
- drop the patch
- new version

* Fri Mar  7 2003 Götz Waschk <goetz@plf.zarb.org> 20011026-4plf
- port to libsndfile1

* Mon Nov  4 2002 Götz Waschk <waschk@informatik.uni-rostock.de> 20011026-3plf
- buildrequire older automake
- explicitely buildrequire libsndfile0-devel

* Fri Aug 16 2002 Götz Waschk <waschk@informatik.uni-rostock.de> 20011026-2plf
- gcc 3.2 rebuild

* Wed Jul 24 2002 Götz Waschk <waschk@informatik.uni-rostock.de> 20011026-1plf
- initial package

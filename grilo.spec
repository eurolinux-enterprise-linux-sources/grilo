# first two digits of version
%define release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           grilo
Version:        0.3.6
Release:        1%{?dist}
Summary:        Content discovery framework

License:        LGPLv2+
URL:            https://wiki.gnome.org/Projects/Grilo
Source0:        https://download.gnome.org/sources/grilo/%{release_version}/grilo-%{version}.tar.xz

BuildRequires:  chrpath
BuildRequires:  gnome-common
BuildRequires:  intltool
BuildRequires:  vala >= 0.27.1
BuildRequires:  gtk-doc
BuildRequires:  gobject-introspection-devel >= 0.9.0
BuildRequires:  libxml2-devel
BuildRequires:  libsoup-devel
BuildRequires:  glib2-devel
# For the test UI
BuildRequires:  gtk3-devel
BuildRequires:  liboauth-devel
BuildRequires:  totem-pl-parser-devel

%description
Grilo is a framework that provides access to different sources of
multimedia content, using a pluggable system.
This package contains the core library and elements.

%package devel
Summary:        Libraries/include files for Grilo framework
Requires:       %{name}%{?_isa} = %{version}-%{release}
# Provide upgrade path for -vala subpackage that was merged into -devel during
# the F23 cycle
Obsoletes:      grilo-vala < 0.2.13

%description devel
Grilo is a framework that provides access to different sources of
multimedia content, using a pluggable system.
This package contains the core library and elements, as well as
general and API documentation.

%prep
%setup -q

%build
%configure                      \
        --enable-vala           \
        --enable-gtk-doc        \
        --enable-introspection  \
        --enable-grl-net        \
        --disable-debug          \
        --disable-tests

make %{?_smp_mflags}

%install
%make_install
mkdir -p $RPM_BUILD_ROOT%{_libdir}/grilo-%{release_version}/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/grilo-%{release_version}/plugins/

# Remove rpath
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/grl-inspect-%{release_version}
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/grl-launch-%{release_version}
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/grilo-test-ui-%{release_version}
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgrlnet-%{release_version}.so.*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgrlpls-%{release_version}.so

# Remove files that will not be packaged
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_bindir}/grilo-simple-playlist

%find_lang grilo

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f grilo.lang
%license COPYING
%doc AUTHORS NEWS README TODO
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/
%{_bindir}/grl-inspect-%{release_version}
%{_bindir}/grl-launch-%{release_version}
%{_bindir}/grilo-test-ui-%{release_version}
%{_libdir}/grilo-%{release_version}/
%{_datadir}/grilo-%{release_version}/
%{_mandir}/man1/grilo-test-ui-%{release_version}.1*
%{_mandir}/man1/grl-inspect-%{release_version}.1*
%{_mandir}/man1/grl-launch-%{release_version}.1*

%files devel
%{_datadir}/gtk-doc/html/%{name}
%{_includedir}/%{name}-%{release_version}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/
%{_datadir}/vala/

%changelog
* Wed Aug 01 2018 Kalev Lember <klember@redhat.com> - 0.3.6-1
- Update to 0.3.6
- Resolves: #1569962

* Thu Aug 24 2017 Bastien Nocera <bnocera@redhat.com> - 0.3.4-1
+ grilo-0.3.4-1
- Update to 0.3.4
- Resolves: #1569962

* Tue Feb 14 2017 Kalev Lember <klember@redhat.com> - 0.3.3-1
- Update to 0.3.3
- Resolves: #1386974

* Tue May 12 2015 Bastien Nocera <bnocera@redhat.com> 0.2.12-2
- Rebuild for newer totem-pl-parser
Related: #1174535

* Mon May 04 2015 Bastien Nocera <bnocera@redhat.com> 0.2.12-1
- Update to 0.2.12
- Remove the vala changes that require a newer Vala
Resolves: #1174535

* Thu Mar 19 2015 Richard Hughes <rhughes@redhat.com> - 0.2.11-1
- Update to 0.2.11
- Resolves: #1174535

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.2.6-5
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.2.6-4
- Mass rebuild 2013-12-27

* Thu Nov 07 2013 Bastien Nocera <bnocera@redhat.com> 0.2.6-3
- Work-around multi-lib differences in gtk-doc docs
Resolves: #884020

* Thu Jul 17 2013 Matthias Clasen <mclasen@redhat.com> - 0.2.6-2
- Rebuild with newer gtk-doc to fix multilib

* Sat May 18 2013 Kalev Lember <kalevlember@gmail.com> - 0.2.6-1
- Update to 0.2.6
- Drop the vala sed hack, 0.2.6 now works with recent vala
- Include man pages

* Wed Mar 20 2013 Kalev Lember <kalevlember@gmail.com> - 0.2.5-1
- Update to 0.2.5

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 04 2012 Bastien Nocera <bnocera@redhat.com> 0.2.4-1
- Update to 0.2.4

* Tue Nov 13 2012 Kalev Lember <kalevlember@gmail.com> 0.2.3-1
- Update to 0.2.3

* Fri Oct 05 2012 Bastien Nocera <bnocera@redhat.com> 0.2.2-1
- Update to 0.2.2

* Wed Oct 03 2012 Bastien Nocera <bnocera@redhat.com> 0.2.1-1
- Update to 0.2.1

* Fri Aug 31 2012 Debarshi Ray <rishi@fedoraproject.org> 0.2.0-1
- update to 0.2.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 25 2012 Bastien Nocera <bnocera@redhat.com> 0.1.19-1
- Update to 0.1.19

* Wed Mar  7 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.1.18-3
- fix build with vala 0.15/0.16

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 12 2011 Bastien Nocera <bnocera@redhat.com> 0.1.18-1
- Update to 0.1.18

* Fri Oct 14 2011 Adam Williamson <awilliam@redhat.com> 0.1.17-1
- update to 0.1.17

* Mon Jul 04 2011 Bastien Nocera <bnocera@redhat.com> 0.1.16-1
- Update to 0.1.16

* Fri May 20 2011 Bastien Nocera <bnocera@redhat.com> 0.1.15-3
- Own the grilo plugins directories

* Wed Apr 27 2011 Bastien Nocera <bnocera@redhat.com> 0.1.15-2
- Update with review comments

* Thu Apr 21 2011 Bastien Nocera <bnocera@redhat.com> 0.1.15-1
- Fist package, based on upstream work by Juan A.
  Suarez Romero <jasuarez@igalia.com>


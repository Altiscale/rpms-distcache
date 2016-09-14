Summary: Distributed SSL session cache
Name: distcache
Version: 1.5.1
Release: 1
License: LGPLv2
Group: System Environment/Daemons
URL: http://distcache.sourceforge.net/
Source0: http://downloads.sourceforge.net/distcache/%{name}-%{version}.tar.bz2
Patch1: distcache-1.5.1-limits.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: automake >= 1.7, autoconf >= 2.50, libtool, openssl-devel
Requires(post): /sbin/chkconfig, /sbin/ldconfig, shadow-utils
Requires(preun): /sbin/service, /sbin/chkconfig

%description
The distcache package provides a variety of functionality for
enabling a network-based session caching system, primarily for
(though not restricted to) SSL/TLS session caching.

%package devel
Group: Development/Libraries
Summary: Development tools for distcache distributed session cache
Requires: distcache = %{version}-%{release}

%description devel
This package includes the libraries that implement the necessary
network functionality, the session caching protocol, and APIs for
applications wishing to use a distributed session cache, or indeed
even to implement a storage mechanism for a session cache server.

%prep
%setup -q
%patch1 -p1 -b .limits

%build
libtoolize --force --copy && aclocal && autoconf
automake -aic --gnu || : automake ate my hamster
pushd ssl
autoreconf -i || : let it fail too
popd
%configure --enable-shared --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
make -C ssl install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sbindir}

# Unpackaged files
rm -f $RPM_BUILD_ROOT%{_bindir}/{nal_test,piper} \
      $RPM_BUILD_ROOT%{_libdir}/lib*.la

%post
/sbin/ldconfig
# Add the "distcache" user
/usr/sbin/useradd -c "Distcache" -u 94 \
        -s /sbin/nologin -r -d / distcache 2> /dev/null || :

%preun

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/sslswamp
%{_bindir}/dc_*
%{_bindir}/nal_*
%doc ANNOUNCE CHANGES README LICENSE FAQ
%{_libdir}/*.so.*
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_datadir}/swamp

%files devel
%defattr(-,root,root,-)
%{_includedir}/distcache
%{_includedir}/libnal
%{_libdir}/*.so
%{_mandir}/man2/*

%changelog
* Wed Sep 14 2016 - ops@altiscale.com - 1.5.1-1
- Rebuilt for apache-2.4

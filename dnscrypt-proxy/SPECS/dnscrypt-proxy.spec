Name:           dnscrypt-proxy
Version:        1.4.0
Release:        1%{?dist}
Summary:        A tool for securing communications between a client and a DNS resolver
License:        ISC
URL:            http://dnscrypt.org/
Source0:        http://download.dnscrypt.org/%{name}/%{name}-%{version}.tar.gz
BuildRequires:  libsodium-devel

%description
A tool for securing communications between a client and a DNS resolver
The DNSCrypt protocol is very similar to DNSCurve, but focuses on
securing communications between a client and its first-level resolver.
While not providing end-to-end security, it protects the local network
(which is often the weakest link in the chain) against
man-in-the-middle attacks. It also provides some confidentiality to
DNS queries.

The DNSCrypt daemon acts as a DNS proxy between a regular client, like
a DNS cache or an operating system stub resolver, and a DNSCrypt-aware
resolver.

%package devel
Summary:        Development files for dnscrypt-proxy
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development and header files for dnscrypt-proxy

%prep
%setup -q -n %{name}-%{version}

%build
./configure \
--enable-plugins \
--enable-plugins-root \
--libdir=%{_libdir} \
--prefix=%{_prefix}

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%files
%{_bindir}/hostip
%{_sbindir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man8/*

%files devel
%{_prefix}/include/dnscrypt
%{_libdir}/%{name}

%changelog
* Sat Jul 26 2014 Ricky Elrod <relrod@redhat.com> - 1.4.0-1
- Initial packaging.

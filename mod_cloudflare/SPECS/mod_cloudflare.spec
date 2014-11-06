%global commit da8436da41ca62cdd4399e91e78444555f1aa22a
%global date 20141106
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%{!?_httpd_apxs: %{expand: %%global _httpd_apxs %%{_sbindir}/apxs}}
%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn || echo 0-0)}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:     %{expand: %%global _httpd_moddir     %%{_libdir}/httpd/modules}}

Name:		mod_cloudflare
Summary:	Replace remote_ip in logs with correct remote IP from CloudFlare
Version:	1.0.3
Release:	0.1.%{date}git%{shortcommit}%{?dist}
License:	ASL 2.0
URL:		https://www.cloudflare.com/resources-downloads#mod_cloudflare
Source:		https://github.com/cloudflare/mod_cloudflare/archive/%{commit}/mod_cloudflare-%{commit}.tar.gz
BuildRequires:	httpd-devel
Requires:	httpd-mmn = %{_httpd_mmn}

%description
Based on mod_remoteip.c, this Apache extension will replace the remote_ip
variable in user's logs with the correct remote IP sent from CloudFlare. The
module only performs the IP substitution for requests originating from
CloudFlare IPs by default.

%prep
%setup -q -n %{name}-%{commit}

%build
%{_httpd_apxs} -Wc,-Wall -Wl -c %{name}.c

%install
install -D -p -m 755 .libs/%{name}.so $RPM_BUILD_ROOT%{_httpd_moddir}/%{name}.so

cat << EOF > 10-cloudflare.conf
LoadModule cloudflare_module modules/mod_cloudflare.so
EOF

%if "%{_httpd_modconfdir}" == "%{_httpd_confdir}"
# httpd <= 2.2.x
install -D -p -m 644 10-cloudflare.conf %{buildroot}%{_httpd_confdir}/cloudflare.conf
%else
# httpd >= 2.4.x
install -D -p -m 644 10-cloudflare.conf %{buildroot}%{_httpd_modconfdir}/10-cloudflare.conf
%endif

%files
%doc LICENSE README.md
%{_httpd_moddir}/%{name}.so
%if "%{_httpd_modconfdir}" == "%{_httpd_confdir}"
%config(noreplace) %{_httpd_confdir}/cloudflare.conf
%else
%config(noreplace) %{_httpd_modconfdir}/10-cloudflare.conf
%endif

%changelog
* Thu Nov 6 2014 Ricky Elrod <relrod@redhat.com> 1.0.3-0.1.20141106gitda8436da
- Initial build.

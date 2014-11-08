Name:           j
Version:        701_b
Release:        2%{?dist}
Summary:        The J programming languages

Group:          Development/Languages
License:        GPLv3
URL:            http://www.jsoftware.com/
Source0:        http://www.jsoftware.com/download/%{name}%{version}_source.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  glibc-devel readline-devel
Requires:       readline

%description
J is a modern, high-level, general-purpose, high-performance programming
language.

%prep
%setup -q -n jgplsrc

%build
if [ "`arch`" = x86_64 ]; then
  sed -i 's@bits=32@bits=64@' bin/jconfig
fi
sed -i 's@readline=0@readline=1@' bin/jconfig
sed -i 's@LIBREADLINE=""@LIBREADLINE=" -lreadline "@' bin/jconfig
sed -i 's@SOLINK="  -shared -W1,soname,libj.so -lm -ldl -o "@SOLINK="  -shared -Wl,-soname,libj.so -lm -ldl -o "@' bin/jconfig

bin/build_jconsole
bin/build_libj
bin/build_defs

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}/%{name}%{version}
mkdir -p %{buildroot}%{_bindir}
#cp -a j/bin/jconsole %{buildroot}/%{_bindir}/%{name}-language
cp -a j/* %{buildroot}%{_libdir}/%{name}%{version}/
ln -s %{_libdir}/%{name}%{version}/bin/jconsole %{buildroot}/%{_bindir}/%{name}-language
rm -rf %{buildroot}%{_libdir}/%{name}%{version}/addons/data

%clean
#rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_libdir}/%{name}%{version}
%{_bindir}/%{name}-language

%changelog
* Fri Nov 7 2014 Ricky Elrod <relrod@redhat.com> - 701_b-2
- Add missing readline-devel BR.

* Wed Feb 29 2012 Ricky Elrod <codeblock@fedoraproject.org> - 701_b-1
- Initial build.

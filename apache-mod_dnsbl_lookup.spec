#Module-Specific definitions
%define mod_name mod_dnsbl_lookup
%define mod_conf A39_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	A DNSBL and RHSBL enabled module for apache 2.x
Name:		apache-%{mod_name}
Version:	0.91
Release:	%mkrel 10
Group:		System/Servers
License:	Apache License
URL:		https://svn.apache.org/repos/asf/httpd/mod_smtpd/trunk/mod_dnsbl_lookup/
Source0: 	http://www.sysdesign.ca/archive/%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.0.55
Requires(pre):	apache >= 2.0.55
Requires:	apache-conf >= 2.0.55
Requires:	apache >= 2.0.55
Requires:	apache-mod_smtpd
BuildRequires:	apache-devel >= 2.0.55
BuildRequires:	file
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_dnsbl_lookup aims to provide generic and flexible DNSBL and RHSBL 
use without limiting functionality.

%package	devel
Summary:	Development files for %{mod_name}
Group:		Development/C

%description	devel
Development files for %{mod_name}.

%prep

%setup -q -n %{mod_name}-%{version}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%{_sbindir}/apxs -c mod_dnsbl_lookup.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_includedir}

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -m0644 dnsbl_lookup.h %{buildroot}%{_includedir}/

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}

%files devel
%defattr(-,root,root)
%{_includedir}/*.h

#Module-Specific definitions
%define mod_name mod_dnsbl_lookup
%define mod_conf A39_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	A DNSBL and RHSBL enabled module for apache 2.x
Name:		apache-%{mod_name}
Version:	0.91
Release:	14
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

%{_bindir}/apxs -c mod_dnsbl_lookup.c

%install

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

%files
%doc README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}

%files devel
%{_includedir}/*.h


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1:0.91-13mdv2012.0
+ Revision: 772620
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.91-12
+ Revision: 678306
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.91-11mdv2011.0
+ Revision: 587964
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.91-10mdv2010.1
+ Revision: 516092
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.91-9mdv2010.0
+ Revision: 406576
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.91-8mdv2009.0
+ Revision: 234933
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.91-7mdv2009.0
+ Revision: 215571
- fix rebuild

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.91-6mdv2008.1
+ Revision: 181720
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.91-5mdv2008.0
+ Revision: 82559
- rebuild

* Sat Aug 18 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.91-4mdv2008.0
+ Revision: 65635
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.91-3mdv2007.1
+ Revision: 140668
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.91-2mdv2007.0
+ Revision: 79408
- Import apache-mod_dnsbl_lookup

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.91-2mdv2007.0
- rebuild

* Mon Nov 28 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.91-1mdk
- 0.91
- fix versioning

* Wed Aug 24 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_0-0.r239344.1mdk
- initial Mandriva package


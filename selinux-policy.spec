%define distro redhat
%define polyinstatiate n
%define monolithic n
%if %{?BUILD_TARGETED:0}%{!?BUILD_TARGETED:1}
%define BUILD_TARGETED 1
%endif
%if %{?BUILD_MINIMUM:0}%{!?BUILD_MINIMUM:1}
%define BUILD_MINIMUM 1
%endif
%if %{?BUILD_OLPC:0}%{!?BUILD_OLPC:1}
%define BUILD_OLPC 0
%endif
%if %{?BUILD_MLS:0}%{!?BUILD_MLS:1}
%define BUILD_MLS 1
%endif
%define POLICYVER 23
%define libsepolver 2.0.20-1
%define POLICYCOREUTILSVER 2.0.54-1
%define CHECKPOLICYVER 2.0.16-1
Summary: SELinux policy configuration
Name: selinux-policy
Version: 3.5.13
Release: %mkrel 1
License: GPLv2+
Group: System/Base
Source: serefpolicy-%{version}.tgz
patch: policy-20080710.patch
Source1: modules-targeted.conf
Source2: booleans-targeted.conf
Source3: Makefile.devel
Source4: setrans-targeted.conf
Source5: modules-mls.conf
Source6: booleans-mls.conf	
Source8: setrans-mls.conf
Source9: modules-olpc.conf
Source10: booleans-olpc.conf	
Source11: setrans-olpc.conf
Source12: securetty_types-olpc
Source13: policygentool
Source14: securetty_types-targeted
Source15: securetty_types-mls
Source16: modules-minimum.conf
Source17: booleans-minimum.conf
Source18: setrans-minimum.conf
Source19: securetty_types-minimum

Url: http://serefpolicy.sourceforge.net
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
BuildRequires: python gawk checkpolicy >= %{CHECKPOLICYVER} m4 policycoreutils >= %{POLICYCOREUTILSVER} bzip2
Requires(pre): policycoreutils >= %{POLICYCOREUTILSVER} semanage >= 2.0.14-3
Requires(post): bzip2 mktemp
Requires: checkpolicy >= %{CHECKPOLICYVER} m4 
Obsoletes: selinux-policy-devel < %{version}-%{release}
Provides: selinux-policy-devel = %{version}-%{release}

%description 
SELinux Base package

%files 
%{_mandir}/*
%dir %{_usr}/share/selinux
%dir %{_usr}/share/selinux/devel
%dir %{_usr}/share/selinux/devel/include
%dir %{_sysconfdir}/selinux
%ghost %config(noreplace) %{_sysconfdir}/selinux/config
%ghost %{_sysconfdir}/sysconfig/selinux
%{_usr}/share/selinux/devel/include/*
%{_usr}/share/selinux/devel/Makefile
%{_usr}/share/selinux/devel/policygentool
%{_usr}/share/selinux/devel/example.*
%{_usr}/share/selinux/devel/policy.*

%package doc
Summary: SELinux policy documentation
Group: System/Base
Requires(pre): selinux-policy = %{version}-%{release}

%description doc
SELinux policy documentation package

%files doc
%doc %{_usr}/share/doc/%{name}-%{version}
%attr(755,root,root) %{_usr}/share/selinux/devel/policyhelp

%check
/usr/bin/sepolgen-ifgen -i %{buildroot}%{_usr}/share/selinux/devel/include -o /dev/null

%define setupCmds() \
make UNK_PERMS=%5 NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%4 MLS_CATS=1024 MCS_CATS=1024 bare \
make UNK_PERMS=%5 NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%4 MLS_CATS=1024 MCS_CATS=1024  conf \
cp -f $RPM_SOURCE_DIR/modules-%1.conf  ./policy/modules.conf \
cp -f $RPM_SOURCE_DIR/booleans-%1.conf ./policy/booleans.conf \

%define moduleList() %([ -f %{_sourcedir}/modules-%{1}.conf ] && \
awk '$1 !~ "/^#/" && $2 == "=" && $3 == "module" { printf "-i %%s.pp ", $1 }' %{_sourcedir}/modules-%{1}.conf )

%define bzmoduleList() %([ -f %{_sourcedir}/modules-%{1}.conf ] && \
awk '$1 !~ "/^#/" && $2 == "=" && $3 == "module" { printf " ../%%s.pp.bz2 ", $1 }' %{_sourcedir}/modules-%{1}.conf )

%define installCmds() \
make UNK_PERMS=%5 NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%4 MLS_CATS=1024 MCS_CATS=1024 base.pp \
make validate UNK_PERMS=%5 NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%4 MLS_CATS=1024 MCS_CATS=1024 modules \
make UNK_PERMS=%5 NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} POLY=%4 MLS_CATS=1024 MCS_CATS=1024 install \
make UNK_PERMS=%5 NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} POLY=%4 MLS_CATS=1024 MCS_CATS=1024 install-appconfig \
#%{__cp} *.pp %{buildroot}/%{_usr}/share/selinux/%1/ \
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/selinux/%1/policy \
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/selinux/%1/modules/active \
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/selinux/%1/contexts/files \
touch %{buildroot}/%{_sysconfdir}/selinux/%1/modules/semanage.read.LOCK \
touch %{buildroot}/%{_sysconfdir}/selinux/%1/modules/semanage.trans.LOCK \
rm -rf %{buildroot}%{_sysconfdir}/selinux/%1/booleans \
touch %{buildroot}%{_sysconfdir}/selinux/%1/seusers \
touch %{buildroot}%{_sysconfdir}/selinux/%1/policy/policy.%{POLICYVER} \
touch %{buildroot}%{_sysconfdir}/selinux/%1/contexts/files/file_contexts \
touch %{buildroot}%{_sysconfdir}/selinux/%1/contexts/files/file_contexts.homedirs \
install -m0644 $RPM_SOURCE_DIR/securetty_types-%1 %{buildroot}%{_sysconfdir}/selinux/%1/contexts/securetty_types \
install -m0644 $RPM_SOURCE_DIR/setrans-%1.conf %{buildroot}%{_sysconfdir}/selinux/%1/setrans.conf \
echo -n > %{buildroot}%{_sysconfdir}/selinux/%1/contexts/customizable_types \
bzip2 %{buildroot}/%{_usr}/share/selinux/%1/*.pp
%nil

%define fileList() \
%defattr(-,root,root) \
%dir %{_usr}/share/selinux/%1 \
%{_usr}/share/selinux/%1/*.pp.bz2 \
%dir %{_sysconfdir}/selinux/%1 \
%config(noreplace) %{_sysconfdir}/selinux/%1/setrans.conf \
%ghost %{_sysconfdir}/selinux/%1/seusers \
%dir %{_sysconfdir}/selinux/%1/modules \
%verify(not mtime) %{_sysconfdir}/selinux/%1/modules/semanage.read.LOCK \
%verify(not mtime) %{_sysconfdir}/selinux/%1/modules/semanage.trans.LOCK \
%attr(700,root,root) %dir %{_sysconfdir}/selinux/%1/modules/active \
#%verify(not md5 size mtime) %attr(600,root,root) %config(noreplace) %{_sysconfdir}/selinux/%1/modules/active/seusers \
%dir %{_sysconfdir}/selinux/%1/policy/ \
%ghost %{_sysconfdir}/selinux/%1/policy/policy.* \
%dir %{_sysconfdir}/selinux/%1/contexts \
%config %{_sysconfdir}/selinux/%1/contexts/customizable_types \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/securetty_types \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/dbus_contexts \
%config %{_sysconfdir}/selinux/%1/contexts/x_contexts \
%config %{_sysconfdir}/selinux/%1/contexts/default_contexts \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/default_type \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/failsafe_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/initrc_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/removable_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/userhelper_context \
%dir %{_sysconfdir}/selinux/%1/contexts/files \
%ghost %{_sysconfdir}/selinux/%1/contexts/files/file_contexts \
%ghost %{_sysconfdir}/selinux/%1/contexts/files/file_contexts.homedirs \
%config %{_sysconfdir}/selinux/%1/contexts/files/media \
%dir %{_sysconfdir}/selinux/%1/contexts/users \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/root \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/guest_u \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/xguest_u \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/user_u \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/staff_u 

%define saveFileContext() \
if [ -s /etc/selinux/config ]; then \
	. %{_sysconfdir}/selinux/config; \
	FILE_CONTEXT=%{_sysconfdir}/selinux/%1/contexts/files/file_contexts; \
	if [ "${SELINUXTYPE}" == %1 -a -f ${FILE_CONTEXT} ]; then \
		cp -f ${FILE_CONTEXT} ${FILE_CONTEXT}.pre; \
	fi \
fi

%define loadminpolicy() \
tempdir=`mktemp -d /usr/share/selinux/%1/tmpXXXX`; \
( cd $tempdir; \
cp ../base.pp.bz2 ../unconfined.pp.bz2 .; \
bunzip2 *; \
semodule -b base.pp -i unconfined.pp -s %1; \
); \
rm -rf $tempdir; \

%define loadpolicy() \
tempdir=`mktemp -d /usr/share/selinux/%1/tmpXXXX`; \
( cd $tempdir; \
cp ../base.pp.bz2 %{expand:%%bzmoduleList %1} .; \
bunzip2 *; \
semodule -b base.pp %{expand:%%moduleList %1} -s %1; \
); \
rm -rf $tempdir; \

%define relabel() \
. %{_sysconfdir}/selinux/config; \
FILE_CONTEXT=%{_sysconfdir}/selinux/%1/contexts/files/file_contexts; \
selinuxenabled; \
if [ $? == 0  -a "${SELINUXTYPE}" == %1 -a -f ${FILE_CONTEXT}.pre ]; then \
	fixfiles -C ${FILE_CONTEXT}.pre restore; \
	restorecon -R /var/log /var/run 2> /dev/null; \
	rm -f ${FILE_CONTEXT}.pre; \
fi; 

%description
SELinux Reference Policy - modular.
Based off of reference policy: Checked out revision  2837.

%build

%prep 
%setup -n serefpolicy-%{version} -q
%patch -p1

%install
# Build targeted policy
%{__rm} -fR %{buildroot}
mkdir -p %{buildroot}%{_mandir}
cp -R  man/* %{buildroot}%{_mandir}
mkdir -p %{buildroot}%{_sysconfdir}/selinux
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
touch %{buildroot}%{_sysconfdir}/selinux/config
touch %{buildroot}%{_sysconfdir}/sysconfig/selinux

# Always create policy module package directories
mkdir -p %{buildroot}%{_usr}/share/selinux/{targeted,mls}/

# Install devel
make clean
%if %{BUILD_TARGETED}
# Build targeted policy
# Commented out because only targeted ref policy currently builds
%setupCmds targeted mcs n y allow
%installCmds targeted mcs n y allow
%endif

%if %{BUILD_MINIMUM}
# Build minimum policy
# Commented out because only minimum ref policy currently builds
%setupCmds minimum mcs n y allow
%installCmds minimum mcs n y allow
%endif

%if %{BUILD_MLS}
# Build mls policy
%setupCmds mls mls n y deny
%installCmds mls mls n y deny
%endif

%if %{BUILD_OLPC}
# Build olpc policy
# Commented out because only olpc ref policy currently builds
%setupCmds olpc mcs n y allow
%installCmds olpc mcs n y allow
%endif

make UNK_PERMS=allow NAME=targeted TYPE=targeted-mcs DISTRO=%{distro} DIRECT_INITRC=n MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} PKGNAME=%{name}-%{version} POLY=y MLS_CATS=1024 MCS_CATS=1024 install-headers install-docs
mkdir %{buildroot}%{_usr}/share/selinux/devel/
mv %{buildroot}%{_usr}/share/selinux/targeted/include %{buildroot}%{_usr}/share/selinux/devel/include
install -m 755 $RPM_SOURCE_DIR/policygentool %{buildroot}%{_usr}/share/selinux/devel/
install -m 644 $RPM_SOURCE_DIR/Makefile.devel %{buildroot}%{_usr}/share/selinux/devel/Makefile
install -m 644 doc/example.* %{buildroot}%{_usr}/share/selinux/devel/
install -m 644 doc/policy.* %{buildroot}%{_usr}/share/selinux/devel/
echo  "xdg-open file:///usr/share/doc/selinux-policy-%{version}/html/index.html"> %{buildroot}%{_usr}/share/selinux/devel/policyhelp
chmod +x %{buildroot}%{_usr}/share/selinux/devel/policyhelp


%clean
%{__rm} -fR %{buildroot}

%post
if [ ! -s /etc/selinux/config ]; then
	#
	#	New install so we will default to targeted policy
	#
	echo "
# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#	enforcing - SELinux security policy is enforced.
#	permissive - SELinux prints warnings instead of enforcing.
#	disabled - No SELinux policy is loaded.
SELINUX=enforcing
# SELINUXTYPE= can take one of these two values:
#	targeted - Targeted processes are protected,
#	mls - Multi Level Security protection.
SELINUXTYPE=targeted 

" > /etc/selinux/config

	ln -sf ../selinux/config /etc/sysconfig/selinux 
	restorecon /etc/selinux/config 2> /dev/null || :
else
	. /etc/selinux/config
	# if first time update booleans.local needs to be copied to sandbox
	[ -f /etc/selinux/${SELINUXTYPE}/booleans.local ] && mv /etc/selinux/${SELINUXTYPE}/booleans.local /etc/selinux/targeted/modules/active/
	[ -f /etc/selinux/${SELINUXTYPE}/seusers ] && cp -f /etc/selinux/${SELINUXTYPE}/seusers /etc/selinux/${SELINUXTYPE}/modules/active/seusers
	grep -q "^SETLOCALDEFS" /etc/selinux/config || echo -n "
">> /etc/selinux/config
fi
[ -x /usr/bin/sepolgen-ifgen ] && /usr/bin/sepolgen-ifgen 
exit 0

%postun
if [ $1 = 0 ]; then
	setenforce 0 2> /dev/null
	if [ ! -s /etc/selinux/config ]; then
		echo "SELINUX=disabled" > /etc/selinux/config
	else
		sed -i 's/^SELINUX=.*/SELINUX=disabled/g' /etc/selinux/config
	fi
fi
exit 0

%if %{BUILD_TARGETED}
%package targeted
Summary: SELinux targeted base policy
Provides: selinux-policy-base = %{version}-%{release}
Group: System/Base
Obsoletes: selinux-policy-targeted-sources < 2
Requires(pre): policycoreutils >= %{POLICYCOREUTILSVER}
Requires(pre): coreutils
Requires(pre): selinux-policy = %{version}-%{release}
Conflicts:  audispd-plugins <= 1.7.7-1

%description targeted
SELinux Reference policy targeted base module.

%pre targeted
%saveFileContext targeted

%post targeted
if [ $1 -eq 1 ]; then
%loadpolicy targeted
semanage -S targeted -i - << __eof
user -a -P user -R "unconfined_r system_r" -r s0-s0:c0.c1023 unconfined_u 
user -a -P user -R guest_r guest_u
user -a -P user -R xguest_r xguest_u 
__eof
semanage -S targeted -i - << __eof
login -m  -s unconfined_u -r s0-s0:c0.c1023 __default__
login -m  -s unconfined_u -r s0-s0:c0.c1023 root
__eof
restorecon -R /root /var/log /var/run 2> /dev/null
else
semodule -s targeted -r moilscanner 2>/dev/null
semodule -s targeted -r gamin 2>/dev/null
%loadpolicy targeted
%relabel targeted
fi
exit 0


%triggerpostun targeted -- selinux-policy-targeted < 3.2.5-9.fc9
. /etc/selinux/config
[ "${SELINUXTYPE}" != "targeted" ] && exit 0
setsebool -P use_nfs_home_dirs=1
semanage user -l | grep -s unconfined_u > /dev/null
if [ $? -eq 0 ]; then
   semanage user -m -R "unconfined_r system_r" -r s0-s0:c0.c1023 unconfined_u
else
   semanage user -a -P user -R "unconfined_r system_r" -r s0-s0:c0.c1023 unconfined_u
fi
seuser=`semanage login -l | grep __default__ | awk '{ print $2 }'`
[ "$seuser" != "unconfined_u" ]  && semanage login -m -s "unconfined_u"  -r s0-s0:c0.c1023 __default__
seuser=`semanage login -l | grep root | awk '{ print $2 }'`
[ "$seuser" == "system_u" ] && semanage login -m -s "unconfined_u"  -r s0-s0:c0.c1023 root
restorecon -R /root /etc/selinux/targeted 2> /dev/null
semodule -r qmail 2> /dev/null
exit 0

%files targeted
%config(noreplace) %{_sysconfdir}/selinux/targeted/contexts/users/unconfined_u
%fileList targeted
%endif

%if %{BUILD_MINIMUM}
%package minimum
Summary: SELinux minimum base policy
Provides: selinux-policy-base
Group: System/Base
Requires(pre): policycoreutils >= %{POLICYCOREUTILSVER}
Requires(pre): coreutils
Requires(pre): selinux-policy = %{version}-%{release}

%description minimum
SELinux Reference policy minimum base module.

%pre minimum
%saveFileContext minimum

%post minimum
if [ $1 -eq 1 ]; then
%loadminpolicy minimum
semanage -S minimum -i - << __eof
user -a -P user -R "unconfined_r system_r" -r s0-s0:c0.c1023 unconfined_u 
__eof
semanage -S minimum -i - << __eof
login -m  -s unconfined_u -r s0-s0:c0.c1023 __default__
login -m  -s unconfined_u -r s0-s0:c0.c1023 root
__eof
restorecon -R /root /var/log /var/run 2> /dev/null
else
%loadminpolicy minimum
%relabel minimum
fi
exit 0

%files minimum
%config(noreplace) %{_sysconfdir}/selinux/minimum/contexts/users/unconfined_u
%fileList minimum
%endif

%if %{BUILD_OLPC}
%package olpc 
Summary: SELinux olpc base policy
Group: System/Base
Provides: selinux-policy-base
Requires(pre): policycoreutils >= %{POLICYCOREUTILSVER}
Requires(pre): coreutils
Requires(pre): selinux-policy = %{version}-%{release}

%description olpc 
SELinux Reference policy olpc base module.

%pre olpc 
%saveFileContext olpc

%post olpc 
%loadpolicy olpc

if [ $1 -ne 1 ]; then
%relabel olpc
fi
exit 0

%files olpc
%fileList olpc

%endif

%if %{BUILD_MLS}
%package mls 
Summary: SELinux mls base policy
Group: System/Base
Provides: selinux-policy-base = %{version}-%{release}
Obsoletes: selinux-policy-mls-sources < 2
Requires: policycoreutils-newrole >= %{POLICYCOREUTILSVER} setransd
Requires(pre): policycoreutils >= %{POLICYCOREUTILSVER}
Requires(pre): coreutils
Requires(pre): selinux-policy = %{version}-%{release}

%description mls 
SELinux Reference policy mls base module.

%pre mls 
%saveFileContext mls

%post mls 
%loadpolicy mls

if [ $1 != 1 ]; then
%relabel mls
fi
exit 0

%files mls
%config(noreplace) %{_sysconfdir}/selinux/mls/contexts/users/unconfined_u
%fileList mls

%endif

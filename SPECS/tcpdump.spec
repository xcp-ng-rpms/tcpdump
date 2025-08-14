%global package_speccommit 790d1e00848366b8e1bec1adb6e12942498b56e8
%global usver 4.9.2
%global xsver 5
%global xsrel %{xsver}%{?xscount}%{?xshash}

Summary: A network traffic monitoring tool
Name: tcpdump
Epoch: 14
Version: 4.9.2
Release: %{?xsrel}%{?dist}
License: BSD with advertising
URL: http://www.tcpdump.org
Group: Applications/Internet
Requires(pre): shadow-utils
Requires: libpcap >= 14:1.5.3-10
BuildRequires: automake sharutils openssl-devel libcap-ng-devel libpcap-devel git

Source0: tcpdump-4.9.2.tar.gz
Source1: tcpslice-1.2a3.tar.gz
Patch0: 0001-icmp6-print-Reachable-Time-and-Retransmit-Time-from-.patch
Patch1: 0002-Use-getnameinfo-instead-of-gethostbyaddr.patch
Patch2: 0003-tcpslice-update-tcpslice-patch-to-1.2a3.patch
Patch3: 0004-tcpslice-remove-unneeded-include.patch
Patch4: 0005-tcpslice-don-t-test-the-pointer-but-pointee-for-NULL.patch
Patch5: 0006-Introduce-nn-option.patch
Patch6: 0007-Don-t-print-out-we-dropped-root-we-are-always-droppi.patch
Patch7: 0008-Change-P-to-Q-and-print-warning.patch
Patch8: 0009-Change-n-flag-to-nn-in-TESTonce.patch
Patch9: 0010-Expect-miliseconds-instead-of-seconds-in-icmp-captur.patch
Patch10: 0011-Disable-tests-that-require-newer-version-of-libpcap.patch
Patch11: 0012-Make-default-capture-buffer-size-bigger.patch
Patch12: 0013-Add-printing-support-for-vsockmon-devices.patch
Patch13: 0014-Disable-test-with-unsupported-link-type.patch

%define tcpslice_dir tcpslice-1.2a3

%description
Tcpdump is a command-line tool for monitoring network traffic.
Tcpdump can capture and display the packet headers on a particular
network interface or on all interfaces.  Tcpdump can display all of
the packet headers, or just the ones that match particular criteria.

Install tcpdump if you need a program to monitor network traffic.

%prep
%autosetup -a 1 -S git

%build
export CFLAGS="$RPM_OPT_FLAGS $(getconf LFS_CFLAGS) -fno-strict-aliasing -DHAVE_GETNAMEINFO"

pushd %{tcpslice_dir}
# update config.{guess,sub}
automake -a -f 2> /dev/null || :
%configure
make %{?_smp_mflags}
popd

%configure --with-crypto --with-user=tcpdump --without-smi
make %{?_smp_mflags}

%check
make check

%install
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}

pushd %{tcpslice_dir}
install -m755 tcpslice ${RPM_BUILD_ROOT}%{_sbindir}
install -m644 tcpslice.1 ${RPM_BUILD_ROOT}%{_mandir}/man8/tcpslice.8
popd

install -m755 tcpdump ${RPM_BUILD_ROOT}%{_sbindir}
install -m644 tcpdump.1 ${RPM_BUILD_ROOT}%{_mandir}/man8/tcpdump.8

# fix section numbers
sed -i 's/\(\.TH[a-zA-Z ]*\)[1-9]\(.*\)/\18\2/' \
	${RPM_BUILD_ROOT}%{_mandir}/man8/*

%pre
/usr/sbin/groupadd -g 72 tcpdump 2> /dev/null
/usr/sbin/useradd -u 72 -g 72 -s /sbin/nologin -M -r \
	-d / tcpdump 2> /dev/null
exit 0

%files
%defattr(-,root,root)
%doc LICENSE README.md CHANGES CREDITS
%{_sbindir}/tcpdump
%{_sbindir}/tcpslice
%{_mandir}/man8/tcpslice.8*
%{_mandir}/man8/tcpdump.8*

%changelog
* Fri Jan 03 2025 Deli Zhang <deli.zhang@cloud.com> - 4.9.2-5
- Add epoch 14

* Mon Oct 07 2024 Deli Zhang <deli.zhang@citrix.com> - 4.9.2-4
- First imported release


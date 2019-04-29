%define vendor_name Qlogic
%define vendor_label qlogic
%define driver_name fastlinq

%global tag 3

%if %undefined module_dir
%define module_dir updates
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Version: 8.37.30.0
Release: %{tag}%{?dist}
License: GPL

Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-qlogic-fastlinq/archive?at=8.37.30.0-3&format=tgz&prefix=driver-qlogic-fastlinq-8.37.30.0#/qlogic-fastlinq-8.37.30.0.tar.gz


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-qlogic-fastlinq/archive?at=8.37.30.0-3&format=tgz&prefix=driver-qlogic-fastlinq-8.37.30.0#/qlogic-fastlinq-8.37.30.0.tar.gz) = 0c2f9e179bf3afec3900ab35beb040c8da167f79


BuildRequires: gcc
BuildRequires: kernel-devel, git
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -S git -n driver-%{name}-%{version}

%build
%{?cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qed-%{version}/src  modules
%{?cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qede-%{version}/src modules
%{?cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qedr-%{version}/src modules
%{?cov_wrap} %{make_build} -C $(pwd)/qedf-%{version} KVER=%{kernel_version} build_pre
%{?cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qedf-%{version} modules
%{?cov_wrap} %{make_build} -C $(pwd)/qedi-%{version} KVER=%{kernel_version} build_pre
%{?cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qedi-%{version} modules

%install
%{?cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qed-%{version}/src  INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install
%{?cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qede-%{version}/src INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install
%{?cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qedr-%{version}/src INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install
%{?cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qedf-%{version} INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install
%{?cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qedi-%{version} INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install
# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x
mkdir -p %{buildroot}/lib/firmware/qed
install -m 755 $(pwd)/qed-%{version}/src/qed_init_values_zipped-*.bin %{buildroot}/lib/firmware/qed

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/firmware
/lib/modules/%{kernel_version}/*/*.ko

%changelog
* Fri Jan 25 2019 Deli Zhang <deli.zhang@citrix.com> - 8.37.30.0-3
- CP-30073: Resolve issue of duplicate copy in target build_pre of makefile

* Mon Jan 14 2019 Deli Zhang <deli.zhang@citrix.com> - 8.37.30.0-2
- CP-30073: Build all ko and include firwmware

* Thu Dec 20 2018 Deli Zhang <deli.zhang@citrix.com> - 8.37.30.0-1
- CP-30073: Upgrade fastlinq driver to version 8.37.30.0

* Wed Mar 07 2018 Simon Rowe <simon.rowe@citrix.com> - 8.30.15.0-1
- UPD-229: (QL-659) updating fastlinq version to 8.30.15.0

* Wed Jan 10 2018 Simon Rowe <simon.rowe@citrix.com> - 8.30.13.0-1
- UPD-193: (QL-655) updating fastlinq version to 8.30.13.0

* Wed Sep 20 2017 Simon Rowe <simon.rowe@citrix.com> - 8.20.4.0-1
- UPD-119: (QL-644) updating fastlinq version to 8.20.4.0


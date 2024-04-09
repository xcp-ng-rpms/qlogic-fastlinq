%global package_speccommit f76d0cf2ab6b9f9cac2b2187f29c1db8e30d203c
%global usver 8.74.0.2
%global xsver 1
%global xsrel %{xsver}%{?xscount}%{?xshash}
%global package_srccommit 8.74.0.2
%define vendor_name Qlogic
%define vendor_label qlogic
%define driver_name fastlinq
## Components in the package have different versions
%define qed_version 8.74.0.0
%define qede_version 8.74.0.0
%define qedr_version 8.74.0.0
%define qedi_version 8.74.0.0
%define qedf_version 8.74.0.2

%if %undefined module_dir
%define module_dir updates
%endif

## kernel_version will be set during build because then kernel-devel
## package installs an RPM macro which sets it. This check keeps
## rpmlint happy.
%if %undefined kernel_version
%define kernel_version dummy
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Version: 8.74.0.2
Release: %{?xsrel}%{?dist}
License: GPL
Source0: qlogic-fastlinq-8.74.0.2.tar.gz

BuildRequires: kernel-devel
%{?_cov_buildrequires}
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n %{name}-%{version}
%{?_cov_prepare}

%build
%{?_cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qed-%{qed_version}/src  modules
%{?_cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qede-%{qede_version}/src modules
%{?_cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qedr-%{qedr_version}/src modules
%{?_cov_wrap} %{make_build} -C $(pwd)/qedf-%{version} KVER=%{kernel_version} build_pre
%{?_cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qedf-%{qedf_version} modules
%{?_cov_wrap} %{make_build} -C $(pwd)/qedi-%{qedi_version} KVER=%{kernel_version} build_pre
%{?_cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qedi-%{qedi_version} modules

%install
%{?_cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qed-%{qed_version}/src  INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install
%{?_cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qede-%{qede_version}/src INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install
%{?_cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qedr-%{qedr_version}/src INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install
%{?_cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qedf-%{qedf_version} INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install
%{?_cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qedi-%{qedi_version} INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install
# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x
mkdir -p %{buildroot}/lib/firmware/qed
install -m 755 $(pwd)/qed-%{qed_version}/src/qed_init_values_zipped-*.bin %{buildroot}/lib/firmware/qed

%{?_cov_install}

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

%{?_cov_results_package}

%changelog
* Tue Jan 23 2024 Stephen Cheng <stephen.cheng@cloud.com> - 8.74.0.2-1
- CP-47038: Upgrade fastlinq driver to version 8.74.0.2

* Tue Sep 20 2022 Zhuangxuan Fei <zhuangxuan.fei@citrix.com> - 8.55.13.0-1
- CP-40164: Upgrade fastlinq driver to version 8.55.13.0

* Mon Feb 14 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 8.42.10.0-2
- CP-38416: Enable static analysis

* Wed Jan 19 2022 Deli Zhang <deli.zhang@citrix.com> - 8.42.10.0-1
- CP-37631: Upgrade fastlinq driver to version 8.42.10.0

* Wed Dec 02 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 8.37.30.0-4
- CP-35517: Fix the build for koji

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

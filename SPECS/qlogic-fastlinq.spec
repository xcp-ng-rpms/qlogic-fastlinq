%define vendor_name Qlogic
%define vendor_label qlogic
%define driver_name fastlinq

%if %undefined module_dir
%define module_dir updates
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Version: 8.30.15.0
Release: 1%{?dist}
License: GPL
Source: https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-%{name}/archive?at=%{version}&format=tgz&prefix=driver-%{name}-%{version}#/%{name}-%{version}.tar.gz

BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n driver-%{name}-%{version}

%build
%{?cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qed-%{version}/src  modules
%{?cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qede-%{version}/src modules
%install
%{?cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qed-%{version}/src INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install
%{?cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qede-%{version}/src INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install
# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%changelog
* Wed Mar 07 2018 Simon Rowe <simon.rowe@citrix.com> - 8.30.15.0-1
- UPD-229: (QL-659) updating fastlinq version to 8.30.15.0

* Wed Jan 10 2018 Simon Rowe <simon.rowe@citrix.com> - 8.30.13.0-1
- UPD-193: (QL-655) updating fastlinq version to 8.30.13.0

* Wed Sep 20 2017 Simon Rowe <simon.rowe@citrix.com> - 8.20.4.0-1
- UPD-119: (QL-644) updating fastlinq version to 8.20.4.0


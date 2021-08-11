Name:           risi-tweaks
Version:        0.1
Release:        3%{?dist}
Summary:        risiOS's Tweak Tool

License:        GPL v3
URL:            https://github.com/risiOS/risiTweaks
Source0:        %{name}-%{version}.tar.gz

BuildArch:	noarch

BuildRequires:  python
Requires:       python
Requires:	python3-gobject, python3-yaml

%description
The tweak tool for risiOS. Full alternative to GNOME Tweaks

%prep
%setup -q
%build
%install
# rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/bin/
mkdir -p $RPM_BUILD_ROOT%{_libdir}/risiOS/%{name}/tweaks
mkdir -p $RPM_BUILD_ROOT/usr/share/applications/

cp %{_builddir}/%{name}-%{version}/%{name}/risi-tweaks %{buildroot}/usr/bin
cp %{_builddir}/%{name}-%{version}/%{name}/__main__.py %{buildroot}%{_libdir}/risiOS/%{name}
cp %{_builddir}/%{name}-%{version}/%{name}/__init__.py %{buildroot}%{_libdir}/risiOS/%{name}
cp %{_builddir}/%{name}-%{version}/%{name}/RtMainWindow.py %{buildroot}%{_libdir}/risiOS/%{name}
cp %{_builddir}/%{name}-%{version}/%{name}/RtBaseWidgets.py %{buildroot}%{_libdir}/risiOS/%{name}
cp %{_builddir}/%{name}-%{version}/%{name}/RtCustomWidgets.py %{buildroot}%{_libdir}/risiOS/%{name}
cp %{_builddir}/%{name}-%{version}/%{name}/RtExtensionWidgets.py %{buildroot}%{_libdir}/risiOS/%{name}
cp %{_builddir}/%{name}-%{version}/%{name}/RtSettingsToWidget.py %{buildroot}%{_libdir}/risiOS/%{name}
cp %{_builddir}/%{name}-%{version}/%{name}/RtUtils.py %{buildroot}%{_libdir}/risiOS/%{name}
cp -r %{_builddir}/%{name}-%{version}/%{name}/tweaks %{buildroot}%{_libdir}/risiOS/%{name}

%files
# %license add-license-file-here
# %doc add-docs-here
/usr/bin/%{name}
%dir %{_libdir}/risiOS/%{name}/
%{_libdir}/risiOS/%{name}/__main__.py
%{_libdir}/risiOS/%{name}/__init__.py
%{_libdir}/risiOS/%{name}/RtMainWindow.py
%{_libdir}/risiOS/%{name}/RtBaseWidgets.py
%{_libdir}/risiOS/%{name}/RtCustomWidgets.py
%{_libdir}/risiOS/%{name}/RtExtensionWidgets.py
%{_libdir}/risiOS/%{name}/RtSettingsToWidget.py
%{_libdir}/risiOS/%{name}/RtUtils.py
%{_libdir}/risiOS/%{name}/tweaks/*/*

%changelog
* Tue Jul 13 2021 PizzaLovingNerd
- First spec file

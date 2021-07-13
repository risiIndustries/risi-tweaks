Name:           risi-tweaks
Version:        0.1
Release:        1%{?dist}
Summary:        risiOS's Tweak Tool

License:        LGPL v3
URL:            https://github.com/risiOS/risiTweaks
Source0:        risi-tweaks-%{version}.tar.xz

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
rm -rf $RPM_BUILD_ROOT

mkdir -p ${buildroot}/usr/bin/
mkdir -p ${buildroot}/usr/lib/risi-tweaks/
mkdir -p ${buildroot}/usr/share/applications/

cp %{_builddir}/risi-tweaks/risi-tweaks %{buildroot}/usr/bin
cp %{_builddir}/risi-tweaks/__main__.py %{buildroot}/usr/lib/risi-tweaks
cp %{_builddir}/risi-tweaks/RtMainWindow.py %{buildroot}/usr/lib/risi-tweaks
cp %{_builddir}/risi-tweaks/RtBaseWidgets.py %{buildroot}/usr/lib/risi-tweaks
cp %{_builddir}/risi-tweaks/RtCustomWidgets.py %{buildroot}/usr/lib/risi-tweaks
cp %{_builddir}/risi-tweaks/RtExtensionsWidgets.py %{buildroot}/usr/lib/risi-tweaks
cp %{_builddir}/risi-tweaks/RtSettingsToWidget.py %{buildroot}/usr/lib/risi-tweaks
cp %{_builddir}/risi-tweaks/RtUtils.py %{buildroot}/usr/lib/risi-tweaks
cp -R %{_builddir}/risi-tweaks/tweaks %{buildroot}/usr/lib/risi-tweaks/tweaks

%files
# %license add-license-file-here
# %doc add-docs-here
/usr/bin/risi-tweaks
/usr/lib/risi-tweaks/RtMainWindow.py
/usr/lib/risi-tweaks/RtBaseWidgets.py
/usr/lib/risi-tweaks/RtCustomWidgets.py
/usr/lib/risi-tweaks/RtExtensionsWidgets.py
/usr/lib/risi-tweaks/RtSettingsToWidget.py
/usr/lib/risi-tweaks/RtUtils.py
/usr/lib/risi-tweaks/tweaks/*

%changelog
* Tue Jul 13 2021 PizzaLovingNerd
- First spec file

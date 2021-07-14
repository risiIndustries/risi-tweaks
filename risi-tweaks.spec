Name:           risi-tweaks
Version:        0.1
Release:        1%{?dist}
Summary:        risiOS's Tweak Tool

License:        GPL v3
URL:            https://github.com/risiOS/risiTweaks
Source0:        risi-tweaks-%{version}.tar.gz

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
mkdir -p ${buildroot}%{_libdir}/risi-tweaks/
mkdir -p ${buildroot}/usr/share/applications/

cp %{_builddir}/risi-tweaks/risi-tweaks %{buildroot}/usr/bin
cp %{_builddir}/risi-tweaks/__main__.py %{buildroot}%{_libdir}/risi-tweaks
cp %{_builddir}/risi-tweaks/RtMainWindow.py %{buildroot}%{_libdir}/risi-tweaks
cp %{_builddir}/risi-tweaks/RtBaseWidgets.py %{buildroot}%{_libdir}/risi-tweaks
cp %{_builddir}/risi-tweaks/RtCustomWidgets.py %{buildroot}%{_libdir}/risi-tweaks
cp %{_builddir}/risi-tweaks/RtExtensionsWidgets.py %{buildroot}%{_libdir}/risi-tweaks
cp %{_builddir}/risi-tweaks/RtSettingsToWidget.py %{buildroot}%{_libdir}/risi-tweaks
cp %{_builddir}/risi-tweaks/RtUtils.py %{buildroot}%{_libdir}/risi-tweaks
cp -R %{_builddir}/risi-tweaks/tweaks %{buildroot}%{_libdir}/risi-tweaks/tweaks

%files
# %license add-license-file-here
# %doc add-docs-here
/usr/bin/risi-tweaks
%{_libdir}/risi-tweaks/RtMainWindow.py
%{_libdir}/risi-tweaks/RtBaseWidgets.py
%{_libdir}/risi-tweaks/RtCustomWidgets.py
%{_libdir}/risi-tweaks/RtExtensionsWidgets.py
%{_libdir}/risi-tweaks/RtSettingsToWidget.py
%{_libdir}/risi-tweaks/RtUtils.py
%{_libdir}/risi-tweaks/tweaks/*.yaml

%changelog
* Tue Jul 13 2021 PizzaLovingNerd
- First spec file

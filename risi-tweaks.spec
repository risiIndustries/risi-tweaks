Name:           risi-tweaks
Version:        0.1
Release:        8%{?dist}
Summary:        risiOS's Tweak Tool

License:        GPL v3
URL:            https://github.com/risiOS/risi-tweaks
Source0:        %{name}-%{version}.tar.gz

BuildArch:	noarch

BuildRequires:  python
Requires:       python
Requires:	python3-gobject, python3-yaml
Requires:	risi-adwaita-recolor

%description
The tweak tool for risiOS. Full alternative to GNOME Tweaks

%prep
%autosetup

%build
%install

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/risiOS/%{name}/tweaks
mkdir -p %{buildroot}%{_datadir}/applications/

cp -a %{name} %{buildroot}%{_libdir}/risiOS/
cp io.risi.Tweaks.desktop %{_datadir}/applications/io.risi.Tweaks.desktop
cp io.risi.Tweaks.svg %{_datadir}/icons/hicolor/scalable/apps/io.risi.Tweaks.svg
install -m 755 %{name}/%{name} %{buildroot}%{_bindir}

%files
# %license add-license-file-here
# %doc add-docs-here
%dir %{_libdir}/risiOS/%{name}
%{_datadir}/applications/io.risi.Tweaks.desktop
%{_datadir}/icons/hicolor/scalable/apps/io.risi.Tweaks.svg
%{_bindir}/%{name}
%{_libdir}/risiOS/%{name}/RtAppearanceWidgets.py
%{_libdir}/risiOS/%{name}/RtBaseWidgets.py
%{_libdir}/risiOS/%{name}/RtCustomWidgets.py
%{_libdir}/risiOS/%{name}/RtExtensionWidgets.py
%{_libdir}/risiOS/%{name}/RtMainWindow.py
%{_libdir}/risiOS/%{name}/RtSettingsToWidget.py
%{_libdir}/risiOS/%{name}/RtUtils.py
%{_libdir}/risiOS/%{name}/__init__.py
%{_libdir}/risiOS/%{name}/__main__.py
%{_libdir}/risiOS/%{name}/risi-tweaks
%{_libdir}/risiOS/%{name}/*/*

%changelog
* Tue Jul 13 2021 PizzaLovingNerd
- First spec file

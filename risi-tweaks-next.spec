Name:           risi-tweaks-next
Version:        0.2
Release:        13%{?dist}
Summary:        risiOS's Tweak Tool

License:        GPL v3
URL:            https://github.com/risiOS/risi-tweaks
Source0:        https://github.com/risiOS/risi-tweaks/archive/refs/heads/main.tar.gz

BuildArch:	noarch

BuildRequires:  python
Requires:       python
Requires:	    python3-gobject
Requires:       python3-yaml

Conflicts:      risi-tweaks
Provides:				risi-tweaks

%description
The tweak tool for risiOS. Full alternative to GNOME Tweaks

%prep
%autosetup -n risi-tweaks-main

%build
%install

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/risiOS/%{name}/tweaks
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/risi-script

cp -a %{name}/scripts %{buildroot}%{_datadir}/risi-script/scripts
cp -a %{name}/experiments %{buildroot}%{_datadir}/risi-script/experiments
cp -a %{name} %{buildroot}%{_libdir}/risiOS/
cp io.risi.Tweaks.desktop %{buildroot}%{_datadir}/applications/io.risi.Tweaks.desktop
cp io.risi.Tweaks.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/io.risi.Tweaks.svg
install -m 755 %{name}/%{name} %{buildroot}%{_bindir}

%files
# %license add-license-file-here
# %doc add-docs-here
%dir %{_libdir}/risiOS/%{name}
%{_datadir}/risi-script/scripts/*.risisc
%{_datadir}/risi-script/experiments/*.risisc
%{_datadir}/applications/io.risi.Tweaks.desktop
%{_datadir}/icons/hicolor/scalable/apps/io.risi.Tweaks.svg
%{_bindir}/%{name}
%{_libdir}/risiOS/%{name}/Rt*.py
%{_libdir}/risiOS/%{name}/__init__.py
%{_libdir}/risiOS/%{name}/__main__.py
%{_libdir}/risiOS/%{name}/risi-tweaks
%{_libdir}/risiOS/%{name}/*/*

%changelog
* Tue Jul 13 2021 PizzaLovingNerd
- First spec file

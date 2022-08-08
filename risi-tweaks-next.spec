Name:           risi-tweaks
Version:        0.2
Release:        15%{?dist}
Summary:        risiOS's Tweak Tool

License:        GPL v3
URL:            https://github.com/risiOS/risi-tweaks
Source0:        https://github.com/risiOS/risi-tweaks/archive/refs/heads/next.tar.gz

BuildArch:	noarch

BuildRequires:  python
Requires:       python
Requires:	    python3-gobject
Requires:       python3-yaml
Requires:		adwcolor

Conflicts:      risi-tweaks
Provides:		risi-tweaks

%description
The tweak tool for risiOS. Full alternative to GNOME Tweaks

%prep
%autosetup -n risi-tweaks-next

%build
%install

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/risiOS/risi-tweaks/tweaks
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/risi-script

cp -a risi-tweaks/scripts %{buildroot}%{_datadir}/risi-script/scripts
cp -a risi-tweaks/experiments %{buildroot}%{_datadir}/risi-script/experiments
cp -a risi-tweaks %{buildroot}%{_libdir}/risiOS/
cp io.risi.Tweaks.desktop %{buildroot}%{_datadir}/applications/io.risi.Tweaks.desktop
cp io.risi.Tweaks.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/io.risi.Tweaks.svg
install -m 755 risi-tweaks/risi-tweaks %{buildroot}%{_bindir}

%files
# %license add-license-file-here
# %doc add-docs-here
%dir %{_libdir}/risiOS/risi-tweaks
%{_datadir}/risi-script/scripts/*.risisc
%{_datadir}/risi-script/experiments/*.risisc
%{_datadir}/applications/io.risi.Tweaks.desktop
%{_datadir}/icons/hicolor/scalable/apps/io.risi.Tweaks.svg
%{_bindir}/risi-tweaks
%{_libdir}/risiOS/risi-tweaks/Rt*.py
%{_libdir}/risiOS/risi-tweaks/__init__.py
%{_libdir}/risiOS/risi-tweaks/__main__.py
%{_libdir}/risiOS/risi-tweaks/risi-tweaks
%{_libdir}/risiOS/risi-tweaks/*/*

%changelog
* Sun Aug 07 2022 PizzaLovingNerd
- Added accent colors 

* Tue Jul 13 2021 PizzaLovingNerd
- First spec file

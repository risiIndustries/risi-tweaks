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
Requires:	python3-gobject

%description
The tweak tool for risiOS. Full alternative to GNOME Tweaks

%prep
%setup -q

%build


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p ${buildroot}/usr/bin/
mkdir -p ${buildroot}/usr/lib/risi-tweaks/

cp %{_builddir}/risi-tweaks/risi-tweaks %{buildroot}/usr/bin
cp %{_builddir}/risi-tweaks/RtAppearance.py %{buildroot}/usr/lib/risi-tweaks
cp %{_builddir}/risi-tweaks/RtMain.py %{buildroot}/usr/lib/risi-tweaks
cp %{_builddir}/risi-tweaks/RtSettings.py %{buildroot}/usr/lib/risi-tweaks
cp %{_builddir}/risi-tweaks/RtUtils.py %{buildroot}/usr/lib/risi-tweaks

%files
# %license add-license-file-here
# %doc add-docs-here
/usr/bin/risi-tweaks
/usr/lib/risi-tweaks/RtAppearance.py
/usr/lib/risi-tweaks/RtMain.py
/usr/lib/risi-tweaks/RtSettings.py
/usr/lib/risi-tweaks/RtUtils.py

%changelog
* Thu Apr 29 2021 PizzaLovingNerd
- First RPM

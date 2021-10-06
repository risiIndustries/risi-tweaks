Name:           risi-tweaks
Version:        0.1
Release:        5%{?dist}
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

cp -a %{name}/risi-tweaks %{buildroot}%{_bindir}/%{name}
install -m 644 %{name} %{buildroot}%{_libdir}/risiOS/%{name}

%files
# %license add-license-file-here
# %doc add-docs-here
%dir %{_libdir}/risiOS/%{name}/
%{_bindir}/%{name}

%changelog
* Tue Jul 13 2021 PizzaLovingNerd
- First spec file

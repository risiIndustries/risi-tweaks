Name: risi-tweaks
Version: 0.1
Release: 1%{?dist}
Summary: risiOS's Tweak Tool
License: GPL v3
URL: https://github.com/risiOS/risiTweaks
Source0: risi-tweaks-%{version}.tar.gz
BuildArch: noarch
Requires: python
Requires: python3-gobject
Requires: python3-yaml

%description
The tweak tool for risiOS. Full alternative to GNOME Tweaks

%prep
%setup -n %{name}-%{version} -n %{name}-%{version}
# %setup -q

%build
python setup.py build

%install
python setup.py install --single-verison-externally-managed -01 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
rm -rf $RPM_BUILD_ROOT/usr/lib/python3.9/site-packages/risi-tweaks/risiTweaks-0.1-py3.9.egg-info

%clean
rm -rf $RPM_BUILD_ROOT

%files -f $RPM_BUILD_ROOT
%defattr(-,root,root)

%changelog
* Tue Jul 13 2021 PizzaLovingNerd
- First spec file

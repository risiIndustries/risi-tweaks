version="0.1"
dir=($pwd)
rpmdev-setuptree
tar -zcvf risi-tweaks-${version}.tar.gz risi-tweaks
mv risi-tweaks-${version}.tar.gz ~/rpmbuild/SOURCES/
cp risi-tweaks.spec ~/rpmbuild/SPECS/
cd ~/rpmbuild
rpmbuild risi-tweaks.spec
cd ${dir}
version="0.1"
dir=($pwd)
rpmdev-setuptree
cp -R risi-tweaks/ risi-tweaks-${version}/
tar -zcvf risi-tweaks-${version}.tar.gz risi-tweaks-${version}
rm -rf risi-tweaks-${version}/
mv risi-tweaks-${version}.tar.gz ~/rpmbuild/SOURCES/
cp old-risi-tweaks.spec ~/rpmbuild/SPECS/
cd ~/rpmbuild
rpmbuild -bb SPECS/old-risi-tweaks.spec
cd ${dir}
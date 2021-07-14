version="0.1"
dir=($pwd)
rpmdev-setuptree
cp -R risi-tweaks/ risi-tweaks-${version}/
tar -zcvf risi-tweaks-version="0.1".tar.gz risi-tweaks-version="0.1"
rm -rf risi-tweaks-${version}/
mv risi-tweaks-${version}.tar.gz ~/rpmbuild/SOURCES/
cp risi-tweaks.spec ~/rpmbuild/SPECS/
cd ~/rpmbuild
rpmbuild -bb SPECS/risi-tweaks.spec
cd ${dir}
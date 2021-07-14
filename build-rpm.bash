version="0.1"
dir=($pwd)
rpmdev-setuptree
tar -zcvf risi-tweaks.tar.gz risi-tweaks
mv risi-tweaks.tar.gz ~/rpmbuild/SOURCES/
cp risi-tweaks.spec ~/rpmbuild/SPECS/
cd ~/rpmbuild
rpmbuild -bb SPECS/risi-tweaks.spec
cd ${dir}
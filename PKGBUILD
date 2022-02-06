# Maintainer: Tom Meyers tom@odex.be
pkgname=repo-manager
pkgver=r2.5ed89d2
pkgrel=1
pkgdesc="Build system to easily integrate tos functionality on your system"
arch=(any)
url="https://github.com/ODEX-TOS/repo-sync"
_reponame="repo-sync"
license=('MIT')

source=(
"git+https://github.com/ODEX-TOS/repo-sync.git")
md5sums=('SKIP')
depends=('python')
makedepends=('git')

pkgver() {
  cd "$srcdir/$_reponame"
  printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}


build() {
    return 0;
}

package() {
        cd "$srcdir/$_reponame"
        python setup.py  install --root="${pkgdir}"
        install -Dm755 repo-manager.sh "$pkgdir"/usr/bin/repo-manager
}

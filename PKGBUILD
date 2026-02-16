pkgname=ragmacs-cli
pkgver=0.1.0
pkgrel=1
pkgdesc="CLI bridge to ragmacs Emacs functions via emacsclient"
arch=('any')
license=('custom:unknown')
depends=('python' 'emacs')
optdepends=('ragmacs: ragmacs.el must be available in Emacs load path')
source=(
  "ragmacs-cli"
  "ragmacs-cli.md"
)
sha256sums=(
  'SKIP'
  'SKIP'
)

package() {
  install -Dm755 "ragmacs-cli" "$pkgdir/usr/bin/ragmacs-cli"
  install -Dm644 "ragmacs-cli.md" "$pkgdir/usr/share/doc/$pkgname/README.md"
}

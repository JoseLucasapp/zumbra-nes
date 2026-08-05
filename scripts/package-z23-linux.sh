#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

zumbra_bin="${ZUMBRA_BIN:-zumbra}"
output_dir="${Z23_PACKAGE_DIR:-dist}"
arch="${Z23_ARCH:-amd64}"

rm -rf "$output_dir"
mkdir -p "$output_dir" build

"$zumbra_bin" app doctor --manifest zumbra-app.toml --target linux --arch "$arch" --format appdir --json
"$zumbra_bin" app build --manifest zumbra-app.toml --target linux --arch "$arch" --release -o build/zumbra-nes-app
ZUMBRA_DESKTOP_HEADLESS=1 ./build/zumbra-nes-app | tee build/desktop-headless.txt
grep -q '^Z23 desktop session complete$' build/desktop-headless.txt

"$zumbra_bin" app package --manifest zumbra-app.toml --target linux --arch "$arch" --format appdir --binary build/zumbra-nes-app --output-dir "$output_dir"
"$zumbra_bin" app package --manifest zumbra-app.toml --target linux --arch "$arch" --format deb --binary build/zumbra-nes-app --output-dir "$output_dir"

appdir="$output_dir/zumbra-nes-0.5.21-linux-${arch}.AppDir"
deb="$output_dir/zumbra-nes_0.5.21_${arch}.deb"
test -x "$appdir/AppRun"
test -f "$deb"
ZUMBRA_DESKTOP_HEADLESS=1 "$appdir/AppRun" | tee build/appdir-headless.txt
grep -q '^Z23 desktop session complete$' build/appdir-headless.txt
dpkg-deb --info "$deb" > build/deb-info.txt
dpkg-deb --contents "$deb" > build/deb-contents.txt
grep -q ' Version: 0.5.21' build/deb-info.txt
grep -q 'usr/bin/zumbra-nes' build/deb-contents.txt

if command -v appimagetool >/dev/null 2>&1 || [[ -x tools/appimagetool-x86_64.AppImage ]] || [[ -x tools/appimagetool ]]; then
    "$zumbra_bin" app package --manifest zumbra-app.toml --target linux --arch "$arch" --format appimage --binary build/zumbra-nes-app --output-dir "$output_dir"
else
    echo "AppImage not generated: install appimagetool or place it under tools/."
fi

(
    cd "$output_dir"
    find . -maxdepth 1 -type f ! -name 'SHA256SUMS-Z23.txt' -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS-Z23.txt
)

echo "Z23 Linux packages created in $output_dir."

#!/data/data/com.termux/files/usr/bin/bash
set -e
pkg update
pkg install -y python git
python --version
git --version
echo "تم تثبيت Python وGit فقط. هذه الخطوة لا تبني APK بحد ذاتها."

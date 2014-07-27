#!/usr/bin/env bash

cwd="$( cd "${BASH_SOURCE[0]%/*}" && pwd )"

([ "$1" != "" ] && [ -d "$cwd/$1" ]) || {
  echo "Specify a valid package directory to build from."
  exit 1
}

pkg="$cwd/$1"
mkdir -p "$pkg/SOURCES" "$pkg/OUT"
spectool -g -A "$pkg"/SPECS/* -C "$pkg"/SOURCES
rpmbuild --define "_sourcedir $pkg/SOURCES" \
         --define "_rpmdir $pkg/OUT" \
         --define "_builddir $pkg/OUT" \
         --define "_srcrpmdir $pkg/OUT" \
         --define "_speccdir $pkg/SPECS" \
         -bs "$pkg"/SPECS/*

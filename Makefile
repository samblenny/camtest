# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2024 Sam Blenny
all:
	@echo "build project bundle:    make bundle"
	@echo "sync code to CIRCUITPY:  make sync"

# This is for use by .github/workflows/buildbundle.yml GitHub Actions workflow
bundle:
	@mkdir -p build
	python3 bundle_builder.py

list:
	unzip -l 'build/*.zip'

# This is for syncing current code and libraries to CIRCUITPY drive on macOS.
# To use this on other operating systems, adjust the "/Volumes/CIRCUITPY" path
# as needed. You might also want to read the rsync manual (try "man rsync" from
# a Terminal shell on macOS or Linux).
sync: bundle
	xattr -cr build/camtest
	rsync -rcvO 'build/camtest/CircuitPython 9.x/' /Volumes/CIRCUITPY
	sync

clean:
	rm -rf build

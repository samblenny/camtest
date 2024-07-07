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

# This is for copying current code to CIRCUITPY drive
sync: bundle
	xattr -cr build
	rsync -rcvO --delete build/ /Volumes/CIRCUITPY/; sync

clean:
	rm -rf build

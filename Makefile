ANSIBLE_BRANCH = stable-2.8
DEST = ansible_vault/_vendored

vendor-vaultlib:
	# Grab the latest VaultLib code from ${ANSIBLE_BRANCH}.
	# We strip out the comment about zip() because it causes isort and black
	# to make conflicting edits. If new files are added, you must pre-create
	# their destination directories and corresponding __init__.py files manually.
	set -ex ; \
	for file in \
		ansible/__init__.py \
		ansible/release.py \
		ansible/utils/path.py \
		ansible/module_utils/_text.py \
		ansible/parsing/vault/__init__.py \
		; do \
		wget -q -O - https://raw.githubusercontent.com/ansible/ansible/${ANSIBLE_BRANCH}/lib/$${file} | \
			grep -v "# Note: on py2, this zip is izip not the list based zip() builtin" | \
			sed s'/ansible.module_utils.six/six/' | \
			sed s'/from ansible/from ansible_vault._vendored.ansible/' > ${DEST}/$${file} ; \
	done
	isort -rc ${DEST}
	black ${DEST}


.PHONY: vendor-vaultlib

.PHONY: check contract syntax test

check: contract syntax test

contract:
	python3 tools/validate.py

syntax:
	find applications examples libraries tests types -name '*.lua' -type f -print0 | xargs -0 lua tools/check_syntax.lua

test:
	lua tests/mock_host_test.lua
	lua tests/arp_test.lua

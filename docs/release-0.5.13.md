# zumbra-nes 0.5.13

Runtime desktop stability hotfix.

This release removes the custom startup/splash framebuffer path from the real SDL desktop launch because the 0.5.13 command-line ROM path still triggered `zumbra runtime error: value is not callable` after the compatibility gate passed.

It also tightens the Mapper 227 cooperative scheduler host budget so the desktop event loop is serviced more often while a multicart entry boots.

Zumbra language requirement remains 0.14.3 with the native hot-loop safe fix.

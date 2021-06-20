# The default target of this Makefile is:
all:

PKG_DEPS=gstreamer-1.0 gstreamer-app-1.0 gstreamer-video-1.0 opencv orc-0.4

prefix?=/usr/local
exec_prefix?=$(prefix)
bindir?=$(exec_prefix)/bin
libexecdir?=$(exec_prefix)/libexec
datarootdir?=$(prefix)/share
mandir?=$(datarootdir)/man
man1dir?=$(mandir)/man1
pythondir?=$(prefix)/lib/python2.7/site-packages
sysconfdir?=$(prefix)/etc

INSTALL?=install

INSTALL_CORE_FILES = \
    _sc_stbt/__init__.py \
    _sc_stbt/core_statemachine.py \
    _sc_stbt/core.py \
    _sc_stbt/stbts.py \
    _sc_stbt/zapping.py \
    _sc_stbt/standby_wakeup.py \
    _sc_stbt/menu.py \
    _sc_stbt/usb_serial.py \
    _sc_stbt/guide.py \
    _sc_stbt/video.py \
    _sc_stbt/navigation.py \
    _sc_stbt/memory_monitoring.py \
    _sc_stbt/getting_traces.py \
    _sc_stbt/pyspawn.py \
    _sc_stbt/youtube_keyboard.py \
    _sc_stbt/netflix_keyboard.py \
    _sc_stbt/amazon_keyboard.py \
    tests/__init__.py \
    tests/power_on.py \
    tests/power_off.py \
	tests/power.py \
    tests/video_tests.py \
    tests/youtube_video.py \
    tests/search_youtube.py \
    tests/search_netflix.py \
    tests/standby_wakeup.py \
    tests/netflix_video.py \
    tests/amazon_video.py \
    tests/cbeebies_video.py \
    tests/search_amazon.py \
    tests/signin_amazon.py \
    tests/test_audio.py \
    tests/goto_application.py \
    tests/quad_reset.py


all: $(INSTALL_CORE_FILES) 

install: install-core
install-core: all
	$(INSTALL) -m 0755 -d \
	    $(DESTDIR)$(bindir) \
	    $(DESTDIR)$(pythondir)/sc_stbt \
	    $(patsubst %,$(DESTDIR)$(libexecdir)/stbt/%,$(sort $(dir $(INSTALL_CORE_FILES))))

	$(INSTALL) -m 0644 \
	    sc_stbt/__init__.py \
	    $(DESTDIR)$(pythondir)/sc_stbt/

	for filename in $(INSTALL_CORE_FILES); do \
			[ -x "$$filename" ] && mode=0755 || mode=0644; \
			$(INSTALL) -m $$mode $$filename $(DESTDIR)$(libexecdir)/stbt/$$filename; \
	done

uninstall:
	rm -rf $(DESTDIR)$(pythondir)/sc_stbt
	rm -rf $(DESTDIR)$(libexecdir)/stbt/_sc_stbt



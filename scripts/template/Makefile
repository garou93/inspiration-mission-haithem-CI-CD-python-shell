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
CP?=cp

INSTALL_CORE_FILES = \
    _@PROJECT@/__init__.py\
    _@PROJECT@/toolbox.py

INSTALL_CORE_ALL_FILES = \
    _@PROJECT@

all: $(INSTALL_CORE_FILES)

install: install-core
install-core: all
	$(INSTALL) -m 0755 -d \
	    $(DESTDIR)$(bindir) \
	    $(DESTDIR)$(pythondir)/@PROJECT@ \
	    $(patsubst %,$(DESTDIR)$(libexecdir)/stbt/%,$(sort $(dir $(INSTALL_CORE_FILES))))

	$(INSTALL) -m 0644 \
	    @PROJECT@/__init__.py \
	    $(DESTDIR)$(pythondir)/@PROJECT@/

	$(CP) -Rf $(INSTALL_CORE_ALL_FILES) $(DESTDIR)$(libexecdir)/stbt/$$filename \

uninstall:
	rm -rf $(DESTDIR)$(pythondir)/@PROJECT@
	rm -rf $(DESTDIR)$(libexecdir)/stbt/_@PROJECT@

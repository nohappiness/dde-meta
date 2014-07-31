# generate debian/dde-meta-misc.triggers
TRIGGERS_FILE = debian/dde-meta-misc.triggers
gen_triggers:
	if [ -f $(TRIGGERS_FILE) ]; then rm -f $(TRIGGERS_FILE); fi
	for d in $(shell cut -d',' -f1 'dde-misc/fix_desktop_translation.conf' | sed '/^#/d' | sed 's/\"//g');do \
		echo "interest /usr/share/applications/$${d}.desktop" \
		>> $(TRIGGERS_FILE);\
		done

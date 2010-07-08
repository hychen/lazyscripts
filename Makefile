DOMAIN=lazyscripts
COPYRIGHT_YEAR=2010
PYSRC=${DOMAIN}
PODIR=${PWD}/po
POFILE=${PODIR}/${DOMAIN}.pot
FIRST AUTHOR=Hsin-Yi Chen <ossug.hychen@gmail.com>, ${COPYRIGHT_YEAR}
REV_DATE=`date '+%F %R+%Z'`
LANGUAGE_TEAM=Lazyscripts Developers <lazyscripts-dev@googlegroups.com>
PODESC=lazyscripts is a script management tool

all:
	@echo please read Makefile for more details!

update_pot:
	@echo -n "updating po file of ${DOMAIN} - "
	@pygettext -p ${PODIR} -d ${DOMAIN} ${PYSRC}
	@sed -i "s/CHARSET/utf-8/" ${POFILE}
	@sed -i "s/ENCODING/utf-8/" ${POFILE}
	@sed -i "s/YEAR ORGANIZATION/${COPYRIGHT_YEAR} Lazyscripts Developers/" ${POFILE}
	@sed -i "s/FIRST AUTHOR <EMAIL@ADDRESS>, YEAR/Hsin-Yi Chen <ossug.hychen@gmail.com>, ${COPYRIGHT_YEAR}/" ${POFILE}
	@sed -i "s/YEAR-MO-DA HO:MI+ZONE/${REV_DATE}/" ${POFILE}
	@sed -i 's/LANGUAGE <LL@li.org>/${LANGUAGE_TEAM}/' ${POFILE}
	@sed -i 's/SOME DESCRIPTIVE TITLE/${PODESC}/' ${POFILE}
	@echo done!

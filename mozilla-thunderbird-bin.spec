# TODO
# ./components/libmozgnome.so matches on libnotify.1, subpackage to -gnome
%define		realname	thunderbird
Summary:	Mozilla Thunderbird - email client
Summary(pl.UTF-8):	Mozilla Thunderbird - klient poczty
Name:		mozilla-thunderbird-bin
Version:	38.7.0
Release:	1
License:	MPL 1.1 or GPL v2+ or LGPL v2.1+
Group:		X11/Applications/Networking
Source0:	http://download.cdn.mozilla.net/pub/mozilla.org/thunderbird/releases/%{version}/linux-i686/en-US/thunderbird-%{version}.tar.bz2?/%{realname}-%{version}.tar.bz2
# Source0-md5:	b72be1325a003cfb5b1ac43184129027
Source1:	http://download.cdn.mozilla.net/pub/mozilla.org/thunderbird/releases/%{version}/linux-x86_64/en-US/thunderbird-%{version}.tar.bz2?/%{realname}64-%{version}.tar.bz2
# Source1-md5:	8fffff6de0b9655fd164820040a0d356
Source2:	%{name}.desktop
Source3:	%{name}.sh
URL:		http://www.mozilla.org/projects/thunderbird/
BuildRequires:	tar >= 1:1.15.1
Requires(post,postun):	desktop-file-utils
Requires:	mktemp
Requires:	myspell-common
Requires:	nss >= 1:3.13.0
Requires:	sqlite3 >= 3.6.22-2
Suggests:	%{name}-addon-lightning
ExclusiveArch:	i686 athlon %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# already stripped
%define		_enable_debug_packages	0

%define		nspr_caps		libnspr4.so libplc4.so libplds4.so
%define		moz_caps		libgtkembedmoz.so libmozjs.so libxpcom.so libxul.so libxpcom_core.so libmozsqlite3.so libmozalloc.so

%define		mozldap_caps	libldap60.so libldif60.so libprldap60.so libssldap60.so
%define		sqlite_caps		libsqlite3.so
# temporarily, see todo
%define		notify_caps		libnotify.so.1

%define		_noautoreqdep		%{nspr_caps}
%define		_noautoprovfiles	%{_libdir}/%{name}

# list of script capabilities (regexps) not to be used in Provides
%define     _noautoprov %{moz_caps}
# and as we don't provide them, don't require either
%define     _noautoreq  %{_noautoprov} %{notify_caps}

%description
Mozilla Thunderbird is an open-source, fast and portable email client.
Binary version from %{url}.

%description -l pl.UTF-8
Mozilla Thunderbird jest open sourcowym, szybkim i przenośnym klientem
poczty. Wersja binarna, ze strony %{url}.

%package addon-lightning
Summary:	An integrated calendar for Icedove
Summary(pl.UTF-8):	Zintegrowany kalendarz dla Icedove
License:	MPL 1.1 or GPL v2+ or LGPL v2.1+
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description addon-lightning
Lightning is an calendar extension to Mozilla Thunderbird email
client.

%description addon-lightning -l pl.UTF-8
Lightning to rozszerzenie do klienta poczty Mozilla Thunderdbird
dodające funkcjonalność kalendarza.

%prep
%setup -qcT
%ifarch %{ix86}
%{__tar} jxf %{SOURCE0} --strip-components=1
%endif
%ifarch %{x8664}
%{__tar} jxf %{SOURCE1} --strip-components=1
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name}/plugins,%{_datadir}/%{name},%{_pixmapsdir},%{_desktopdir}}

sed 's,@libdir@,%{_libdir}/%{name},' %{SOURCE3} > $RPM_BUILD_ROOT%{_bindir}/%{name}
cp -a . $RPM_BUILD_ROOT%{_libdir}/%{name}
cp -p chrome/icons/default/default48.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

# files created by register
touch $RPM_BUILD_ROOT%{_libdir}/%{name}/components/compreg.dat
touch $RPM_BUILD_ROOT%{_libdir}/%{name}/components/xpti.dat

# use system dict
%{__rm} -rv $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries
ln -s %{_datadir}/myspell $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries
#%{__rm} -rv $RPM_BUILD_ROOT%{_libdir}/%{name}/hyphenation
ln -s %{_datadir}/myspell $RPM_BUILD_ROOT%{_libdir}/%{name}/hyphenation

# move arch independant ones to datadir
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome $RPM_BUILD_ROOT%{_datadir}/%{name}/chrome
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults $RPM_BUILD_ROOT%{_datadir}/%{name}/defaults
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/icons $RPM_BUILD_ROOT%{_datadir}/%{name}/icons
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/isp $RPM_BUILD_ROOT%{_datadir}/%{name}/isp
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/searchplugins $RPM_BUILD_ROOT%{_datadir}/%{name}/searchplugins
ln -s ../../share/%{name}/chrome $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome
ln -s ../../share/%{name}/defaults $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults
ln -s ../../share/%{name}/icons $RPM_BUILD_ROOT%{_libdir}/%{name}/icons
ln -s ../../share/%{name}/isp $RPM_BUILD_ROOT%{_libdir}/%{name}/isp
ln -s ../../share/%{name}/searchplugins $RPM_BUILD_ROOT%{_libdir}/%{name}/searchplugins

# never package these
# nss
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/lib{freebl3,nss3,nssckbi,nssdbm3,nssutil3,smime3,softokn3,ssl3}.*
# nspr
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/lib{nspr4,plc4,plds4}.so
# mozldap
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/lib{ldap,ldif,prldap}60.so
grep -v 'lib\(nspr4\|plc4\|plds4\|nssutil3\|nss3\|smime3\|ssl3\|ldap60\|ldif60\|prldap60\).so' \
	dependentlibs.list > $RPM_BUILD_ROOT%{_libdir}/%{name}/dependentlibs.list

# remove update notifier, we prefer rpm packages for updating
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/update-settings.ini
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/updater
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/updater.ini
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/Throbber-small.gif
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/precomplete

# remove unecessary stuff
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/removed-files

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
# it attempts to register crashreport in $HOME/.thunderbird
# make temporary $HOME to avoid polluting home of user installing this package
# via sudo.
export HOME=$(mktemp -d)
# also TMPDIR could be pointing to sudo user's homedir
unset TMPDIR TMP || :

umask 022
%{_libdir}/%{name}/thunderbird -register

rm -rf $HOME

%postun
%update_desktop_database_postun

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins

%dir %{_libdir}/%{name}/components
%attr(755,root,root) %{_libdir}/%{name}/components/*.so
%attr(755,root,root) %{_libdir}/%{name}/components/components.manifest

%attr(755,root,root) %{_libdir}/%{name}/*.so
%attr(755,root,root) %{_libdir}/%{name}/*.sh
%attr(755,root,root) %{_libdir}/%{name}/*-bin
%attr(755,root,root) %{_libdir}/%{name}/plugin-container
%attr(755,root,root) %{_libdir}/%{name}/thunderbird

%{_libdir}/%{name}/application.ini
%{_libdir}/%{name}/blocklist.xml
%{_libdir}/%{name}/chrome.manifest
%{_libdir}/%{name}/dependentlibs.list
%{_libdir}/%{name}/omni.ja
%{_libdir}/%{name}/platform.ini

%attr(755,root,root) %{_libdir}/%{name}/crashreporter
%{_libdir}/%{name}/crashreporter.ini

%dir %{_libdir}/%{name}/extensions
%{_libdir}/%{name}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}

%dir %{_libdir}/%{name}/distribution
%dir %{_libdir}/%{name}/distribution/extensions

# symlinks
%{_libdir}/%{name}/chrome
%{_libdir}/%{name}/defaults
%{_libdir}/%{name}/dictionaries
%{_libdir}/%{name}/hyphenation
%{_libdir}/%{name}/icons
%{_libdir}/%{name}/isp
%{_libdir}/%{name}/searchplugins

%{_pixmapsdir}/*.png
%{_desktopdir}/*.desktop

# files created by register
%ghost %{_libdir}/%{name}/components/compreg.dat
%ghost %{_libdir}/%{name}/components/xpti.dat

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/chrome
%{_datadir}/%{name}/defaults
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/isp
%{_datadir}/%{name}/searchplugins

%files addon-lightning
%defattr(644,root,root,755)
%{_libdir}/%{name}/distribution/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}

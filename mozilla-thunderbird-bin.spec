Summary:	Mozilla Thunderbird - email client
Summary(pl.UTF-8):	Mozilla Thunderbird - klient poczty
Name:		mozilla-thunderbird-bin
Version:	3.1.2
Release:	0.4
License:	MPL 1.1 or GPL v2+ or LGPL v2.1+
Group:		X11/Applications/Networking
Source0:	http://releases.mozilla.org/pub/mozilla.org/thunderbird/releases/%{version}/linux-i686/en-US/thunderbird-%{version}.tar.bz2
# Source0-md5:	51f0a90315ce56dce2e8f9a8c8a487f2
Source1:	%{name}.desktop
Source2:	%{name}.sh
URL:		http://www.mozilla.org/projects/thunderbird/
Requires:	myspell-common
Requires:	sqlite3 >= 3.6.22-2
ExclusiveArch:	i686 athlon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# already stripped
%define		_enable_debug_packages	0

%define		nss_caps		libfreebl3.so libnss3.so libnssckbi.so libsmime3.so ibsoftokn3.so libssl3.so libnssutil3.so
%define		nspr_caps		libnspr4.so libplc4.so libplds4.so
%define		moz_caps		libgtkembedmoz.so libmozjs.so libxpcom.so libxul.so
%define		sqlite_caps		libsqlite3.so

%define		_noautoreqdep		libgfxpsshar.so libgkgfx.so libgtkxtbin.so libjsj.so libxpcom_compat.so libxpcom_core.so libxpistub.so
%define		_noautoprovfiles	%{_libdir}/%{name}/components

# list of script capabilities (regexps) not to be used in Provides
%define     _noautoprov %{moz_caps}
# and as we don't provide them, don't require either
%define     _noautoreq  %{_noautoprov} %{sqlite_caps}

%description
Mozilla Thunderbird is an open-source, fast and portable email client.
Binary version from %{url}.

%description -l pl.UTF-8
Mozilla Thunderbird jest open sourcowym, szybkim i przenośnym klientem
poczty. Wersja binarna, ze strony %{url}.

%prep
%setup -qc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name}/plugins,%{_datadir}/%{name},%{_pixmapsdir},%{_desktopdir}}

install -p %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/%{name}
cp -a thunderbird/* $RPM_BUILD_ROOT%{_libdir}/%{name}
cp -a thunderbird/chrome/icons/default/default48.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

# use system dict
rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries
ln -s %{_datadir}/myspell $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries

# use system sqlite
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/libsqlite3.so
ln -s /%{_lib}/libsqlite3.so.0 $RPM_BUILD_ROOT%{_libdir}/%{name}/libsqlite3.so

# move arch independant ones to datadir
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome $RPM_BUILD_ROOT%{_datadir}/%{name}/chrome
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults $RPM_BUILD_ROOT%{_datadir}/%{name}/defaults
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/greprefs $RPM_BUILD_ROOT%{_datadir}/%{name}/greprefs
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/icons $RPM_BUILD_ROOT%{_datadir}/%{name}/icons
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/isp $RPM_BUILD_ROOT%{_datadir}/%{name}/isp
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/modules $RPM_BUILD_ROOT%{_datadir}/%{name}/modules
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/res $RPM_BUILD_ROOT%{_datadir}/%{name}/res
ln -s ../../share/%{name}/chrome $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome
ln -s ../../share/%{name}/defaults $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults
ln -s ../../share/%{name}/greprefs $RPM_BUILD_ROOT%{_libdir}/%{name}/greprefs
ln -s ../../share/%{name}/icons $RPM_BUILD_ROOT%{_libdir}/%{name}/icons
ln -s ../../share/%{name}/isp $RPM_BUILD_ROOT%{_libdir}/%{name}/isp
ln -s ../../share/%{name}/modules $RPM_BUILD_ROOT%{_libdir}/%{name}/modules
ln -s ../../share/%{name}/res $RPM_BUILD_ROOT%{_libdir}/%{name}/res

# never package these
# nss
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/lib{freebl3,nss3,nssckbi,nssdbm3,nssutil3,smime3,softokn3,ssl3}.*
# nspr
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/lib{nspr4,plc4,plds4}.so
# mozldap
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/lib{ldap,ldif,prldap,ssldap}60.so

# remove unecessary stuff
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/README.txt
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/components/components.list
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/removed-files

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins

%dir %{_libdir}/%{name}/components
%attr(755,root,root) %{_libdir}/%{name}/components/*.so
%{_libdir}/%{name}/components/*.js
%{_libdir}/%{name}/components/*.xpt

%attr(755,root,root) %{_libdir}/%{name}/*.so
%attr(755,root,root) %{_libdir}/%{name}/*.sh
%attr(755,root,root) %{_libdir}/%{name}/*-bin
%attr(755,root,root) %{_libdir}/%{name}/mozilla-xremote-client
%attr(755,root,root) %{_libdir}/%{name}/thunderbird

%{_libdir}/%{name}/platform.ini
%{_libdir}/%{name}/application.ini

%attr(755,root,root) %{_libdir}/%{name}/crashreporter
%{_libdir}/%{name}/crashreporter.ini

# updater
%attr(755,root,root) %{_libdir}/%{name}/updater
%{_libdir}/%{name}/Throbber-small.gif
%{_libdir}/%{name}/updater.ini
%{_libdir}/%{name}/update.locale

%dir %{_libdir}/%{name}/extensions
%{_libdir}/%{name}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}

# symlinks
%{_libdir}/%{name}/chrome
%{_libdir}/%{name}/defaults
%{_libdir}/%{name}/dictionaries
%{_libdir}/%{name}/greprefs
%{_libdir}/%{name}/icons
%{_libdir}/%{name}/isp
%{_libdir}/%{name}/modules
%{_libdir}/%{name}/res

%{_pixmapsdir}/*.png
%{_desktopdir}/*.desktop

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/chrome
%{_datadir}/%{name}/defaults
%{_datadir}/%{name}/greprefs
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/isp
%{_datadir}/%{name}/modules
%{_datadir}/%{name}/res

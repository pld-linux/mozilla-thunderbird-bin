# TODO
# ./components/libmozgnome.so matches on libnotify.1, subpackage to -gnome
%define		realname	thunderbird
Summary:	Mozilla Thunderbird - email client
Summary(pl.UTF-8):	Mozilla Thunderbird - klient poczty
Name:		mozilla-thunderbird-bin
Version:	91.2.0
Release:	1
License:	MPL 1.1 or GPL v2+ or LGPL v2.1+
Group:		X11/Applications/Networking
Source0:	https://ftp.mozilla.org/pub/thunderbird/releases/%{version}/linux-i686/en-US/thunderbird-%{version}.tar.bz2?/%{realname}-%{version}.tar.bz2
# Source0-md5:	54b1b5e325b42b43112827cc399aef19
Source1:	https://ftp.mozilla.org/pub/thunderbird/releases/%{version}/linux-x86_64/en-US/thunderbird-%{version}.tar.bz2?/%{realname}64-%{version}.tar.bz2
# Source1-md5:	284b71ba2fd769ecb1ed939b904ef5b1
Source2:	%{name}.desktop
Source3:	%{name}.sh
URL:		http://www.mozilla.org/projects/thunderbird/
BuildRequires:	tar >= 1:1.15.1
Requires(post,postun):	desktop-file-utils
Requires:	glib2 >= 1:2.42
Requires:	glibc >= 6:2.17
Requires:	gtk+3 >= 3.14
Requires:	libstdc++ >= 6:4.8.1
Requires:	mktemp
Requires:	myspell-common
Requires:	nspr >= 1:4.32
Requires:	nss >= 1:3.68
Requires:	pango >= 1:1.22.0
Obsoletes:	mozilla-thunderbird-bin-addon-lightning < 78.0
ExclusiveArch:	i686 athlon %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# already stripped
%define		_enable_debug_packages	0

%define		nspr_caps		libnspr4.so libplc4.so libplds4.so
%define		moz_caps		libgtkembedmoz.so liblgpllibs.so libmozgtk.so libmozjs.so libmozsandbox.so libxpcom.so libxul.so libxpcom_core.so libmozsqlite3.so libmozalloc.so libmozwayland.so

%define		mozldap_caps	libldap60.so libldif60.so libprldap60.so libssldap60.so
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

ln -s %{_datadir}/myspell $RPM_BUILD_ROOT%{_libdir}/%{name}/hyphenation

# move arch independant ones to datadir
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome $RPM_BUILD_ROOT%{_datadir}/%{name}/chrome
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults $RPM_BUILD_ROOT%{_datadir}/%{name}/defaults
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/icons $RPM_BUILD_ROOT%{_datadir}/%{name}/icons
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/isp $RPM_BUILD_ROOT%{_datadir}/%{name}/isp
ln -s ../../share/%{name}/chrome $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome
ln -s ../../share/%{name}/defaults $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults
ln -s ../../share/%{name}/icons $RPM_BUILD_ROOT%{_libdir}/%{name}/icons
ln -s ../../share/%{name}/isp $RPM_BUILD_ROOT%{_libdir}/%{name}/isp

# never package these
# nss
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/lib{freeblpriv3,nss3,nssckbi,nssutil3,otr,smime3,softokn3,ssl3}.*
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

%postun
%update_desktop_database_postun

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins

%attr(755,root,root) %{_libdir}/%{name}/*.so
%attr(755,root,root) %{_libdir}/%{name}/*-bin
%attr(755,root,root) %{_libdir}/%{name}/minidump-analyzer
%attr(755,root,root) %{_libdir}/%{name}/pingsender
%attr(755,root,root) %{_libdir}/%{name}/plugin-container
%attr(755,root,root) %{_libdir}/%{name}/thunderbird

%{_libdir}/%{name}/application.ini
%{_libdir}/%{name}/dependentlibs.list
%{_libdir}/%{name}/omni.ja
%{_libdir}/%{name}/platform.ini

%attr(755,root,root) %{_libdir}/%{name}/crashreporter
%{_libdir}/%{name}/crashreporter.ini

# symlinks
%{_libdir}/%{name}/chrome
%{_libdir}/%{name}/defaults
%{_libdir}/%{name}/hyphenation
%{_libdir}/%{name}/icons
%{_libdir}/%{name}/isp

%dir %{_libdir}/%{name}/fonts
%{_libdir}/%{name}/fonts/TwemojiMozilla.ttf

%{_pixmapsdir}/*.png
%{_desktopdir}/*.desktop

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/chrome
%{_datadir}/%{name}/defaults
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/isp

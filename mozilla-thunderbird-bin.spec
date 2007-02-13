#
# TODO: directories 
#
Summary:	Mozilla Thunderbird - email client
Summary(pl.UTF-8):	Mozilla Thunderbird - klient poczty
Name:		mozilla-thunderbird-bin
Version:	0.8
Release:	0.9
License:	MPL/LGPL
Group:		X11/Applications/Networking
Source0:	http://ftp.mozilla.org/pub/mozilla.org/thunderbird/releases/%{version}/thunderbird-%{version}-i686-linux-gtk2+xft.tar.gz
# Source0-md5:	16ca6cf7b4763aa684eea26cc8b93621
Source1:	%{name}.desktop
Source2:	%{name}.sh
URL:		http://www.mozilla.org/projects/thunderbird/
Requires:	gtk+2
Requires:	freetype >= 2.1.3
Requires:	freetype < 1:2.1.8
Conflicts:	freetype = 2.1.8
Requires:	ORBit2
Requires:	libgnome
ExclusiveArch:	i686 athlon 
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_thunderbirddir		%{_libdir}/%{name}

# mozilla and firefox/thunderbird provide their own versions
%define _noautoreq		libnspr4.so libplc4.so libplds4.so liblinc.so.1
%define	_noautoreqdep		libgkgfx.so libgtkembedmoz.so libgtkxtbin.so libjsj.so libmozjs.so libxpcom.so libxpcom_compat.so libnspr4.so
%define	_noautoprovfiles	libnspr4.so libplc4.so libplds4.so

%description
Mozilla Thunderbird is an open-source, fast and portable email client.
Binary version from %{url}.

%description -l pl.UTF-8
Mozilla Thunderbird jest open sourcowym, szybkim i przenośnym klientem
poczty. 
Wersja binarna, ze strony %{url}.

%prep
%setup -q -n thunderbird

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_pixmapsdir},%{_desktopdir}}
install -d $RPM_BUILD_ROOT%{_thunderbirddir}
install -d $RPM_BUILD_ROOT%{_thunderbirddir}/plugins

install %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/mozilla-thunderbird-bin
cp -afp . $RPM_BUILD_ROOT%{_thunderbirddir}
install icons/mozicon50.xpm $RPM_BUILD_ROOT%{_pixmapsdir}/mozilla-thunderbird-bin.xpm
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/mozilla-thunderbird-bin.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mozilla-thunderbird-bin
%dir %{_thunderbirddir}
%{_thunderbirddir}/res
%dir %{_thunderbirddir}/components
%attr(755,root,root) %{_thunderbirddir}/components/*.so
%{_thunderbirddir}/components/*.js
%{_thunderbirddir}/components/*.xpt
%{_thunderbirddir}/components/xpti.dat
%dir %{_thunderbirddir}/components/talkback
%{_thunderbirddir}/components/talkback/*.ad
%{_thunderbirddir}/components/talkback/*.ini
%attr(755,root,root) %{_thunderbirddir}/components/talkback/*.so
%attr(755,root,root) %{_thunderbirddir}/components/talkback/talkback
%dir %{_thunderbirddir}/components/myspell
%{_thunderbirddir}/components/myspell/*
%{_thunderbirddir}/defaults
%{_thunderbirddir}/greprefs
%{_thunderbirddir}/icons
%{_thunderbirddir}/plugins
%attr(755,root,root) %{_thunderbirddir}/*.so
%{_thunderbirddir}/*.chk
%attr(755,root,root) %{_thunderbirddir}/*.sh
%attr(755,root,root) %{_thunderbirddir}/*-bin
%attr(755,root,root) %{_thunderbirddir}/mozilla-xremote-client
%attr(755,root,root) %{_thunderbirddir}/thunderbird
%{_thunderbirddir}/*.txt
%{_thunderbirddir}/x*
%{_thunderbirddir}/components.ini
%dir %{_thunderbirddir}/chrome
%{_thunderbirddir}/chrome/en-unix.jar
%{_thunderbirddir}/chrome/en-US-mail.jar
%{_thunderbirddir}/chrome/mail.jar
%{_thunderbirddir}/chrome/help.jar
%{_thunderbirddir}/chrome/qute.jar
%{_thunderbirddir}/chrome/newsblog.jar
%{_thunderbirddir}/chrome/chrome.rdf
%{_thunderbirddir}/chrome/icons
%{_thunderbirddir}/chrome/offline.jar
%{_thunderbirddir}/chrome/*.txt
%{_pixmapsdir}/*
%{_desktopdir}/*.desktop
%dir %{_thunderbirddir}/init.d
%{_thunderbirddir}/init.d/*
%dir %{_thunderbirddir}/extensions
%{_thunderbirddir}/extensions/*

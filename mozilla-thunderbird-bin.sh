#!/bin/sh
# based on script by (c) vip at linux.pl, wolf at pld-linux.org

MOZILLA_FIVE_HOME=/usr/lib/mozilla-thunderbird-bin
if [ "$1" == "-remote" ]; then
	$MOZILLA_FIVE_HOME/thunderbird "$@"
else
	PING=`$MOZILLA_FIVE_HOME/thunderbird -remote 'ping()' 2>&1 >/dev/null`
	if [ -n "$PING" ]; then
		$MOZILLA_FIVE_HOME/thunderbird "$@"
	else
		case "$1" in
		    -compose|-editor)
			$MOZILLA_FIVE_HOME/thunderbird -remote 'xfeDoCommand (composeMessage)'
			;;
		    *)
			$MOZILLA_FIVE_HOME/thunderbird -remote 'xfeDoCommand (openInbox)'
			;;
		esac
	fi
fi

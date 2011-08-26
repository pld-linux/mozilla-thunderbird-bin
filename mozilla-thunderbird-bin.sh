#!/bin/sh
# based on script by (c) vip at linux.pl, wolf at pld-linux.org

app=@libdir@/thunderbird

if [ "$1" = "-remote" ]; then
	exec "$app" "$@"
fi

PING=$("$app" -remote 'ping()' 2>&1 >/dev/null)
if [ -n "$PING" ]; then
	exec "$app" "$@"
fi

case "$1" in
-compose|-editor)
	exec "$app" -remote 'xfeDoCommand (composeMessage)'
	;;
*)
	exec "$app" -remote 'xfeDoCommand (openInbox)'
	;;
esac

#!/bin/sh
# Dev deploy: copy the skin to the Kodi box over SSH and reload it.
#   scripts/deploy.sh            (KODI_HOST defaults to 192.168.1.175)
set -eu
HOST="${KODI_HOST:-192.168.1.175}"
ID=skin.estuary.lg
DEST=/storage/.kodi/addons/$ID
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

COPYFILE_DISABLE=1 tar -C "$ROOT" -cf - \
  --exclude ./.git --exclude ./.github --exclude ./dist --exclude ./scripts --exclude ./tools --exclude .DS_Store . |
  ssh "root@$HOST" "set -e; rm -rf $DEST.new; mkdir -p $DEST.new; tar -xf - -C $DEST.new;
    rm -rf $DEST.old; [ -d $DEST ] && mv $DEST $DEST.old; mv $DEST.new $DEST; rm -rf $DEST.old;
    kodi-send -a 'UpdateLocalAddons' >/dev/null; sleep 3; kodi-send -a 'ReloadSkin()' >/dev/null"
echo "deployed $ID to $HOST and reloaded the skin"

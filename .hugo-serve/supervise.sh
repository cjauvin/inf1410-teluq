#!/bin/sh
# Garde un `hugo server` en vie sur le port 1314, détaché de tout terminal.
#
# Le surveillant de fichiers de Hugo s'est révélé peu fiable en session longue
# (il cesse parfois de réagir, et il ne reprend pas les changements de
# hugo.toml), et le serveur a fini par mourir sans laisser de trace. D'où cette
# boucle : elle le relance, et garde le journal pour qu'un prochain plantage
# soit diagnosticable.
cd "$(dirname "$0")/.." || exit 1
while true; do
  echo "=== démarrage $(date '+%F %T') ==="
  hugo server --disableFastRender --noHTTPCache --port 1314
  echo "=== arrêt (code $?) $(date '+%F %T') ==="
  sleep 2
done

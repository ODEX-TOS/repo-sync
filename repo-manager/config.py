
# The default repo ring level to use, in case none was given
RING_LEVEL=2

# ring level 1 is repo.odex.be and should never change
VALID_RING_LEVELS = [2, 3]

# how often a given ring should sync
RING_LEVEL_TIMINGS={
    2: 3600,
    3: 86400
}

# This is the root server, eg ring 1 repository
ROOT_SERVER="https://repo.odex.be"

# The database file to download
DB_NAME="tos.db.tar.gz"

# Default settings for the repo deployment
DEPLOY_TYPE="docker"
DEPLOY_BACKEND="nginx"
DEPLOY_DOMAIN="repo.example.com"

DEPLOY_PATH="/usr/share/nginx/html"
DOCKER_COMPOSE_DIR="/opt/tos/repo"

RING_DATA_URL="https://raw.githubusercontent.com/ODEX-TOS/repo-sync/master/rings/"

DATA_STORAGE="/var/cache/tos-repo/persist.json"


ARCH="x86_64"
COMPRESSION="zst"
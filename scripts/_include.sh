# include this to load server.properties and define some variables

# read server.properties file, must be called when BASE_DIR is set
function read_server_properties() {
    if [ -z "${BASE_DIR:-}" ]; then
        echo "BASE_DIR is not set"
        exit 1
    fi
    if [ ! -f "${BASE_DIR}/server.properties" ]; then
        echo "server.properties file not found!"
        exit 1
    fi
    . "${BASE_DIR}/server.properties"
    if [ -z "${REMOTE_SERVER:-}" ]; then
        echo "REMOTE_SERVER is not set"
        exit 1
    fi
    if [ -z "${REMOTE_USER:-}" ]; then
        echo "REMOTE_USER is not set"
        exit 1
    fi
}

function ssh_options() {
  echo "
       -o BatchMode=yes \
       -o ConnectionAttempts=3 \
       -o ConnectTimeout=12 \
       -o PreferredAuthentications=publickey \
       -o StrictHostKeyChecking=no \
       -o UserKnownHostsFile=/dev/null \
       -o ExitOnForwardFailure=yes \
       -o ServerAliveInterval=60 \
       -o LogLevel=ERROR
       "
}

# execute command on remote server
function _ssh() {
  # shellcheck disable=SC2046,SC2029
  ssh $(ssh_options) "${REMOTE_USER}@${REMOTE_SERVER}" "$@"
}

# copy files to remote server
function _scp() {
  # shellcheck disable=SC2046
  scp $(ssh_options) "$@" "${REMOTE_USER}@${REMOTE_SERVER}:"
}

## log message with time stamp
function log() {
  echo -e '\033[0;32m'"$(ts)" "${*}"'\033[0m'
}

## write time stamp
function ts () {
  date +"%Y-%m-%d %T"
}


# initialize variables
read_server_properties
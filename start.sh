mode="${1-all}"
action="${2-up}"
args="${@:3}"

docker compose -f docker-compose-${mode}.yml $action $args

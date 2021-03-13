#!/usr/bin/env bash

# ./recycle_swarm.sh [-h]
#
# Removes all descriptr services and the node_modules volume
# then rebuilds the images, pushes, and deploys the stack.

# set -e

f_print() { # {{{
    local v_op="$1"
    local v_msg="$2"

    case "$v_op" in
        '-w')
            : "[WARN]"
            ;;
        '-e')
            : "[ERR]"
            ;;
        '-i')
            : "[INFO]"
            ;;
        *)
            v_msg="$v_op"
            : "[INFO]"
            ;;
    esac

    local v_out="$_"
    printf "%s\t%s\n" "$v_out" "$v_msg"
} # }}}

f_usage() { # {{{
    echo "./recycle_swarm.sh [-h]"
    echo "Removes all descriptr services and the node_modules volume" \
        "then rebuilds the images, pushes, and deploys the stack."
} # }}}

while getopts "h" options; do
    case "$options" in
        h)
            f_usage
            exit 0
            ;;
        *)
            f_print -e "Unknown option. Ignoring."
            ;;
    esac
done

f_print "Removing docker services"
docker service rm \
    descriptr_stack_descriptr_api \
    descriptr_stack_descriptr_nginx_load_balancer \
    descriptr_stack_descriptr_web

f_print "Waiting for clean removal (15)"
sleep 15
f_print "Removing node_modules volume"
docker volume rm descriptr_stack_descriptr_web-node_modules

f_print "Rebuilding images"
docker-compose --verbose -f docker-compose-swarm.dev.yml build
f_print "Pushing"
docker-compose --verbose -f docker-compose-swarm.dev.yml push
f_print "Deploy swarm"
docker stack deploy --compose-file=docker-compose-swarm.dev.yml descriptr_stack

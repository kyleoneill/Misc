#!/bin/bash
DESK="/mnt/c/Users/kyleo/Desktop/$2"
HOME="./$2"

if ([ ! "$1" == -f ] && [ ! "$1" == -t ]) || [ -z "$1" ]; then
	echo "Missing flag. Use -f to transfer from desktop and -t to transfer to desktop."
fi

if [ "$1" == -f ]; then
	if [ ! -f "$DESK" ]; then
		echo "File $2 does not exist on the desktop."
		exit
	fi
	cp "$DESK" "$HOME"
	echo "Moved $2 to home directory."
elif [ "$1" == -t ]; then
	if [ ! -f "$HOME" ]; then
		echo "File $2 does not exist in the home directory."
		exit
	fi
	cp "$HOME" "$DESK"
	echo "Moved $2 to desktop."
fi
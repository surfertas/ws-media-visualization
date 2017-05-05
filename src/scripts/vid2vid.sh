#! /usr/bin/env bash
# date: 5/5/2017
# author: Tasuku Miura

## default settings
# file to convert
ifile=input.mp4
# name of output file
ofname=output
# video format type
vidtype=mov

function usage_exit () {
  echo "Usage: $0 [-h] [-i inputfile] [-o filename]"
  echo ""
  echo "DESCRIPTION:"
  echo "  Convert avi file to mp4 and save to ${ofile}"
  echo ""
  echo "OPTIONS:"
  echo "  -i ifile   input file(default: ${ifile})"
  echo "  -o ofname  output file name(default: ${ofile})"
  echo "  -t vidtype video type(default: ${vidtype}"
  echo ""
  exit 1
}

## parse options
while getopts hi:o:t: OPT
do
  case ${OPT} in
    h) usage_exit
      ;;
    i) ifile=${OPTARG}
      ;;
    o) ofname=${OPTARG}
      ;;
    t) vidtype=${OPTARG}
      ;;
    *) echo "Unknown option (${OPT})"
      usage_exit
      ;;
  esac
done

avconv -i ${ifile} -c:v libx264 -c:a copy ${ofname}.${vidtype}
rm ${ifile}

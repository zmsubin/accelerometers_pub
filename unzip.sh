#!/bin/sh
for zip in */*.zip
do
  dirname=`echo $zip | sed 's/\.zip$//'`
  if mkdir "$dirname" #-p "$dirname"
  then
    if cd "$dirname"
    then
      echo "$dirname"
      unzip ../../"$zip"
      cd ../..
      # rm -f $zip # Uncomment to delete the original zip file
    else
      echo "Could not unpack $zip - cd failed"
    fi
  else
    echo "Could not unpack $zip - mkdir failed"
  fi
done

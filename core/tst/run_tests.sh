#!/bin/sh

for file in ./*.php ; do
  phpunit $file
done
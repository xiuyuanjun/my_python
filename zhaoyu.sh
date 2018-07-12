#!/usr/bin/env bash

for f in `ls *anhui_chenggong.csv`;do cat ${f} >> anhui_chenggong.csv ;done
for f in `ls *anhui_weizhi.csv`;do cat ${f} >> anhui_weizhi.csv ;done
for f in `ls *qita_chenggong.csv`;do cat ${f} >> qita_chenggong.csv ;done
for f in `ls *qita_weizhi.csv`;do cat ${f} >> qita_weizhi.csv ;done
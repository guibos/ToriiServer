#!/usr/bin/env bash
mpv --http-header-fields='Cookie: account="2|1:0|10:1560683763|4:account|44:eyJpZCI6IDEsICJzZXNzaW9uX2FjdGl2ZSI6IDAuMH0=|c51acc9f19e6f5687f174c649c90ef0ce4b80697cbefcd58866640f7b8bda151";' http://localhost:8888/library/file/a.mp4
mpv --http-header-fields='Cookie: account="2|1:0|10:0010683763|4:account|44:eyJpZCI6IDEsICJzZXNzaW9uX2FjdGl2ZSI6IDAuMH0=|c51acc9f19e6f5687f174c649c90ef0ce4b80697cbefcd58866640f7b8bda151";' http://localhost:8888/library/file/a.mp4

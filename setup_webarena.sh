#!/bin/bash

conda activate webarena

base_url="http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com"

declare -A websites=(
  ["SHOPPING"]=7770
  ["SHOPPING_ADMIN"]=7780
  ["REDDIT"]=9999
  ["GITLAB"]=8023
  ["MAP"]=3000
  ["WIKIPEDIA"]=8888
  ["HOMEPAGE"]=4399
)

for name in "${!websites[@]}"; do
  port="${websites[$name]}"
  export "$name=${base_url}:${port}"
  export "WA_${name}=${base_url}:${port}"
done

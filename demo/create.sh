#!/bin/bash

# Define variables
bootstrap_server="my-cluster-kafka-bootstrap:9092"
prefix="my-topic-"
num_topics=1000

topics=()
for i in $(seq 1 $num_topics)
do
  topic="${prefix}${i}"
  topics+=("$topic")
done

# Create consumer group for each topic
for topic in "${topics[@]}"
do
  ./kafka-topics.sh --bootstrap-server $bootstrap_server --create --topic $topic --if-not-exists
done

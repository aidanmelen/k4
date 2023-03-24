# K4

K4 is a terminal based UI to interact with your Kafka clusters.

## Roadmap

kafka_wrapper

- [ ] acl
- [x] broker
- [x] test broker
- [ ] consume
- [x] consumer groups/offsets
- [x] test consumer groups/offsets
- [ ] partition
- [ ] producer
- [x] topic
- [x] test topic

k4

- [ ] ~/.config/k4config
- [ ] 10 bit custom colors
- [x] windows
    - [x] command input
    - [x] scrolling - https://github.com/mingrammer/python-curses-scroll-example
    - [x] resizing
- [x] screen
- [ ] screen manager
- [ ] content row edit
- [ ] content row describe
- [x] poc edit ini config using default terminal editor. see examples/kafka_wrapper/topics.py


## Wish List

- producer
- consumer
- schema registry
- kafka connect
- query JMX metrics for and display to users. disk size, bytes-in, bytes-out, etc.
    - https://github.com/dgildeh/JMXQuery/tree/master/python

## Install

```bash
pip install k4
```

## Examples

```
TODO
```

## License

[Apache 2.0 License - aidanmelen/k4](https://github.com/aidanmelen/k4/blob/main/README.md)
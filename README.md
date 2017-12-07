# convert_ts
Generic Timestamp Converter

# Benchmarks

## Considerations

Python 2.7.10 and Pypy 5.9.0 were used. Pypy used the following the options: `--jit vec=1 --jit vec_all=1`

Also used the following `os.environ['TZ'] = 'GMT'` which oddly boosts speed by a lot. For example, from 95.6Klines/s to 129Klines/s.

![Python 2.7.10 vs. Pypy 5.9.0 performance Comparison of the program](https://github.com/carlosvega/convert_ts/raw/master/bench.png)

### Only one timestamp

```Bash
yes "2017/12/06 22:46:53;2017/12/06 22:46:53;2017/12/06 22:46:53;2017/12/06 22:46:53;2017/12/06 22:46:53" | python convert_ts.py -t 0 -f "%Y/%m/%d %H:%M:%S" | pv -l | head -2000000 > /dev/null 
```

```Bash
yes "2017/12/06 22:46:53;2017/12/06 22:46:53;2017/12/06 22:46:53;2017/12/06 22:46:53;2017/12/06 22:46:53" | pypy --jit vec=1 --jit vec_all=1 convert_ts.py -t 0 -f "%Y/%m/%d %H:%M:%S" | pv -l | head -2000000 > /dev/null 
```

### 5 Timestamps

```Bash
yes "2017/12/06 22:46:53;2017/12/06 22:46:53;2017/12/06 22:46:53;2017/12/06 22:46:53;2017/12/06 22:46:53" | python convert_ts.py -t 0 1 2 3 4 -f "%Y/%m/%d %H:%M:%S" | pv -l | head -2000000 > /dev/null 
```

```Bash
yes "2017/12/06 22:46:53;2017/12/06 22:46:53;2017/12/06 22:46:53;2017/12/06 22:46:53;2017/12/06 22:46:53" | pypy --jit vec=1 --jit vec_all=1 convert_ts.py -t 0 1 2 3 4 -f "%Y/%m/%d %H:%M:%S" | pv -l | head -2000000 > /dev/null 
```

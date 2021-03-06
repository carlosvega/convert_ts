# convert_ts
Generic Timestamp Converter

## Usage

* Without any additional option it converts the first column from format `%d/%m/%Y:%H.%M.%S` to seconds since epoch and prints the rest of columns as the original output.
* Default input is stdin. Use -i to set a filename.
* Default output is stdout. Use -o to set a filename.
* If there are more timestamp columns, use -t to specify them.
* If the timestamp can have multiple formats, use -f to specify a list of them between double quotes.
* Keep in mind that these options affect the performance.
* The default separator is the semicolon. For changing it, use the option -s.
* If you want to exclude lines based on the timestamp, use --start and --end to specify the interval (in seconds since epoch).
* If there are multiple timestamps columns, specify the main timestamp using the option --main_ts.
* In order to set which columns to exclude or include, use options --exclude and --include.
* For printing milliseconds since epoch instead of seconds, use --ms.

## Timestamp Format

It uses the format from [Python's strptime function](https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior).

| Directive	| Meaning | 
| --- | --- |
|%a | Weekday as locale’s abbreviated name. |
|%A | Weekday as locale’s full name. |
|%w | Weekday as a decimal number, where 0 is Sunday and 6 is Saturday. |
|%d | Day of the month as a zero-padded decimal number. |
|%b | Month as locale’s abbreviated name. |
|%B | Month as locale’s full name. |
|%m | Month as a zero-padded decimal number. |
|%y | Year without century as a zero-padded decimal number. |
|%Y | Year with century as a decimal number. |
|%H | Hour (24-hour clock) as a zero-padded decimal number. |
|%I | Hour (12-hour clock) as a zero-padded decimal number. |
|%p | Locale’s equivalent of either AM or PM. |	AM, PM (en_US); |
|%M | Minute as a zero-padded decimal number. |
|%S | Second as a zero-padded decimal number. |
|%f | Microsecond as a decimal number, zero-padded on the left. |
|%j | Day of the year as a zero-padded decimal number.	|
|%U | Week number of the year (Sunday as the first day of the week) as a zero padded decimal number. All days in a new year preceding the first Sunday are considered to be in week 0. |
|%W | Week number of the year (Monday as the first day of the week) as a decimal number. All days in a new year preceding the first Monday are considered to be in week 0. |
|%c | Locale’s appropriate date and time representation. |
|%x | Locale’s appropriate date representation. |
|%X | Locale’s appropriate time representation.	|
|%% | A literal '%' character. |


## Limitations

%z [is not available](https://bugs.python.org/issue17342
) for function `datetime.strptime` in Python 2.x :-( 
I plan to port this code to Python 3. I want to code it purely on Python in order to execute it with pypy.

# Benchmarks

## Considerations

Python 2.7.10 and Pypy 5.9.0 were used. 
Pypy used the following options: `--jit vec=1 --jit vec_all=1`.
Also used the following trick which oddly boosts speed by a lot. `os.environ['TZ'] = 'GMT'` For example, from 95.6Klines/s to 129Klines/s.

![Python 2.7.10 vs. Pypy 5.9.0 performance Comparison of the program](https://github.com/carlosvega/convert_ts/raw/master/bench.png)

## Execution line of the benchmarks

*Change python with pypy or python3 accordingly* 

### Only one timestamp

```Bash
yes "2017/12/06 22:46:53;2017/12/06 22:46:53;2017/12/06 22:46:53;2017/12/06 22:46:53;2017/12/06 22:46:53" | python convert_ts.py -t 0 -f "%Y/%m/%d %H:%M:%S" | pv -l | head -2000000 > /dev/null 
```

### 5 Timestamps

```Bash
yes "2017/12/06 22:46:53;2017/12/06 22:46:53;2017/12/06 22:46:53;2017/12/06 22:46:53;2017/12/06 22:46:53" | python convert_ts.py -t 0 1 2 3 4 -f "%Y/%m/%d %H:%M:%S" | pv -l | head -2000000 > /dev/null 
```


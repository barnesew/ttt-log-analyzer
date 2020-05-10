# TTT Log Analyzer

A simple script for parsing the console output from a TTT game.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

* Python 3.7+

### Installing

Clone the repository to your machine:

```
git clone https://github.com/barnesew/ttt-log-analyzer.git
```

Make sure you have at least Python 3.7 installed on your system and that the following command is in your path:

```
python -V
```

## Analyzing Logs

To analyze console logs from a TTT game, save the console output to a file such as console.txt.
You'll then want to edit the INPUT_FILE variable in the python ttt_log_analyzer.py:

```python
INPUT_FILE = "console.txt"
```

After that, execute the following command from terminal to print out the results to console:

```
python ttt_log_analyzer.py
```

## Authors

* **Evan Barnes**

See also the list of [contributors](https://github.com/barnesew/ttt-log-analyzer/graphs/contributors) who participated in this project.

## License

This project is licensed under the Apache-2.0 License - see the [LICENSE.md](LICENSE.md) file for details.

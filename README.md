# Instagram Analyzer
Analyze instagram social networks with visualizations.

## How to use

- Install packages: `pip install -r requirements.txt`
- In your `.envfile put:
```
IG_USERNAME=...
IG_PASSWORD=...
ANALYZE_DEPTH=2
MAX_FOLLOWERS=1000
```
- Run `load_network.py`. This may take a while. A file `followings.json` will be generated.
- Run `analyzer.py`. A file `edges.csv` will be generated.
- `edges.csv` can be imported in a software like [Gephi](https://gephi.org)
- [Gephi tutorial](https://www.youtube.com/watch?v=HJ4Hcq3YX4k)
- for labels copy in node table the id values to Label values
- let OpenOrd run as algorithm and then Expand mutliple times
- change text and node size at will etc for better understanding of the network

![](imgs/gephi.png)

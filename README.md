# Terse Normal Form

# Install dependencies

```
pip install poetry

```

```
poetry install

```

## Benchmark format 🛠️

```
Initial Formula
formula

Safety Formula
formula

```

## Benchmark example 🚀

Follwing safety formula:

```
G((p_e & s & Xs) | (-s & XXs) | (-p_e & -s & XXXs)) 
```

as input format:

```
Initial Formula
True

Safety Formula
(p_e & s & Xs) | (-s & XXs) | (-p_e & -s & XXXs)

```

### Run script format 📋

```
python3 main.py benchmarkFile.txt

```
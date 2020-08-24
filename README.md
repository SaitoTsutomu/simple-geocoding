# Simple geocoding

## Install & Setting

- Download latest.csv from https://geolonia.github.io/japanese-addresses/ .

```
pip install simple-geocoding
python -c '__import__("simple_geocoding").Geocoding("/path/to/latest.csv")'
```

## Usage

```
$ simple-geocoding 東京都千代田区丸の内一丁目
(35.68156, 139.767201)

$ simple-geocoding 35.68156 139.7672
東京都千代田区丸の内一丁目
```

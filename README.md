ptt-crawler
===========

## `pip` 安裝 package

```bash
$ make pip install [package name]
```

跟開發相關的 package 加到 `requirements-dev.txt`，其他加到 `requirements.txt`

## 執行 container 裡的 Python

```bash
$ make python [file]
```

## 進入 container

```bash
$ make bash
```

## Coding style

[flake8](https://pypi.python.org/pypi/flake8/)

### 檢查 Coding style

```bash
$ make lint
```

ptt-crawler
===========

Python 版本: `2.6`, `2.7`, `3.x`

```python
from ptt_crawler import Board

board = Board("Gossiping")

for article in board:
    print(article["meta"]["title"])
```

## API

### `Board`

#### `#get_data(path)`

使用網頁位置取得頁面資料，`ptt-crawler` 會從 `path` 來判斷該如何解析頁面，像是 `/bbs/mobile-game/index.html` 會回傳文章列表，`/bbs/mobile-game/M.1419858662.A.F95.html` 會回傳單一文章資料。

#### `#reset()`

重設 iterator

## SSL

發 Request 的時候有可能會出錯，這是後可以用 `verify` 這個參數來忽略 SSL 驗證

```python
board = Board("Gossiping", verify=False)
```

## 開發

### `pip` 安裝 package

```bash
$ make pip install [package name]
```

跟開發相關的 package 加到 `requirements-dev.txt`，其他加到 `requirements.txt`

### 執行 container 裡的 Python

```bash
$ make python [file]
```

### 進入 container

```bash
$ make bash
```

### Coding style

[flake8](https://pypi.python.org/pypi/flake8/)

#### 檢查 Coding style

```bash
$ make lint
```

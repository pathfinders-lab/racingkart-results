# racingkart-results

Optuna MPC チューニング結果のダッシュボード（GitHub Pages）。

- `studies/*.json` は racingkart-analysis の `publish_results.py` が push する。
- push をトリガに GitHub Actions が `render/build_site.py` で HTML を生成し Pages にデプロイする。
- HTML はリポにコミットされない（Actions の artifact デプロイ）。

## 開発

```bash
make install   # uv sync
make test      # uv run pytest
make build     # render/out/ にローカル生成
```

# pj_random_object

ランダムオブジェクトに関する研究をまとめるための作業リポジトリです。
研究テーマごとにディレクトリを分け、テーマに依存しない勉強メモは `notes/` に置きます。

## Directory Layout

- `topics/`: 研究テーマごとの作業場所。新しいテーマは `make topic TOPIC=<theme>` で作ります。
- `notes/`: 論文・本・技術メモなど、特定の研究テーマに閉じない勉強メモ。
- `papers/`: ランダムオブジェクト関連の PDF 文献置き場。
- `shared/`: 複数テーマで再利用する小さな道具、共通メモ、参考文献断片など。

## Commands

```sh
make
make topic TOPIC=random_sets
make note TITLE=random_closed_sets
make papers
```

- `make`: 利用できるコマンドを表示します。
- `make topic TOPIC=<theme>`: `topics/_template/` から新しい研究テーマを作ります。
- `make note TITLE=<short_title>`: `notes/YYYY-MM-DD_<short_title>.md` を作ります。
- `make papers`: `papers/` にある PDF 文献を一覧表示します。

## Topic Layout

各テーマは原則として次の構成にします。

```text
topics/<theme>/
  README.md
  code/
    python/
    R/
    julia/
  data/
  output/
  manuscript/
  slides/
```

- `README.md`: 研究目的、主要な問い、現在の作業状態、再現手順。
- `code/`: 言語別の実験・シミュレーション・推定コード。
- `data/`: 小さい入力データやデータ生成メモ。大きいデータは原則として Git 管理しません。
- `output/`: 図表・中間結果・ログ。再生成できるものは必要に応じて Git 管理から外します。
- `manuscript/`: 論文・ノート本文。
- `slides/`: 報告資料。

## Naming

- テーマ名は `snake_case` を基本にします。
- 迷ったら、方法名よりも研究対象や問いが残る名前にします。
- テーマ横断の勉強メモは `notes/YYYY-MM-DD_short_title.md` にします。
- PDF は原則として `papers/<paper title>.pdf` に置き、個別テーマで使う読みメモは `notes/` か `topics/<theme>/` に書きます。

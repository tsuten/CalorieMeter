# 開発について
## branchの役割
`main`が意図した動作をする完成形を管理するbranchです。  
`development_{数字}`は開発中のブランチで、ある程度の大雑把さは許されます。（現在は非運用）  
区切りが良い所で`main`へsquash mergeして整えます。  
それぞれの開発状況は`feature_{名前}`内のコミットで管理します。
**`main`への直接プッシュはせず**、<u>必ず</u>プルリクエストを挟むようにします。

## gitの基本的運用について
コミットメッセージは[Conventional Commit](https://www.conventionalcommits.org/ja/v1.0.0/)を使ってください。  
コミットはなるべく小さい単位に分割して、意図を明確に示すようにしてください。**変更を加える時は特にです。**

## スタイリングについて
### python
[PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)を基準とします。
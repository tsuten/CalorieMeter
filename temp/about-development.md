# 開発について
## branchの役割
`master`が意図した動作をする完成形を管理するbranchです。  
`development_{数字}`は開発中のブランチで、ある程度の大雑把さは許されます。  
区切りが良い所で`master`へsquash mergeして整えます。  
それぞれの開発状況は`feature_{名前}`内のコミットで管理します。
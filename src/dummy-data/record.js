// Recordページ用のデータと設定

// 食事タイプの日本語名マッピング
export const mealTypeNames = {
  breakfast: '朝食',
  lunch: '昼食',
  dinner: '夕食',
  snack: '間食',
}

// 食事タイプに応じたBadgeの色マッピング
export const mealTypeColors = {
  breakfast: 'yellow',
  lunch: 'green',
  dinner: 'blue',
  snack: 'pink',
}

// 食事タイプのソート順
export const mealTypeOrder = {
  breakfast: 0,
  lunch: 1,
  dinner: 2,
  snack: 3,
}

// 食事タイプの日本語名を取得するヘルパー関数
export const getMealTypeName = (mealType) => {
  return mealTypeNames[mealType] || mealType
}

// 食事タイプに応じたBadgeの色を取得するヘルパー関数
export const getMealTypeColor = (mealType) => {
  return mealTypeColors[mealType] || 'gray'
}

// 日付を日本語形式に変換するヘルパー関数
export const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const weekdays = ['日', '月', '火', '水', '木', '金', '土']
  const weekday = weekdays[date.getDay()]
  return `${year}/${month}/${day} (${weekday})`
}

// テーブルの列定義
export const tableColumns = [
  { key: 'date', label: '日付' },
  { key: 'mealType', label: '食事タイプ' },
  { key: 'menu', label: 'メニュー' },
  { key: 'calories', label: 'カロリー' },
]

// 空のメッセージ
export const emptyMessage = '記録がありません'

// 説明文
export const description = 'それぞれの記録をクリックすると詳細を見れます'

// picsumからランダムな画像URLを取得する関数
// seedに基づいて一貫した画像を返す（同じseedなら同じ画像）
export const getRandomImageUrl = (seed, width = 400, height = 300) => {
  // seedが数値の場合はそのまま使用、文字列の場合はハッシュ化
  const imageSeed = typeof seed === 'string' 
    ? seed.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
    : seed
  return `https://picsum.photos/seed/${imageSeed}/${width}/${height}`
}

// カレンダー用のダミーデータ
// FullCalendarのイベント形式で食事記録を定義

// 日付をYYYY-MM-DD形式で取得するヘルパー関数
const formatDate = (date) => {
  return date.toISOString().split('T')[0]
}

// 日付を加算するヘルパー関数
const addDays = (date, days) => {
  const result = new Date(date)
  result.setDate(result.getDate() + days)
  return result
}

// 現在の日付を基準にダミーデータを生成
const today = new Date()
const startDate = addDays(today, -14) // 2週間前から
const endDate = addDays(today, 14) // 2週間後まで

// 食事タイプごとの色設定
const mealColors = {
  breakfast: { bg: '#FFE082', border: '#FFC107' }, // 黄色（朝食）
  lunch: { bg: '#81C784', border: '#4CAF50' }, // 緑色（昼食）
  dinner: { bg: '#64B5F6', border: '#2196F3' }, // 青色（夕食）
  snack: { bg: '#F48FB1', border: '#E91E63' }, // ピンク色（間食）
}

// ランダムなカロリー値を生成（指定範囲内）
const randomCalorie = (min, max) => {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

// 食事メニューのサンプル
const mealMenus = {
  breakfast: [
    'トーストとスクランブルエッグ',
    'ご飯と味噌汁',
    'シリアルと牛乳',
    'パンケーキ',
    'おにぎり',
  ],
  lunch: [
    'ラーメン',
    'カレーライス',
    'サンドイッチ',
    'うどん',
    'ハンバーガー',
  ],
  dinner: [
    '焼き魚定食',
    'パスタ',
    'ステーキ',
    '鍋料理',
    '寿司',
  ],
  snack: [
    'チョコレート',
    'フルーツ',
    'クッキー',
    'ヨーグルト',
    'ナッツ',
  ],
}

// ランダムなメニューを選択
const getRandomMenu = (mealType) => {
  const menus = mealMenus[mealType]
  return menus[Math.floor(Math.random() * menus.length)]
}

// イベントデータを生成
const generateEvents = () => {
  const events = []
  const currentDate = new Date(startDate)

  while (currentDate <= endDate) {
    const dateStr = formatDate(currentDate)
    const dayOfWeek = currentDate.getDay()

    // 週末は少し多めの食事を記録
    const isWeekend = dayOfWeek === 0 || dayOfWeek === 6

    // 朝食（80%の確率で記録）
    if (Math.random() > 0.6) {
      const calories = randomCalorie(300, 600)
      events.push({
        title: `朝食: ${getRandomMenu('breakfast')} (${calories}kcal)`,
        date: dateStr,
        backgroundColor: mealColors.breakfast.bg,
        borderColor: mealColors.breakfast.border,
        extendedProps: {
          mealType: 'breakfast',
          calories: calories,
          menu: getRandomMenu('breakfast'),
        },
      })
    }

    // 昼食（90%の確率で記録）
    if (Math.random() > 0.6) {
      const calories = randomCalorie(500, 900)
      events.push({
        title: `昼食: ${getRandomMenu('lunch')} (${calories}kcal)`,
        date: dateStr,
        backgroundColor: mealColors.lunch.bg,
        borderColor: mealColors.lunch.border,
        extendedProps: {
          mealType: 'lunch',
          calories: calories,
          menu: getRandomMenu('lunch'),
        },
      })
    }

    // 夕食（95%の確率で記録）
    if (Math.random() > 0.5) {
      const calories = randomCalorie(600, 1000)
      events.push({
        title: `夕食: ${getRandomMenu('dinner')} (${calories}kcal)`,
        date: dateStr,
        backgroundColor: mealColors.dinner.bg,
        borderColor: mealColors.dinner.border,
        extendedProps: {
          mealType: 'dinner',
          calories: calories,
          menu: getRandomMenu('dinner'),
        },
      })
    }

    // 間食（30%の確率で記録、週末は50%）
    const snackProbability = isWeekend ? 0.5 : 0.3
    if (Math.random() > snackProbability) {
      const calories = randomCalorie(100, 300)
      events.push({
        title: `間食: ${getRandomMenu('snack')} (${calories}kcal)`,
        date: dateStr,
        backgroundColor: mealColors.snack.bg,
        borderColor: mealColors.snack.border,
        extendedProps: {
          mealType: 'snack',
          calories: calories,
          menu: getRandomMenu('snack'),
        },
      })
    }

    // 次の日へ
    currentDate.setDate(currentDate.getDate() + 1)
  }

  return events
}

// ダミーデータをエクスポート
export const calendarEvents = generateEvents()

// 日付ごとの合計カロリーを計算するヘルパー関数
export const getTotalCaloriesByDate = (dateStr) => {
  return calendarEvents
    .filter((event) => event.date === dateStr)
    .reduce((total, event) => total + event.extendedProps.calories, 0)
}

// 特定の日付のイベントを取得するヘルパー関数
export const getEventsByDate = (dateStr) => {
  return calendarEvents.filter((event) => event.date === dateStr)
}

// 食事タイプごとの色をエクスポート
export { mealColors }

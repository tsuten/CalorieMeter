import { Modal, Text, Title, Group, Badge, Image, Stack } from '@mantine/core'

// 食事タイプの日本語名を取得するヘルパー関数
const getMealTypeName = (mealType) => {
  const names = {
    breakfast: '朝食',
    lunch: '昼食',
    dinner: '夕食',
    snack: '間食',
  }
  return names[mealType] || mealType
}

// 食事タイプに応じたBadgeの色を取得
const getMealTypeColor = (mealType) => {
  const colors = {
    breakfast: 'yellow',
    lunch: 'green',
    dinner: 'blue',
    snack: 'pink',
  }
  return colors[mealType] || 'gray'
}

// イベント情報から一貫した画像IDを生成
const getImageId = (date, mealType) => {
  // 日付とmealTypeを組み合わせてシード値を作成
  const seed = `${date}-${mealType}`
  // 文字列を数値に変換（簡易的なハッシュ）
  let hash = 0
  for (let i = 0; i < seed.length; i++) {
    const char = seed.charCodeAt(i)
    hash = ((hash << 5) - hash) + char
    hash = hash & hash // Convert to 32bit integer
  }
  // 1-1000の範囲に正規化
  return Math.abs(hash % 1000) + 1
}

function CalendarRecordModal({ opened, onClose, event }) {
  if (!event) return null

  // イベントごとに一貫した画像を取得
  const imageId = getImageId(event.date, event.mealType)
  const imageUrl = `https://picsum.photos/seed/${imageId}/400/300`

  return (
    <Modal
      opened={opened}
      onClose={onClose}
      title="食事記録の詳細"
      centered
      zIndex={1000}
      portalProps={{ target: typeof document !== 'undefined' ? document.body : undefined }}
      overlayProps={{ opacity: 0.55 }}
      size="md"
    >
      <Stack gap="md">
        {/* 画像 */}
        <Image
          src={imageUrl}
          alt={event.menu}
          radius="md"
          height={200}
          fit="cover"
        />

        {/* 食事タイプのBadge */}
        <Group>
          <Badge color={getMealTypeColor(event.mealType)} size="lg">
            {getMealTypeName(event.mealType)}
          </Badge>
        </Group>

        {/* メニュー名 */}
        <Title order={4}>{event.menu}</Title>

        {/* カロリー情報 */}
        <Text size="lg" fw={500}>
          カロリー: <Text span c="red" fw={700}>{event.calories}kcal</Text>
        </Text>

        {/* 日付情報 */}
        <Text size="sm" c="dimmed">
          日付: {event.date}
        </Text>
      </Stack>
    </Modal>
  )
}

export default CalendarRecordModal

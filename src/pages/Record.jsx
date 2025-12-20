import '../styles/pageStyle.css'
import { Card, Badge, Text, Group, Stack, Image, Table } from '@mantine/core'
import { calendarEvents } from '../dummy-data/calendar.js'
import {
  getMealTypeName,
  getMealTypeColor,
  formatDate,
  mealTypeOrder,
  emptyMessage,
  description,
  getRandomImageUrl,
} from '../dummy-data/record.js'

function Record() {
  // カレンダーイベントをカード用のデータに変換
  const cardData = calendarEvents
    .map((event) => ({
      id: `${event.date}-${event.extendedProps.mealType}`,
      date: event.date,
      mealType: event.extendedProps.mealType,
      menu: event.extendedProps.menu,
      calories: event.extendedProps.calories,
    }))
    .sort((a, b) => {
      // 日付でソート（新しい順）
      const dateCompare = b.date.localeCompare(a.date)
      if (dateCompare !== 0) return dateCompare
      // 同じ日付の場合は食事タイプでソート（朝食→昼食→夕食→間食）
      return mealTypeOrder[a.mealType] - mealTypeOrder[b.mealType]
    })

  const cards = cardData.map((item) => (
    <Card key={item.id} shadow="sm" padding="lg" radius="md" withBorder>
      <Group align="stretch" gap="md" wrap="nowrap">
        <Image
          src={getRandomImageUrl(item.id)}
          alt={item.menu}
          radius="md"
          style={{
            width: '200px',
            height: '100%',
            flexShrink: 0,
            objectFit: 'cover',
          }}
        />
        <Stack gap="sm" style={{ flex: 1 }}>
          <Table>
            <Table.Tbody>
              <Table.Tr>
                <Table.Td style={{ padding: '4px 8px', fontWeight: 500 }}>日付</Table.Td>
                <Table.Td style={{ padding: '4px 8px' }}>{formatDate(item.date)}</Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td style={{ padding: '4px 8px', fontWeight: 500 }}>食事タイプ</Table.Td>
                <Table.Td style={{ padding: '4px 8px' }}>
                  <Badge color={getMealTypeColor(item.mealType)}>
                    {getMealTypeName(item.mealType)}
                  </Badge>
                </Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td style={{ padding: '4px 8px', fontWeight: 500 }}>メニュー</Table.Td>
                <Table.Td style={{ padding: '4px 8px' }}>{item.menu}</Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td style={{ padding: '4px 8px', fontWeight: 500 }}>カロリー</Table.Td>
                <Table.Td style={{ padding: '4px 8px' }}>{item.calories}kcal</Table.Td>
              </Table.Tr>
            </Table.Tbody>
          </Table>
        </Stack>
      </Group>
    </Card>
  ))

  return (
    <div className="page-container">
      <h1 className="page-title">記録</h1>
      <p>{description}</p>
      <div className="page-content">
        {cards.length > 0 ? (
          <Stack gap="md">{cards}</Stack>
        ) : (
          <Card shadow="sm" padding="lg" radius="md" withBorder>
            <Text ta="center" c="dimmed">
              {emptyMessage}
            </Text>
          </Card>
        )}
      </div>
    </div>
  )
}

export default Record

/* Todo: 絞り込み機能を追加する */
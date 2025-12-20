import '../styles/pageStyle.css'
import { useState } from 'react'
import FullCalendar from '@fullcalendar/react'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'
import jaLocale from '@fullcalendar/core/locales/ja'
import { calendarEvents } from '../dummy-data/calendar.js'
import CalendarRecordModal from '../components/CalendarRecordModal'

function Calendar() {
  // ダミーデータを使用
  const events = calendarEvents

  // Modalの状態管理
  const [opened, setOpened] = useState(false)
  const [selectedEvent, setSelectedEvent] = useState(null)

  // 日付クリック時の処理
  const handleDateClick = (info) => {
    console.log('クリックされた日付:', info.dateStr)
  }

  // イベントクリック時の処理
  const handleEventClick = (info) => {
    const event = info.event
    const extendedProps = event.extendedProps
    setSelectedEvent({
      title: event.title,
      date: event.startStr,
      calories: extendedProps.calories,
      menu: extendedProps.menu,
      mealType: extendedProps.mealType,
    })
    setOpened(true)
  }


  return (
    <div className="page-container">
      <h1 className="page-title">カレンダー</h1>
      <div className="page-content">
        <div style={{ padding: '20px' }}>
          <FullCalendar
            plugins={[dayGridPlugin, interactionPlugin]}
            initialView="dayGridMonth"
            locale={jaLocale}
            headerToolbar={{
              left: 'prev,next today',
              center: 'title',
              right: 'dayGridMonth,dayGridWeek'
            }}
            buttonText={{
              today: '今日',
              month: '月',
              week: '週'
            }}
            events={events}
            dateClick={handleDateClick}
            eventClick={handleEventClick}
            height="auto"
            editable={true}
            selectable={true}
          />
        </div>
      </div>

      {/* イベント詳細Modal */}
      <CalendarRecordModal
        opened={opened}
        onClose={() => setOpened(false)}
        event={selectedEvent}
      />
    </div>
  )
}

export default Calendar


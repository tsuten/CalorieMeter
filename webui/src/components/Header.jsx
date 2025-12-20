import { Link, useLocation, useNavigate } from 'react-router-dom'
import { Group, Title, Paper, Avatar, Tabs, Stack } from '@mantine/core'
import { pageRoutes } from '../App'
import HomeIcon from '@mui/icons-material/Home'
import CalendarMonthIcon from '@mui/icons-material/CalendarMonth'
import EditNoteIcon from '@mui/icons-material/EditNote'
import BarChartIcon from '@mui/icons-material/BarChart'
import PersonIcon from '@mui/icons-material/Person'
import SettingsIcon from '@mui/icons-material/Settings'
import InfoIcon from '@mui/icons-material/Info'

// ルート情報のマッピング
const routeConfig = {
  '/': {
    label: 'ホーム',
    icon: HomeIcon
  },
  '/calendar': {
    label: 'カレンダー',
    icon: CalendarMonthIcon
  },
  '/record': {
    label: '記録',
    icon: EditNoteIcon
  },
  '/statistics': {
    label: '統計',
    icon: BarChartIcon
  },
  '/profile': {
    label: 'プロフィール',
    icon: PersonIcon
  },
  '/settings': {
    label: '設定',
    icon: SettingsIcon
  },
  '/about': {
    label: 'About',
    icon: InfoIcon
  }
}

function Header() {
  const location = useLocation()
  const navigate = useNavigate()

  return (
    <Paper
      component="header"
      shadow="none"
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        zIndex: 1000,
        borderRadius: 0,
      }}
    >
      <Stack
        gap="md"
        style={{
          maxWidth: '1280px',
          width: '100%',
          margin: '0 auto',
          padding: '1rem 1.5rem',
        }}
      >
        {/* 上の列: ロゴとAvatar */}
        <Group
          justify="space-between"
          align="center"
        >
          <Link
            to="/"
            style={{
              textDecoration: 'none',
              color: 'inherit',
            }}
          >
            <Title order={3} style={{ margin: 0 }}>
              CalorieMeter
            </Title>
          </Link>
          <Avatar
            component={Link}
            to="/profile"
            radius="xl"
            color="blue"
          >
            <PersonIcon />
          </Avatar>
        </Group>
        
        {/* 下の列: Tabs */}
        <Tabs
          value={location.pathname}
          onChange={(value) => navigate(value || '/')}
          variant="outline"
          style={{
            position: 'relative',
            top: '-3rem',
          }}
        >
          <Tabs.List justify="center">
            {pageRoutes.map((route) => {
              const { label, icon: Icon } = routeConfig[route]
              return (
                <Tabs.Tab
                  key={route}
                  value={route}
                  leftSection={<Icon fontSize="small" />}
                >
                  {label}
                </Tabs.Tab>
              )
            })}
          </Tabs.List>
        </Tabs>
      </Stack>
    </Paper>
  )
}

export default Header


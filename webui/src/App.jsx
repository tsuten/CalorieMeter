import { useLocation } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import { useRef, useEffect } from 'react'
import Header from './components/Header'
import PageWrapper from './utils/PageWrapper'
import Home from './pages/Home'
import Calendar from './pages/Calendar'
import Record from './pages/Record'
import Statistics from './pages/Statistics'
import Profile from './pages/Profile'
import Settings from './pages/Settings'
import About from './pages/About'
import './App.css'

// ページの横の位置関係を定義（左から右の順序）
export const pageRoutes = ['/', '/calendar', '/record', '/statistics', '/profile', '/settings', '/about']

function App() {
  const location = useLocation()
  // initialize prevPathnameRef
  const prevPathnameRef = useRef(location.pathname)

  // render後にprevPathnameRefを更新（次回のrenderで使用される）
  const prevPathname = prevPathnameRef.current
  
  useEffect(() => {
    // update prevPathnameRef for next render
    return () => {
      prevPathnameRef.current = location.pathname
    }
  }, [location.pathname])

  const getPageComponent = () => {
    switch (location.pathname) {
      case '/':
        return <Home />
      case '/calendar':
        return <Calendar />
      case '/record':
        return <Record />
      case '/statistics':
        return <Statistics />
      case '/profile':
        return <Profile />
      case '/settings':
        return <Settings />
      case '/about':
        return <About />
      default:
        return <Home />
    }
  }

  const prevIndex = pageRoutes.indexOf(prevPathname)
  const currentIndex = pageRoutes.indexOf(location.pathname)

  return (
    <>
      <style>{`
        .app-container {
          padding-top: 64px;
          overflow-x: hidden;
          position: relative;
          max-width: 1280px;
          width: 100%;
          margin: 0 auto;
          padding-left: 1.5rem;
          padding-right: 1.5rem;
        }
      `}</style>
      <Header />
      <div className="app-container">
        <AnimatePresence mode="wait" initial={false}>
          <PageWrapper 
            key={location.pathname} 
            pathname={location.pathname}
            prevIndex={prevIndex}
            currentIndex={currentIndex}
          >
            {getPageComponent()}
          </PageWrapper>
        </AnimatePresence>
      </div>
    </>
  )
}

export default App

/*
思考過程 / 意思決定

- routesを使用していないのは全てのルートをPageWrapperで囲む必要が出てきて、可読性が落ちて重複が増える為

*/
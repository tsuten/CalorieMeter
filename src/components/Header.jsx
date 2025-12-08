import { Link, useLocation } from 'react-router-dom'

function Header() {
  const location = useLocation()

  return (
    <>
      <style>{`
        .header {
          width: 100%;
          background-color: rgba(26, 26, 26, 0.8);
          backdrop-filter: blur(10px);
          border-bottom: 1px solid rgba(100, 108, 255, 0.2);
          padding: 1rem 2rem;
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          z-index: 1000;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .header-container {
          max-width: 1280px;
          margin: 0 auto;
          display: flex;
          justify-content: space-between;
          align-items: center;
          gap: 2rem;
        }

        .header-title {
          font-size: 1.8rem;
          font-weight: 600;
          margin: 0;
          background: linear-gradient(135deg, #646cff 0%, #535bf2 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .header-title-link {
          text-decoration: none;
        }

        .header-nav {
          display: flex;
          gap: 1.5rem;
          align-items: center;
        }

        .nav-link {
          color: rgba(255, 255, 255, 0.87);
          text-decoration: none;
          font-weight: 500;
          padding: 0.5rem 1rem;
          border-radius: 6px;
          transition: all 0.2s ease;
        }

        .nav-link:hover {
          color: #646cff;
          background-color: rgba(100, 108, 255, 0.1);
        }

        .nav-link.active {
          color: #646cff;
          background-color: rgba(100, 108, 255, 0.2);
        }

        @media (prefers-color-scheme: light) {
          .header {
            background-color: rgba(255, 255, 255, 0.9);
            border-bottom-color: rgba(100, 108, 255, 0.2);
          }

          .nav-link {
            color: #213547;
          }

          .nav-link:hover {
            color: #535bf2;
            background-color: rgba(100, 108, 255, 0.1);
          }

          .nav-link.active {
            color: #535bf2;
            background-color: rgba(100, 108, 255, 0.2);
          }
        }

        @media (max-width: 768px) {
          .header {
            padding: 1rem;
          }

          .header-container {
            flex-direction: column;
            gap: 1rem;
          }

          .header-title {
            font-size: 1.5rem;
          }

          .header-nav {
            flex-wrap: wrap;
            justify-content: center;
            gap: 1rem;
          }

          .nav-link {
            font-size: 0.9rem;
            padding: 0.4rem 0.8rem;
          }
        }
      `}</style>
      <header className="header">
        <div className="header-container">
          <Link to="/" className="header-title-link">
            <h1 className="header-title">CalorieMeter</h1>
          </Link>
          <nav className="header-nav">
            <Link 
              to="/" 
              className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
            >
              ホーム
            </Link>
            <Link 
              to="/calendar" 
              className={`nav-link ${location.pathname === '/calendar' ? 'active' : ''}`}
            >
              カレンダー
            </Link>
            <Link 
              to="/record" 
              className={`nav-link ${location.pathname === '/record' ? 'active' : ''}`}
            >
              記録
            </Link>
            <Link 
              to="/statistics" 
              className={`nav-link ${location.pathname === '/statistics' ? 'active' : ''}`}
            >
              統計
            </Link>
            <Link 
              to="/profile" 
              className={`nav-link ${location.pathname === '/profile' ? 'active' : ''}`}
            >
              プロフィール
            </Link>
            <Link 
              to="/settings" 
              className={`nav-link ${location.pathname === '/settings' ? 'active' : ''}`}
            >
              設定
            </Link>
            <Link 
              to="/about" 
              className={`nav-link ${location.pathname === '/about' ? 'active' : ''}`}
            >
              About
            </Link>
          </nav>
        </div>
      </header>
    </>
  )
}

export default Header


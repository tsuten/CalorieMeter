import { useNavigate } from 'react-router-dom'
import { motion, useMotionValue, useTransform } from 'framer-motion'
import { useState, useEffect, useMemo } from 'react'
import { pageRoutes } from '../App'

function PageWrapper({ children, pathname, prevIndex, currentIndex }) {
  const navigate = useNavigate()
  const x = useMotionValue(0)
  const opacity = useTransform(x, [-300, 0, 300], [0, 1, 0])
  const [isDragging, setIsDragging] = useState(false)

  // アニメーション方向に応じたvariantsをメモ化して生成（不要なre-renderを防ぐ）
  const pageVariants = useMemo(() => {
    if (currentIndex > prevIndex) {
      // 次のページへ（右から左へ）
      return {
        initial: {
          opacity: 0,
          x: 300,
        },
        animate: {
          opacity: 1,
          x: 0,
          transition: {
            duration: 0.3,
            ease: 'easeInOut',
          },
        },
        exit: {
          opacity: 0,
          x: -300,
          transition: {
            duration: 0.3,
            ease: 'easeInOut',
          },
        },
      }
    } else if (currentIndex < prevIndex) {
      // 前のページへ（左から右へ）
      return {
        initial: {
          opacity: 0,
          x: -300,
        },
        animate: {
          opacity: 1,
          x: 0,
          transition: {
            duration: 0.3,
            ease: 'easeInOut',
          },
        },
        exit: {
          opacity: 0,
          x: 300,
          transition: {
            duration: 0.3,
            ease: 'easeInOut',
          },
        },
      }
    } else {
      // 初回ロード時など、方向が不明な場合
      return {
        initial: {
          opacity: 0,
          x: 300,
        },
        animate: {
          opacity: 1,
          x: 0,
          transition: {
            duration: 0.3,
            ease: 'easeInOut',
          },
        },
        exit: {
          opacity: 0,
          x: -300,
          transition: {
            duration: 0.3,
            ease: 'easeInOut',
          },
        },
      }
    }
  }, [currentIndex, prevIndex])

  useEffect(() => {
    // ページが変わったときにxをリセット
    x.set(0)
  }, [pathname, x])

  const handleDragEnd = (event, info) => {
    const threshold = 100
    const velocity = info.velocity.x

    if (Math.abs(info.offset.x) > threshold || Math.abs(velocity) > 500) {
      if (info.offset.x > 0 && currentIndex > 0) {
        // 右にスワイプ（前のページへ）
        navigate(pageRoutes[currentIndex - 1])
      } else if (info.offset.x < 0 && currentIndex < pageRoutes.length - 1) {
        // 左にスワイプ（次のページへ）
        navigate(pageRoutes[currentIndex + 1])
      } else {
        // しきい値に達していない場合は元に戻す
        x.set(0)
      }
    } else {
      // しきい値に達していない場合は元に戻す
      x.set(0)
    }
    setIsDragging(false)
  }

  return (
    <>
      <style>{`
        .page-wrapper {
          width: 100%;
          min-height: calc(100vh - 80px);
        }
      `}</style>
      <motion.div
        className="page-wrapper"
        variants={pageVariants}
        initial="initial"
        animate={isDragging ? undefined : "animate"}
        exit="exit"
        drag="x"
        dragConstraints={{ left: -300, right: 300 }}
        dragElastic={0.2}
        onDragStart={() => setIsDragging(true)}
        onDragEnd={handleDragEnd}
        style={{ x, opacity }}
      >
        {children}
      </motion.div>
    </>
  )
}

export default PageWrapper

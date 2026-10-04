import { useEffect, useState } from 'react'
import { useQueryClient } from '@tanstack/react-query'
import { api } from '../api'
import { Button, ErrorBox } from '../ui'

interface Start {
  token: string
  bot_url: string
  ttl: number
}

const KEY = 'panel_login'

function loadToken(): Start | null {
  try {
    const raw = sessionStorage.getItem(KEY)
    return raw ? (JSON.parse(raw) as Start) : null
  } catch {
    return null
  }
}

function saveToken(s: Start | null) {
  try {
    if (s) sessionStorage.setItem(KEY, JSON.stringify(s))
    else sessionStorage.removeItem(KEY)
  } catch {
    // saqlab bo'lmasa ham kirish ishlaydi, faqat sahifa yangilansa qaytadan bosiladi
  }
}

export default function Login() {
  const qc = useQueryClient()
  // Sahifa yangilansa ham kutilayotgan kirish yo'qolmasin
  const [start, setStart] = useState<Start | null>(loadToken)
  const [expired, setExpired] = useState(false)
  const [error, setError] = useState<unknown>(null)

  const begin = async () => {
    setError(null)
    setExpired(false)
    // Oynani bosish paytida ochamiz, aks holda brauzer popup'ni bloklaydi
    const tab = window.open('', '_blank')
    try {
      const s = await api.post<Start>('/auth/start')
      setStart(s)
      saveToken(s)
      if (tab) {
        tab.opener = null
        tab.location.href = s.bot_url
      }
    } catch (e) {
      tab?.close()
      setError(e)
    }
  }

  // Egasi botda tasdiqlaguncha tekshirib turamiz. Brauzer orqa fondagi sahifaning taymerini
  // sekinlatishi yoki to'xtatishi mumkin — shuning uchun sahifaga qaytilganda darhol ham tekshiramiz.
  useEffect(() => {
    if (!start) return
    let done = false
    const check = async () => {
      if (done) return
      try {
        const r = await api.get<{ status: string }>(`/auth/poll?token=${encodeURIComponent(start.token)}`)
        setError(null)
        if (r.status === 'ok') {
          done = true
          saveToken(null)
          qc.invalidateQueries({ queryKey: ['me'] })
        } else if (r.status === 'expired') {
          done = true
          saveToken(null)
          setStart(null)
          setExpired(true)
        }
      } catch (e) {
        // Uxlab qolgan sahifada so'rov uzilishi mumkin — keyingi urinishda o'tib ketadi
        setError(e)
      }
    }
    const onVisible = () => {
      if (document.visibilityState === 'visible') check()
    }
    const timer = setInterval(check, 2000)
    document.addEventListener('visibilitychange', onVisible)
    window.addEventListener('focus', check)
    return () => {
      done = true
      clearInterval(timer)
      document.removeEventListener('visibilitychange', onVisible)
      window.removeEventListener('focus', check)
    }
  }, [start, qc])

  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <div className="w-full max-w-sm rounded-2xl bg-white p-8 text-center shadow-sm ring-1 ring-zinc-200 dark:bg-zinc-900 dark:ring-zinc-800">
        <div className="mb-2 text-4xl">🎀</div>
        <h1 className="mb-1 text-xl font-semibold">Boshqaruv paneli</h1>
        <p className="mb-6 text-sm text-zinc-500">Faqat kanal egasi va muharrir kira oladi.</p>

        {!start ? (
          <Button className="w-full" onClick={begin}>
            Telegram orqali kirish
          </Button>
        ) : (
          <div className="space-y-4 text-sm">
            <p>
              Telegram'da bot ochildi. U yerda <b>Start</b>, keyin <b>«✅ Ha, men kiryapman»</b> tugmasini bosing.
            </p>
            <p className="animate-pulse text-zinc-500">Tasdiq kutilmoqda…</p>
            <a href={start.bot_url} target="_blank" rel="noopener" className="block text-brand-600 underline">
              Bot ochilmadimi? Shu yerni bosing
            </a>
            <button
              type="button"
              className="text-zinc-500 underline"
              onClick={() => {
                saveToken(null)
                setStart(null)
              }}
            >
              Qaytadan boshlash
            </button>
          </div>
        )}

        {expired && <p className="mt-4 text-sm text-amber-600">Vaqt tugadi. Qaytadan bosing.</p>}
        <div className="mt-4">
          <ErrorBox error={error} />
        </div>
      </div>
    </div>
  )
}

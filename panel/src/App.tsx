import { useQuery, useQueryClient } from '@tanstack/react-query'
import { NavLink, Navigate, Route, Routes } from 'react-router-dom'
import { ApiError, api, type Me } from './api'
import { Loading, MeContext, cx } from './ui'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Giveaways from './pages/Giveaways'
import GiveawayNew from './pages/GiveawayNew'
import GiveawayView from './pages/GiveawayView'
import LiveDraw from './pages/LiveDraw'
import PublicList from './pages/PublicList'
import Payouts from './pages/Payouts'
import Sponsors from './pages/Sponsors'
import Content from './pages/Content'

const NAV = [
  { to: '/', label: 'Bosh sahifa', icon: '🏠', end: true },
  { to: '/giveaways', label: 'Rozigrishlar', icon: '🎁' },
  { to: '/payouts', label: "To'lovlar", icon: '💳' },
  { to: '/sponsors', label: 'Homiylar', icon: '📣' },
  { to: '/content', label: 'Kontent', icon: '📝' },
]
// Muharrir: kontent, rozigrishlarni ko'radi va jonli o'yinni o'tkazadi (to'lov, homiy, yangi rozigrish — faqat egasi)
const EDITOR_NAV = [
  { to: '/content', label: 'Kontent', icon: '📝', end: false },
  { to: '/giveaways', label: 'Rozigrishlar', icon: '🎁', end: false },
]
const SOON = [
  { label: 'CRM (reklama)', icon: '🤝' },
  { label: 'AI suhbatlar', icon: '💬' },
]

export default function App() {
  return (
    <Routes>
      {/* Ochiq sahifa: ishtirokchilar ro'yxati, login shart emas */}
      <Route path="/p/:id" element={<PublicList />} />
      <Route path="*" element={<Private />} />
    </Routes>
  )
}

function Private() {
  const me = useQuery({
    queryKey: ['me'],
    queryFn: () => api.get<Me>('/me'),
  })

  if (me.isPending) return <Loading />
  if (me.error) {
    if (me.error instanceof ApiError && me.error.status === 401) return <Login />
    return <div className="p-6 text-sm text-red-600">Server bilan aloqa yo'q: {me.error.message}</div>
  }
  return (
    <MeContext.Provider value={me.data}>
      <Routes>
        {/* Jonli o'yin: menyusiz, to'liq ekran (efirda ulashiladi) */}
        <Route path="/giveaways/:id/live" element={<LiveDraw />} />
        <Route path="*" element={<Shell me={me.data} />} />
      </Routes>
    </MeContext.Provider>
  )
}

function Shell({ me }: { me: Me }) {
  const qc = useQueryClient()
  const logout = async () => {
    await api.post('/auth/logout')
    qc.clear()
    window.location.href = '/'
  }
  const nav = me.role === 'owner' ? NAV : EDITOR_NAV
  const navClass = ({ isActive }: { isActive: boolean }) =>
    cx(
      'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium',
      isActive ? 'bg-brand-50 text-brand-700 dark:bg-brand-700/20 dark:text-brand-100' : 'text-zinc-600 hover:bg-zinc-100 dark:text-zinc-300 dark:hover:bg-zinc-800',
    )

  return (
    <div className="flex min-h-screen">
      {/* Kompyuter: chap menyu */}
      <aside className="sticky top-0 hidden h-screen w-60 shrink-0 flex-col border-r border-zinc-200 bg-white p-4 md:flex dark:border-zinc-800 dark:bg-zinc-900">
        <div className="mb-6 px-3">
          <div className="text-base font-semibold">🎀 {me.channel.title}</div>
          <div className="text-xs text-zinc-500">Boshqaruv paneli</div>
        </div>
        <nav className="space-y-1">
          {nav.map((n) => (
            <NavLink key={n.to} to={n.to} end={n.end} className={navClass}>
              <span>{n.icon}</span>
              {n.label}
            </NavLink>
          ))}
        </nav>
        <div className="mt-6 space-y-1">
          <div className="px-3 text-xs font-medium tracking-wide text-zinc-400 uppercase">Tez orada</div>
          {SOON.map((n) => (
            <div key={n.label} className="flex items-center gap-3 px-3 py-2 text-sm text-zinc-400">
              <span className="opacity-60">{n.icon}</span>
              {n.label}
            </div>
          ))}
        </div>
        <div className="mt-auto border-t border-zinc-200 px-3 pt-4 text-sm dark:border-zinc-800">
          <div className="truncate font-medium">{me.name}</div>
          <div className="mb-2 text-xs text-zinc-500">{me.role === 'owner' ? 'Egasi' : 'Muharrir'}</div>
          <button onClick={logout} className="text-xs text-zinc-500 hover:text-brand-600">
            Chiqish
          </button>
        </div>
      </aside>

      <div className="flex min-w-0 flex-1 flex-col">
        {/* Telefon: yuqori panel */}
        <header className="flex items-center justify-between border-b border-zinc-200 bg-white px-4 py-3 md:hidden dark:border-zinc-800 dark:bg-zinc-900">
          <div className="font-semibold">🎀 {me.channel.title}</div>
          <button onClick={logout} className="text-xs text-zinc-500">
            Chiqish
          </button>
        </header>

        <main className="mx-auto w-full max-w-5xl flex-1 p-4 pb-24 md:p-8">
          {me.role === 'owner' ? (
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/giveaways" element={<Giveaways />} />
              <Route path="/giveaways/new" element={<GiveawayNew />} />
              <Route path="/giveaways/:id" element={<GiveawayView />} />
              <Route path="/payouts" element={<Payouts />} />
              <Route path="/sponsors" element={<Sponsors />} />
              <Route path="/content" element={<Content />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          ) : (
            <Routes>
              <Route path="/giveaways" element={<Giveaways />} />
              <Route path="/giveaways/:id" element={<GiveawayView />} />
              <Route path="/content" element={<Content />} />
              <Route path="*" element={<Navigate to="/content" replace />} />
            </Routes>
          )}
        </main>

        {/* Telefon: pastki menyu */}
        {nav.length > 1 && (
          <nav
            className={cx(
              'fixed inset-x-0 bottom-0 z-40 grid border-t border-zinc-200 bg-white md:hidden dark:border-zinc-800 dark:bg-zinc-900',
              nav.length === 5 ? 'grid-cols-5' : 'grid-cols-2',
            )}
          >
            {nav.map((n) => (
              <NavLink
                key={n.to}
                to={n.to}
                end={n.end}
                className={({ isActive }) =>
                  cx('flex flex-col items-center gap-0.5 py-2 text-[11px]', isActive ? 'text-brand-600' : 'text-zinc-500')
                }
              >
                <span className="text-lg">{n.icon}</span>
                {n.label}
              </NavLink>
            ))}
          </nav>
        )}
      </div>
    </div>
  )
}

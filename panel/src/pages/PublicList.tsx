// Ochiq sahifa: rozigrish ishtirokchilari (ism va raqam). Login shart emas — kanal postidagi tugmadan ochiladi.

import { useMemo, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { useParams } from 'react-router-dom'
import { ApiError, api, type GiveawayStatus, type PublicGiveaway } from '../api'
import { Card, Loading, cx, formatDate, inputClass } from '../ui'

const PAGE = 200
const MEDALS = ['🥇', '🥈', '🥉']

const STATUS: Record<GiveawayStatus, [string, string]> = {
  active: ['🟢 Qatnashish davom etmoqda', 'bg-green-100 text-green-800 dark:bg-green-950 dark:text-green-300'],
  drawing: ["🎥 Qatnashish yopildi — g'oliblar jonli efirda aniqlanadi", 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300'],
  finished: ['🏁 Rozigrish yakunlandi', 'bg-zinc-100 text-zinc-700 dark:bg-zinc-800 dark:text-zinc-300'],
  cancelled: ['Bekor qilingan', 'bg-red-100 text-red-700 dark:bg-red-950 dark:text-red-300'],
}

export default function PublicList() {
  const { id } = useParams()
  const [q, setQ] = useState('')
  const [limit, setLimit] = useState(PAGE)
  const [onlyMissing, setOnlyMissing] = useState(false)
  const g = useQuery({
    queryKey: ['public', id],
    queryFn: () => api.get<PublicGiveaway>(`/public/giveaways/${id}`),
    refetchInterval: (query) => (query.state.data?.status === 'finished' ? false : 15_000),
  })

  const filtered = useMemo(() => {
    const all = g.data?.participants ?? []
    const items = onlyMissing ? all.filter((p) => p.missing.length) : all
    const term = q.trim().replace(/^#/, '').toLowerCase()
    if (!term) return items
    return items.filter((p) => String(p.number) === term || p.name.toLowerCase().includes(term))
  }, [g.data, q, onlyMissing])

  if (g.isPending) return <Loading />
  if (g.error)
    return (
      <div className="px-4 py-16 text-center text-sm text-zinc-500">
        {g.error instanceof ApiError && g.error.status === 404 ? 'Rozigrish topilmadi.' : `Xato: ${g.error.message}`}
      </div>
    )
  const d = g.data
  const dropped = d.participants.filter((p) => p.missing.length).length

  return (
    <div className="mx-auto max-w-2xl px-4 py-6 pb-16">
      <div className="mb-1 text-sm text-zinc-500">
        🎀{' '}
        {d.channel.link ? (
          <a href={d.channel.link} className="hover:text-brand-600">
            {d.channel.title}
          </a>
        ) : (
          d.channel.title
        )}
      </div>
      <h1 className="mb-3 text-2xl font-bold">{d.title}</h1>
      <div className={cx('mb-5 inline-block rounded-full px-3 py-1 text-sm font-medium', STATUS[d.status][1])}>{STATUS[d.status][0]}</div>

      {d.winners.length > 0 && (
        <Card className="mb-5 ring-amber-300 dark:ring-amber-700">
          <h2 className="mb-3 font-semibold">🏆 G'oliblar</h2>
          <ol className="space-y-2">
            {d.winners.map((w) => (
              <li key={w.place} className="flex items-center gap-3">
                <span className="w-7 text-center text-xl">{MEDALS[w.place - 1] ?? '🏅'}</span>
                <div className="min-w-0 flex-1">
                  <div className="truncate font-medium">
                    {w.name} <span className="text-zinc-400 tabular-nums">#{w.number}</span>
                  </div>
                  <div className="text-xs text-zinc-500">{w.prize.label}</div>
                </div>
              </li>
            ))}
          </ol>
        </Card>
      )}

      <div className="mb-5 grid grid-cols-2 gap-3">
        <Card>
          <div className="text-2xl font-semibold tabular-nums">{d.participants.length - dropped}</div>
          <div className="text-xs text-zinc-500">
            ishtirokchi
            {dropped > 0 && <span className="text-red-600 dark:text-red-400"> · {dropped} tasi obuna emas</span>}
          </div>
        </Card>
        <Card>
          <div className="text-base font-semibold">{formatDate(d.ends_at, d.timezone)}</div>
          <div className="text-xs text-zinc-500">{d.status !== 'active' ? 'qatnashish yopildi' : d.auto_draw ? 'qatnashish yopiladi' : "jonli o'yin (taxminan)"}</div>
        </Card>
      </div>

      {d.winners.length === 0 && (
        <Card className="mb-5">
          <h2 className="mb-2 font-semibold">🎁 Sovrinlar</h2>
          <ol className="space-y-1 text-sm">
            {d.prizes.map((p, i) => (
              <li key={i} className="flex gap-3">
                <span className="w-6 text-zinc-500">{i + 1}.</span>
                {p.label}
              </li>
            ))}
          </ol>
        </Card>
      )}

      <Card>
        <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
          <div className="flex flex-wrap items-center gap-x-3 gap-y-1">
            <h2 className="font-semibold">👥 Ishtirokchilar</h2>
            {(dropped > 0 || onlyMissing) && (
              <label className="flex items-center gap-1.5 text-sm text-zinc-600 dark:text-zinc-300">
                <input
                  type="checkbox"
                  className="accent-brand-500"
                  checked={onlyMissing}
                  onChange={(e) => {
                    setOnlyMissing(e.target.checked)
                    setLimit(PAGE)
                  }}
                />
                Faqat obuna bo'lmaganlar ({dropped})
              </label>
            )}
          </div>
          <input
            className={inputClass + ' sm:w-60'}
            placeholder="Ismingiz yoki raqamingiz"
            value={q}
            onChange={(e) => {
              setQ(e.target.value)
              setLimit(PAGE)
            }}
          />
        </div>
        {filtered.length ? (
          <ul className="divide-y divide-zinc-100 text-sm dark:divide-zinc-800">
            {filtered.slice(0, limit).map((p) => (
              <li key={p.number} className="flex gap-3 py-1.5">
                <span className="w-14 shrink-0 text-zinc-400 tabular-nums">#{p.number}</span>
                {p.missing.length ? (
                  <div className="min-w-0">
                    <div className="truncate text-zinc-400 line-through">{p.name}</div>
                    <div className="text-xs text-red-600 dark:text-red-400">❌ Obuna emas: {p.missing.join(', ')}</div>
                  </div>
                ) : (
                  <span className="min-w-0 truncate">{p.name}</span>
                )}
              </li>
            ))}
          </ul>
        ) : (
          <div className="py-8 text-center text-sm text-zinc-500">{q ? 'Topilmadi.' : onlyMissing ? 'Hamma obuna ✅' : "Hali hech kim qatnashmagan."}</div>
        )}
        {filtered.length > limit && (
          <button onClick={() => setLimit(limit + PAGE)} className="mt-3 w-full rounded-lg py-2 text-sm text-brand-600 hover:bg-brand-50 dark:hover:bg-zinc-800">
            Yana ko'rsatish ({filtered.length - limit})
          </button>
        )}
      </Card>

      {d.post_url && (
        <div className="mt-6 text-center">
          <a href={d.post_url} className="text-sm text-brand-600 hover:underline">
            Rozigrish postiga o'tish ↗
          </a>
        </div>
      )}
    </div>
  )
}

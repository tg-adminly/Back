// Jonli o'yin: efirda ekranni ulashib ko'rsatiladi. G'olibni server (draw.py) aniqlaydi,
// bu sahifa faqat barabanni aylantirib, natijani chiroyli ochib beradi.

import { useEffect, useMemo, useRef, useState, type CSSProperties, type ReactNode } from 'react'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { Link, useParams } from 'react-router-dom'
import { api, type LivePick, type LiveState } from '../api'
import { Loading, cx } from '../ui'

type Stage =
  | { kind: 'idle' }
  | { kind: 'spin'; number: number; name: string; tick: number }
  | { kind: 'winner'; pick: LivePick; key: number }
  | { kind: 'skipped'; pick: LivePick; key: number }

const MEDALS = ['🥇', '🥈', '🥉']
const medal = (place: number) => MEDALS[place - 1] ?? '🏅'
const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms))

export default function LiveDraw() {
  const { id } = useParams()
  const qc = useQueryClient()
  const live = useQuery({
    queryKey: ['live', id],
    queryFn: () => api.get<LiveState>(`/giveaways/${id}/live`),
    refetchOnWindowFocus: false,
    // Obuna tekshiruvi ketayotganda jarayonni ko'rsatib turamiz
    // Tekshiruv ketayotganda — jarayon; qatnashish ochiq paytda — ishtirokchilar soni
    refetchInterval: (query) => (query.state.data?.check ? 1000 : query.state.data?.status === 'active' ? 10_000 : false),
  })
  // Sahifa ochilgandan keyin chiqqanlar shu yerda — animatsiya tugagach ro'yxatga qo'shiladi
  const [picks, setPicks] = useState<LivePick[] | null>(null)
  const [stage, setStage] = useState<Stage>({ kind: 'idle' })
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [exhausted, setExhausted] = useState(false)
  const [announcing, setAnnouncing] = useState<'ask' | 'sending' | null>(null)
  const [starting, setStarting] = useState<'ask' | 'sending' | null>(null)
  const [announced, setAnnounced] = useState(false)
  const alive = useRef(true)
  useEffect(() => {
    alive.current = true
    return () => {
      alive.current = false
    }
  }, [])

  const d = live.data
  const all = picks ?? d?.picks ?? []
  const winners = all.filter((p) => p.place !== null)
  const skipped = all.filter((p) => p.place === null)
  const nextPlace = winners.length + 1
  const finished = d?.status === 'finished' || announced
  const done = !!d && (winners.length >= d.winners_count || exhausted || d.exhausted)
  const checking = !!d?.check
  const canSpin = !!d && d.status === 'drawing' && !busy && !done && !finished && !checking
  // Ro'yxatni faqat o'yin boshlanmasdan yangilash mumkin (birinchi g'olib chiqqach — yo'q)
  const canCheck = !!d && d.status === 'drawing' && all.length === 0 && !busy
  const eligible = d ? d.participants - d.excluded.length : 0
  // Shartni bajarmaganlar: o'yindan oldingi tekshiruvda chiqib ketganlar + o'yinda o'tkazib yuborilganlar
  const dropped = [...(d?.excluded ?? []), ...skipped]

  /** Jonli rejim: qatnashishni yopib, o'yinni boshlash (vaqtdan oldin ham, keyin ham) */
  async function start() {
    setStarting('sending')
    setError(null)
    try {
      await api.post(`/giveaways/${id}/finish`)
      qc.invalidateQueries({ queryKey: ['giveaway', id] })
      qc.invalidateQueries({ queryKey: ['giveaways'] })
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
    } finally {
      setStarting(null)
    }
    await qc.invalidateQueries({ queryKey: ['live', id] })
  }

  async function check() {
    setError(null)
    try {
      await api.post(`/giveaways/${id}/live/check`)
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
    }
    await qc.invalidateQueries({ queryKey: ['live', id] })
  }

  async function next() {
    if (!d || !canSpin) return
    setBusy(true)
    setError(null)
    let tick = 0
    const show = () => {
      const n = d.names[Math.floor(Math.random() * d.names.length)]
      setStage({ kind: 'spin', number: n.number, name: n.name, tick: ++tick })
    }
    const fast = async (ms: number, until?: () => boolean) => {
      const start = performance.now()
      while (alive.current && (performance.now() - start < ms || (until && !until()))) {
        show()
        await sleep(60)
      }
    }
    const slowDown = async () => {
      for (let delay = 70; delay < 480 && alive.current; delay *= 1.16) {
        show()
        await sleep(delay)
      }
    }

    // So'rov baraban aylanayotganda ketadi — internet sekin bo'lsa ham ekranda to'xtab qolmaydi
    let result: LivePick[] | null = null
    let failed: unknown = null
    const req = api.post<{ picks: LivePick[] }>(`/giveaways/${id}/live/next`).then(
      (r) => (result = r.picks),
      (e) => (failed = e),
    )
    try {
      await fast(2200, () => result !== null || failed !== null)
      await req
      if (failed) throw failed
      const got: LivePick[] = result!
      for (const [i, p] of got.entries()) {
        if (i > 0) await fast(1200)
        await slowDown()
        if (!alive.current) return
        setPicks((prev) => [...(prev ?? d.picks), p])
        if (p.place === null) {
          setStage({ kind: 'skipped', pick: p, key: Date.now() })
          if (i < got.length - 1) await sleep(3000)
        } else {
          setStage({ kind: 'winner', pick: p, key: Date.now() })
        }
      }
      if (got[got.length - 1]?.place === null) setExhausted(true) // nomzod qolmadi
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
      setStage({ kind: 'idle' })
      setPicks(null) // server holatiga qaytamiz
      await qc.invalidateQueries({ queryKey: ['live', id] })
    } finally {
      if (alive.current) setBusy(false)
    }
  }

  async function announce() {
    setAnnouncing('sending')
    setError(null)
    try {
      await api.post(`/giveaways/${id}/live/announce`)
      setAnnounced(true)
      qc.invalidateQueries({ queryKey: ['giveaway', id] })
      qc.invalidateQueries({ queryKey: ['giveaways'] })
      qc.invalidateQueries({ queryKey: ['payouts'] })
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
    } finally {
      setAnnouncing(null)
    }
  }

  // Probel — keyingi g'olib (efirda sichqonchani qidirmaslik uchun)
  const listRef = useRef<HTMLOListElement>(null)
  useEffect(() => {
    listRef.current?.querySelector(`[data-place="${Math.min(nextPlace, d?.winners_count ?? 1)}"]`)?.scrollIntoView({ block: 'nearest', behavior: 'smooth' })
  }, [nextPlace, d?.winners_count])

  const nextRef = useRef(next)
  useEffect(() => {
    nextRef.current = next
  })
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.code !== 'Space' || e.repeat) return
      e.preventDefault()
      nextRef.current()
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [])

  if (live.isPending) return <Loading />
  if (live.error || !d) return <div className="p-6 text-sm text-red-600">{live.error?.message}</div>

  const prizeOf = (place: number) => d.prizes[place - 1]?.label ?? ''

  return (
    <div className="fixed inset-x-0 top-0 h-dvh overflow-hidden bg-[#14060e] text-white">
      {/* Fon */}
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(225,29,116,0.35),transparent_60%),radial-gradient(ellipse_at_bottom_right,rgba(250,204,21,0.12),transparent_55%)]" />

      <div className="relative flex h-full flex-col gap-3 p-4 sm:p-5 lg:gap-5 lg:p-8 short:gap-2 short:py-3">
        {/* Sarlavha */}
        <header className="space-y-1 short:flex short:items-center short:gap-3 short:space-y-0">
          <div className="flex items-center justify-between gap-3 short:order-2 short:shrink-0">
            <div className="text-[11px] short:hidden font-semibold tracking-[0.25em] text-pink-300/80 uppercase lg:text-xs">🎀 Jonli rozigrish</div>
            <div className="flex shrink-0 items-center gap-2">
              <div className="rounded-full bg-white/10 px-3 py-1.5 text-sm font-semibold ring-1 ring-white/15 lg:px-4 lg:py-2 lg:text-base">
                👥 {eligible} <span className="hidden sm:inline">ishtirokchi</span>
              </div>
              {/* iPhone Safari to'liq ekranni qo'llab-quvvatlamaydi — u yerda tugma chiqmaydi */}
              {document.fullscreenEnabled && (
                <button
                  onClick={() => (document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen())}
                  className="rounded-full bg-white/10 px-3 py-1.5 text-sm ring-1 ring-white/15 hover:bg-white/20 lg:py-2"
                  title="To'liq ekran"
                >
                  ⛶
                </button>
              )}
              <Link to={`/giveaways/${d.id}`} className="rounded-full px-2 py-1.5 text-sm text-white/50 hover:text-white lg:py-2" title="Panelga qaytish">
                ✕
              </Link>
            </div>
          </div>
          <h1 className="line-clamp-2 text-2xl leading-tight font-bold break-words sm:text-3xl lg:text-5xl short:min-w-0 short:flex-1 short:truncate short:text-xl">{d.title}</h1>
        </header>

        {/* Telefon (tik): baraban tepada, g'oliblar pastda. Keng ekran / yotiq telefon: yonma-yon */}
        <div className="grid min-h-0 flex-1 grid-rows-[minmax(0,1fr)_auto] gap-3 md:grid-cols-[1fr_minmax(240px,320px)] md:grid-rows-1 lg:grid-cols-[1fr_minmax(300px,380px)] lg:gap-5">
          <StageView stage={stage} d={d} nextPlace={nextPlace} done={done} finished={finished} busy={busy} prizeOf={prizeOf} />

          {/* G'oliblar ustuni */}
          <aside className="flex max-h-[34dvh] min-h-0 flex-col rounded-2xl bg-white/[0.06] p-3 ring-1 ring-white/10 backdrop-blur md:max-h-none lg:rounded-3xl lg:p-4">
            <h2 className="mb-2 px-1 text-base font-bold lg:mb-3 lg:text-lg short:mb-1 short:text-sm">🏆 G'oliblar</h2>
            <ol ref={listRef} className="min-h-0 flex-1 space-y-1.5 overflow-y-auto pr-1 lg:space-y-2">
              {Array.from({ length: d.winners_count }, (_, i) => i + 1).map((place) => {
                const w = winners.find((p) => p.place === place)
                const current = busy && place === nextPlace
                return (
                  <li
                    key={place + (w ? '-w' : '')}
                    data-place={place}
                    className={cx(
                      'flex items-center gap-2 rounded-xl px-2.5 py-1.5 ring-1 lg:gap-3 lg:rounded-2xl lg:px-3 lg:py-2.5',
                      w ? 'anim-pop bg-amber-300/10 ring-amber-300/40' : 'bg-white/[0.03] ring-white/10',
                      current && 'ring-2 ring-pink-400',
                    )}
                  >
                    <span className="w-7 text-center text-xl lg:w-9 lg:text-2xl">{medal(place)}</span>
                    <div className="min-w-0 flex-1">
                      {w ? (
                        <div className="truncate text-sm font-semibold lg:text-base">
                          {w.name} <span className="font-normal text-white/50 tabular-nums">#{w.number}</span>
                        </div>
                      ) : (
                        <div className="text-sm text-white/35 lg:text-base">{current ? 'aniqlanmoqda…' : `${place}-o'rin`}</div>
                      )}
                      <div className="truncate text-xs text-amber-200/80">{prizeOf(place)}</div>
                    </div>
                  </li>
                )
              })}
            </ol>
            {dropped.length > 0 && (
              <div className="mt-2 max-h-[30%] shrink-0 overflow-y-auto border-t border-white/10 px-1 pt-2 text-xs text-white/50 lg:mt-3 lg:pt-3">
                <span className="font-semibold text-red-300/80">❌ Kanalga obuna bo'lmagani uchun qatnashmaydi ({dropped.length}): </span>
                <span className="line-clamp-2 md:line-clamp-none short:line-clamp-1">
                  {dropped.map((p) => `#${p.number} ${p.name}${p.missing.length ? ` (${p.missing.join(', ')})` : ''}`).join(' · ')}
                </span>
              </div>
            )}
          </aside>
        </div>

        {/* Pastki qism: ishtirokchilar lentasi + boshqaruv */}
        <footer className="space-y-3 lg:space-y-4">
          {/* Past ekranda (yotiq telefon) joy tejash uchun lenta yashiriladi */}
          <div className="short:hidden">
            <NamesMarquee names={d.names} />
          </div>
          {d.check ? (
            <CheckProgress done={d.check.done} total={d.check.total} />
          ) : (
            canCheck && (
              <div className="flex flex-wrap items-center justify-center gap-x-3 gap-y-1 text-sm text-white/60">
                <span>
                  {d.excluded.length
                    ? `🔄 Obuna tekshirildi: ${d.excluded.length} kishi obuna emas`
                    : '🔄 Obuna tekshirildi: hamma shartni bajargan'}
                </span>
                <button onClick={check} className="rounded-full px-3 py-1 text-pink-300 ring-1 ring-pink-300/40 hover:bg-pink-300/10">
                  Qayta tekshirish
                </button>
              </div>
            )
          )}
          {d.check_error && !d.check && (
            <div className="rounded-xl bg-amber-500/15 px-4 py-2 text-sm text-amber-100 ring-1 ring-amber-400/30">⚠️ {d.check_error}</div>
          )}
          {error && <div className="rounded-xl bg-red-500/15 px-4 py-2 text-sm text-red-200 ring-1 ring-red-400/30">{error}</div>}
          <div className="flex flex-wrap items-center justify-center gap-3">
            {d.status === 'active' && d.auto_draw ? (
              <div className="text-center text-white/60">
                🤖 Bu rozigrishda g'olibni bot avtomatik aniqlaydi.{' '}
                <Link to={`/giveaways/${d.id}`} className="text-pink-300 underline">
                  Rozigrish sahifasi
                </Link>
              </div>
            ) : d.status === 'active' && starting === 'ask' ? (
              <>
                <span className="w-full text-center text-white/80 sm:w-auto">Qatnashish yopiladi — keyin hech kim qo'shila olmaydi. Boshlaymizmi?</span>
                <BigButton onClick={start}>Ha, boshlaymiz</BigButton>
                <button onClick={() => setStarting(null)} className="px-4 py-3 text-white/60 hover:text-white">
                  Yo'q
                </button>
              </>
            ) : d.status === 'active' ? (
              <BigButton onClick={() => setStarting('ask')} disabled={starting === 'sending'}>
                {starting === 'sending' ? 'Yopilmoqda…' : "⏹ Qatnashishni yopib, o'yinni boshlash"}
              </BigButton>
            ) : finished ? (
              <div className="rounded-full bg-green-500/15 px-6 py-3 font-semibold text-green-200 ring-1 ring-green-400/30">
                ✅ Natija kanalga e'lon qilindi
              </div>
            ) : !done ? (
              <>
                <BigButton onClick={next} disabled={!canSpin}>
                  {busy ? '🎲 Aylanmoqda…' : `🎲 ${nextPlace}-o'rin g'olibini aniqlash`}
                </BigButton>
                {!busy && <span className="hidden text-xs text-white/40 pointer-fine:inline">yoki Probel tugmasi</span>}
              </>
            ) : announcing === 'ask' ? (
              <>
                <span className="w-full text-center text-white/80 sm:w-auto">G'oliblarni kanalga e'lon qilaymi?</span>
                <BigButton onClick={announce}>Ha, e'lon qilaman</BigButton>
                <button onClick={() => setAnnouncing(null)} className="px-4 py-3 text-white/60 hover:text-white">
                  Yo'q
                </button>
              </>
            ) : (
              <BigButton onClick={() => setAnnouncing('ask')} disabled={busy || announcing === 'sending'}>
                {announcing === 'sending' ? 'Yuborilmoqda…' : "📣 Natijani kanalga e'lon qilish"}
              </BigButton>
            )}
          </div>
        </footer>
      </div>
    </div>
  )
}

function StageView({
  stage,
  d,
  nextPlace,
  done,
  finished,
  busy,
  prizeOf,
}: {
  stage: Stage
  d: LiveState
  nextPlace: number
  done: boolean
  finished: boolean
  busy: boolean
  prizeOf: (place: number) => string
}) {
  const base = 'relative flex min-h-[180px] flex-col items-center justify-center overflow-hidden rounded-2xl p-4 text-center ring-1 lg:rounded-3xl lg:p-6'

  if (stage.kind === 'winner') {
    const p = stage.pick
    return (
      <section key={stage.key} className={cx(base, 'anim-glow bg-gradient-to-b from-amber-300/15 to-pink-500/10 ring-amber-300/50')}>
        <Confetti />
        <div className="anim-land relative">
          <div className="mb-2 text-sm font-bold tracking-[0.2em] whitespace-nowrap text-amber-300 uppercase sm:text-lg lg:mb-3 lg:text-2xl lg:tracking-[0.3em]">
            {medal(p.place!)} {p.place}-o'rin g'olibi
          </div>
          <div className="text-4xl leading-tight font-black break-words sm:text-5xl lg:text-8xl">{p.name}</div>
          <div className="mt-2 text-xl text-white/60 tabular-nums lg:mt-3 lg:text-4xl">#{p.number}</div>
          <div className="mt-4 inline-block rounded-full bg-amber-300 px-5 py-1.5 text-base font-bold text-amber-950 lg:mt-6 lg:px-6 lg:py-2 lg:text-2xl">
            🎁 {prizeOf(p.place!)}
          </div>
        </div>
      </section>
    )
  }

  if (stage.kind === 'skipped') {
    const p = stage.pick
    return (
      <section key={stage.key} className={cx(base, 'anim-shake bg-red-500/10 ring-red-400/50')}>
        <div className="text-3xl font-bold break-words text-white/50 line-through decoration-red-400 sm:text-4xl lg:text-7xl">{p.name}</div>
        <div className="mt-1 text-lg text-white/40 tabular-nums lg:mt-2 lg:text-3xl">#{p.number}</div>
        <div className="mt-4 rounded-full bg-red-500/20 px-4 py-1.5 text-sm font-semibold text-red-200 lg:mt-6 lg:px-5 lg:py-2 lg:text-xl">
          ❌ {p.missing.length ? `«${p.missing.join('», «')}» kanaliga obuna emas` : 'Kanalga obuna emas'} — o'tkazib yuborildi
        </div>
        {busy && <div className="mt-3 text-sm text-white/50">Qayta aylantiramiz…</div>}
      </section>
    )
  }

  if (stage.kind === 'spin') {
    return (
      <section className={cx(base, 'bg-white/[0.06] ring-pink-400/40')}>
        <div className="mb-3 text-xs font-semibold tracking-[0.15em] whitespace-nowrap text-pink-300 uppercase sm:text-base lg:mb-4 lg:text-xl lg:tracking-[0.25em]">
          {medal(nextPlace)} {nextPlace}-o'rin aniqlanmoqda…
        </div>
        <div key={stage.tick} className="anim-slot w-full">
          <div className="truncate text-4xl font-black sm:text-5xl lg:text-8xl">{stage.name}</div>
          <div className="mt-2 text-xl text-pink-200/70 tabular-nums lg:mt-3 lg:text-4xl">#{stage.number}</div>
        </div>
      </section>
    )
  }

  return (
    <section className={cx(base, 'bg-white/[0.06] ring-white/10')}>
      <div className="mb-3 text-6xl lg:mb-4 lg:text-9xl short:text-4xl">{finished || done ? '🎉' : '🎲'}</div>
      {finished ? (
        <div className="text-2xl font-bold sm:text-3xl lg:text-5xl">Rozigrish yakunlandi!</div>
      ) : done ? (
        <>
          <div className="text-2xl font-bold sm:text-3xl lg:text-5xl">Barcha g'oliblar aniqlandi!</div>
          <div className="mt-3 text-lg text-white/60">Tabriklaymiz! 💕</div>
        </>
      ) : d.status === 'active' ? (
        <>
          <div className="text-2xl font-bold sm:text-3xl lg:text-5xl">Qatnashish davom etmoqda</div>
          <div className="mt-2 text-base text-white/60 sm:text-lg lg:mt-3 lg:text-2xl">
            {d.participants} ishtirokchi · {d.winners_count} ta g'olib
          </div>
        </>
      ) : (
        <>
          <div className="text-2xl font-bold sm:text-3xl lg:text-5xl">
            {nextPlace === 1 ? "Baraban tayyor" : `Keyingi: ${nextPlace}-o'rin`}
          </div>
          <div className="mt-2 text-base text-white/60 sm:text-lg lg:mt-3 lg:text-2xl">
            {nextPlace === 1
              ? `${d.participants - d.excluded.length} ishtirokchi orasidan ${d.winners_count} ta g'olib`
              : `🎁 ${prizeOf(nextPlace)}`}
          </div>
        </>
      )}
    </section>
  )
}

function CheckProgress({ done, total }: { done: number; total: number }) {
  const pct = total ? Math.round((done / total) * 100) : 0
  return (
    <div className="mx-auto w-full max-w-md text-center text-sm text-white/70">
      <div className="mb-1.5">
        🔄 Obuna tekshirilmoqda… <span className="tabular-nums">{done}/{total}</span>
      </div>
      <div className="h-1.5 overflow-hidden rounded-full bg-white/10">
        <div className="h-full rounded-full bg-pink-400 transition-[width] duration-500" style={{ width: `${pct}%` }} />
      </div>
    </div>
  )
}

function BigButton({ children, onClick, disabled }: { children: ReactNode; onClick: () => void; disabled?: boolean }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className="w-full rounded-full bg-gradient-to-r from-pink-500 to-fuchsia-500 px-6 py-3.5 text-base font-bold shadow-lg shadow-pink-500/30 transition hover:scale-[1.03] hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-50 disabled:hover:scale-100 sm:w-auto sm:px-8 sm:py-4 sm:text-lg lg:text-xl short:py-2.5 short:text-base"
    >
      {children}
    </button>
  )
}

const CONFETTI_COLORS = ['#f472b6', '#facc15', '#a78bfa', '#34d399', '#60a5fa', '#fb7185', '#ffffff']

function Confetti() {
  const pieces = useMemo(
    () =>
      Array.from({ length: 90 }, (_, i) => ({
        left: Math.random() * 100,
        delay: Math.random() * 0.8,
        duration: 2.6 + Math.random() * 2,
        color: CONFETTI_COLORS[i % CONFETTI_COLORS.length],
        drift: `${(Math.random() - 0.5) * 30}vw`,
        spin: `${(Math.random() - 0.5) * 1440}deg`,
      })),
    [],
  )
  return (
    <div className="pointer-events-none absolute inset-0">
      {pieces.map((p, i) => (
        <span
          key={i}
          className="confetti"
          style={
            {
              left: `${p.left}%`,
              background: p.color,
              animationDelay: `${p.delay}s`,
              animationDuration: `${p.duration}s`,
              '--drift': p.drift,
              '--spin': p.spin,
            } as CSSProperties
          }
        />
      ))}
    </div>
  )
}

/** Barcha ishtirokchilar baraban ichida ekanini ko'rsatuvchi aylanma lenta */
function NamesMarquee({ names }: { names: LiveState['names'] }) {
  const shown = useMemo(() => {
    const copy = [...names]
    for (let i = copy.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1))
      ;[copy[i], copy[j]] = [copy[j], copy[i]]
    }
    return copy.slice(0, 200)
  }, [names])
  if (!shown.length) return null
  const duration = Math.min(Math.max(shown.length * 1.2, 25), 180)
  return (
    <div className="overflow-hidden [mask-image:linear-gradient(90deg,transparent,black_8%,black_92%,transparent)]">
      <div className="marquee flex w-max gap-2" style={{ animationDuration: `${duration}s` }}>
        {[...shown, ...shown].map((n, i) => (
          <span key={i} className="rounded-full bg-white/[0.07] px-3 py-1 text-sm whitespace-nowrap text-white/70 ring-1 ring-white/10">
            <span className="text-white/40 tabular-nums">#{n.number}</span> {n.name}
          </span>
        ))}
      </div>
    </div>
  )
}

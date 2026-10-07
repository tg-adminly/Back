import { useEffect, useRef, useState, type ClipboardEvent, type ReactNode } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useSearchParams } from 'react-router-dom'
import { api, type AiUsage, type GuideVersion, type Sample, type TrainMessage } from '../api'
import { Button, Card, ConfirmButton, Empty, ErrorBox, Field, Loading, Modal, PageHeader, cx, formatDate, inputClass, useMe } from '../ui'

const TABS = [
  { key: 'train', label: "💬 O'qitish" },
  { key: 'guide', label: '📘 Uslub qo\'llanma' },
  { key: 'samples', label: '🖼 Namunalar' },
] as const
type Tab = (typeof TABS)[number]['key']
const MAX_ALBUM = 10 // Telegram albomi

export default function Content() {
  const [params, setParams] = useSearchParams()
  const tab = (TABS.find((t) => t.key === params.get('tab'))?.key ?? 'train') as Tab
  return (
    <>
      <PageHeader title="📝 Kontent" action={<UsageChip />} />
      <div className="mb-4 flex gap-1 overflow-x-auto">
        {TABS.map((t) => (
          <button
            key={t.key}
            onClick={() => setParams(t.key === 'train' ? {} : { tab: t.key }, { replace: true })}
            className={cx(
              'shrink-0 rounded-full px-3 py-1 text-sm',
              tab === t.key ? 'bg-zinc-900 text-white dark:bg-white dark:text-zinc-900' : 'text-zinc-600 hover:bg-zinc-100 dark:text-zinc-300 dark:hover:bg-zinc-800',
            )}
          >
            {t.label}
          </button>
        ))}
      </div>
      {tab === 'train' && <TrainChat />}
      {tab === 'guide' && <GuidePage />}
      {tab === 'samples' && <SamplesPage />}
    </>
  )
}

function UsageChip() {
  const usage = useQuery({ queryKey: ['ai-usage'], queryFn: () => api.get<AiUsage>('/content/usage') })
  const u = usage.data
  if (!u) return null
  if (!u.enabled) return <span className="rounded-full bg-amber-100 px-3 py-1 text-xs text-amber-800 dark:bg-amber-950 dark:text-amber-300">⚠️ AI ulanmagan (OPENAI_API_KEY)</span>
  const over = u.month_cost >= u.limit
  return (
    <span
      title={`Model: ${u.model}`}
      className={cx('rounded-full px-3 py-1 text-xs', over ? 'bg-red-100 text-red-700 dark:bg-red-950 dark:text-red-300' : 'bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-300')}
    >
      AI bu oy: ${u.month_cost.toFixed(2)} / ${u.limit.toFixed(0)}
    </span>
  )
}

// --- O'qitish chati (chatbot ko'rinishida) ---

type ChatState = { messages: TrainMessage[]; thinking: boolean; error: string | null }

function TrainChat() {
  const qc = useQueryClient()
  const chat = useQuery({
    queryKey: ['train-chat'],
    queryFn: () => api.get<ChatState>('/content/chat'),
    // Agent fonda yozadi — javob kelguncha tez-tez so'raymiz
    refetchInterval: (q) => (q.state.data?.thinking ? 1500 : false),
  })
  const retry = useMutation({
    mutationFn: () => api.post('/content/chat/retry'),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['train-chat'] }),
  })
  const thinking = chat.data?.thinking ?? false
  useEffect(() => {
    if (!thinking) qc.invalidateQueries({ queryKey: ['ai-usage'] })
  }, [thinking, qc])

  // Yangi xabar kelganda pastga: sahifa oxirida yozish maydoni o'z joyida turadi, xabarni to'smaydi
  const count = chat.data?.messages.length ?? 0
  useEffect(() => {
    if (count || thinking) requestAnimationFrame(() => window.scrollTo({ top: document.documentElement.scrollHeight }))
  }, [count, thinking])

  if (chat.isPending) return <Loading />
  const { messages, error } = chat.data ?? { messages: [], thinking: false, error: null }

  return (
    <div className="flex min-h-[calc(100vh-14rem)] flex-col">
      <ErrorBox error={chat.error} />
      <div className="flex-1 space-y-4 pb-4">
        <AiBubble>
          <p className="mb-2">Salom! Men kanal uchun post yozishni o'rganyapman 👋</p>
          <ul className="list-disc space-y-1 pl-5 text-zinc-600 dark:text-zinc-300">
            <li>📎 bilan yoqqan postlarni rasmlari va matni bilan yuboring — 10–20 ta yetadi.</li>
            <li>Men ularni o'rganib, o'zim uchun uslub qoidalarini taklif qilaman — siz qabul qilasiz yoki tuzatasiz.</li>
            <li>Istalgan payt ko'rsatma bering: «emoji kamroq», «savol bilan tugat»…</li>
          </ul>
        </AiBubble>
        {messages.map((m) => (
          <MessageRow key={m.id} m={m} />
        ))}
        {thinking && (
          <AiBubble>
            <span className="inline-flex gap-1 py-1" aria-label="AI yozmoqda">
              {[0, 150, 300].map((d) => (
                <span key={d} className="h-2 w-2 animate-bounce rounded-full bg-zinc-400" style={{ animationDelay: `${d}ms` }} />
              ))}
            </span>
          </AiBubble>
        )}
        {error && !thinking && (
          <AiBubble>
            <p className="mb-2 text-red-600 dark:text-red-400">⚠️ {error}</p>
            <Button variant="secondary" onClick={() => retry.mutate()} disabled={retry.isPending}>
              🔄 Qayta urinish
            </Button>
          </AiBubble>
        )}
      </div>
      <Composer />
    </div>
  )
}

function AiBubble({ children, footer }: { children: ReactNode; footer?: ReactNode }) {
  return (
    <div className="flex items-end gap-2">
      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-brand-50 text-base dark:bg-brand-700/30">🤖</div>
      <div className="max-w-[85%] sm:max-w-xl">
        <div className="rounded-2xl rounded-bl-sm bg-white px-4 py-2.5 text-sm ring-1 ring-zinc-200 dark:bg-zinc-900 dark:ring-zinc-800">{children}</div>
        {footer}
      </div>
    </div>
  )
}

function MessageRow({ m }: { m: TrainMessage }) {
  const me = useMe()
  const time = formatDate(m.created_at, me.timezone).split(' ')[1]
  if (m.role === 'assistant') {
    return (
      <AiBubble footer={<div className="mt-1 text-xs text-zinc-400">{time}</div>}>
        <div className="whitespace-pre-wrap">{m.text}</div>
        {m.proposal && <ProposalBox m={m} />}
      </AiBubble>
    )
  }
  const meta = (
    <div className="mt-1 text-right text-xs text-zinc-400">
      {m.author} · {time}
    </div>
  )
  if (m.sample || m.sample_deleted) {
    return (
      <div className="flex justify-end">
        <div className="w-full max-w-[85%] sm:max-w-sm">
          {m.sample ? <SampleBubble s={m.sample} /> : <div className="text-right text-xs text-zinc-400 italic">Namuna o'chirilgan</div>}
          {meta}
        </div>
      </div>
    )
  }
  return (
    <div className="flex justify-end">
      <div className="max-w-[85%] sm:max-w-lg">
        <div className="rounded-2xl rounded-br-sm bg-brand-500 px-4 py-2.5 text-sm whitespace-pre-wrap text-white">{m.text}</div>
        {meta}
      </div>
    </div>
  )
}

/** Xodim yuborgan namuna post — Telegram postidek: albom + matn */
function SampleBubble({ s }: { s: Sample }) {
  const [more, setMore] = useState(false)
  return (
    <div className="overflow-hidden rounded-2xl rounded-br-sm bg-brand-50 ring-1 ring-brand-100 dark:bg-brand-700/20 dark:ring-brand-700/40">
      <Album images={s.images} compact />
      <div className="space-y-1.5 px-3 py-2 text-sm">
        <div className="flex items-center justify-between gap-2 text-xs text-zinc-500">
          <span className="truncate">📎 Namuna · {s.source === 'own' ? "o'z kanalimiz" : s.source_name || 'boshqa kanal'}</span>
          {s.analysis === null ? <span className="shrink-0">⏳</span> : <span className="shrink-0 text-green-700 dark:text-green-400">✓ o'rganildi</span>}
        </div>
        {s.text && <p className={cx('whitespace-pre-wrap', !more && 'line-clamp-6')}>{s.text}</p>}
        {(s.text.length > 250 || s.analysis) && (
          <button className="text-xs text-brand-600 hover:underline" onClick={() => setMore(!more)}>
            {more ? "Yig'ish" : s.analysis ? "To'liq va AI tahlili" : "To'liq"}
          </button>
        )}
        {more && s.analysis && (
          <div className="rounded-lg bg-white/70 p-2 text-xs text-zinc-600 dark:bg-zinc-900/60 dark:text-zinc-300">
            {s.image_desc && <p className="mb-1">🖼 {s.image_desc}</p>}
            <p>🤖 {s.analysis}</p>
          </div>
        )}
      </div>
    </div>
  )
}

const PROPOSAL_STATUS = {
  pending: ['', ''],
  accepted: ['✅ Qabul qilindi', 'text-green-700 dark:text-green-400'],
  rejected: ['❌ Rad etildi', 'text-zinc-500'],
  superseded: ['↪︎ Keyingi taklif bilan almashtirildi', 'text-zinc-500'],
} as const

function ProposalBox({ m }: { m: TrainMessage }) {
  const [open, setOpen] = useState(false)
  const status = m.proposal_status ?? 'pending'
  return (
    <div className="mt-2 rounded-xl bg-amber-50 p-3 text-sm ring-1 ring-amber-200 dark:bg-amber-950/40 dark:ring-amber-900">
      <div className="mb-2 font-medium">📘 Qo'llanmaga o'zgarish taklifi</div>
      {m.proposal_note && <p className="mb-2 text-zinc-700 dark:text-zinc-300">{m.proposal_note}</p>}
      {status === 'pending' ? (
        <Button onClick={() => setOpen(true)}>Ko'rib chiqish</Button>
      ) : (
        <div className="flex items-center justify-between gap-2">
          <span className={PROPOSAL_STATUS[status][1]}>{PROPOSAL_STATUS[status][0]}</span>
          <button className="text-xs text-brand-600 hover:underline" onClick={() => setOpen(true)}>
            Matnni ko'rish
          </button>
        </div>
      )}
      {open && <ProposalModal m={m} onClose={() => setOpen(false)} />}
    </div>
  )
}

function ProposalModal({ m, onClose }: { m: TrainMessage; onClose: () => void }) {
  const qc = useQueryClient()
  const guide = useQuery({ queryKey: ['guide'], queryFn: () => api.get<{ current: GuideVersion | null; versions: GuideVersion[] }>('/content/guide') })
  const [editing, setEditing] = useState(false)
  const [text, setText] = useState(m.proposal ?? '')
  const pending = m.proposal_status === 'pending'
  const decide = useMutation({
    mutationFn: (accept: boolean) => api.post(`/content/chat/${m.id}/decide`, { accept, text: accept && editing ? text : null }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['train-chat'] })
      qc.invalidateQueries({ queryKey: ['guide'] })
      onClose()
    },
  })
  return (
    <Modal title="📘 Qo'llanma taklifi" onClose={onClose}>
      {m.proposal_note && <p className="mb-3 text-sm text-zinc-600 dark:text-zinc-400">{m.proposal_note}</p>}
      {editing ? (
        <textarea className={cx(inputClass, 'mb-3 font-mono text-xs')} rows={16} value={text} onChange={(e) => setText(e.target.value)} />
      ) : guide.isPending ? (
        <Loading />
      ) : (
        <>
          {pending && guide.data?.current && <p className="mb-2 text-xs text-zinc-500">Joriy qo'llanmaga nisbatan: yashil — qo'shiladi, qizil — olib tashlanadi.</p>}
          <LineDiff before={pending ? (guide.data?.current?.text ?? '') : ''} after={m.proposal ?? ''} />
        </>
      )}
      <ErrorBox error={decide.error} />
      {pending && (
        <div className="mt-4 flex flex-wrap justify-end gap-2">
          <Button variant="ghost" onClick={() => decide.mutate(false)} disabled={decide.isPending}>
            ❌ Rad etish
          </Button>
          {!editing && (
            <Button variant="secondary" onClick={() => setEditing(true)}>
              ✏️ Tuzatish
            </Button>
          )}
          <Button onClick={() => decide.mutate(true)} disabled={decide.isPending || (editing && !text.trim())}>
            ✅ {editing ? 'Tuzatib qabul qilish' : 'Qabul qilish'}
          </Button>
        </div>
      )}
    </Modal>
  )
}

/** Qatorlar bo'yicha farq (LCS): nima qo'shildi, nima olib tashlandi */
function LineDiff({ before, after }: { before: string; after: string }) {
  const a = before ? before.split('\n') : []
  const b = after.split('\n')
  const dp = Array.from({ length: a.length + 1 }, () => new Array<number>(b.length + 1).fill(0))
  for (let i = a.length - 1; i >= 0; i--)
    for (let j = b.length - 1; j >= 0; j--) dp[i][j] = a[i] === b[j] ? dp[i + 1][j + 1] + 1 : Math.max(dp[i + 1][j], dp[i][j + 1])
  const rows: { kind: ' ' | '+' | '-'; line: string }[] = []
  let i = 0
  let j = 0
  while (i < a.length || j < b.length) {
    if (i < a.length && j < b.length && a[i] === b[j]) rows.push({ kind: ' ', line: a[i++] }), j++
    else if (j < b.length && (i >= a.length || dp[i][j + 1] >= dp[i + 1][j])) rows.push({ kind: '+', line: b[j++] })
    else rows.push({ kind: '-', line: a[i++] })
  }
  const showMarks = a.length > 0
  return (
    <div className="max-h-[50vh] overflow-y-auto rounded-lg bg-zinc-50 p-3 text-sm leading-relaxed dark:bg-zinc-800/60">
      {rows.map((r, k) => (
        <div
          key={k}
          className={cx(
            'min-h-[1.25rem] px-1 whitespace-pre-wrap',
            showMarks && r.kind === '+' && 'bg-green-100 text-green-900 dark:bg-green-950 dark:text-green-200',
            showMarks && r.kind === '-' && 'bg-red-100 text-red-800 line-through dark:bg-red-950 dark:text-red-300',
          )}
        >
          {r.line}
        </div>
      ))}
    </div>
  )
}

const isTouch = () => window.matchMedia('(pointer: coarse)').matches

/** Pastdagi yozish maydoni: matn + 📎 rasmlar. Rasm biriktirilsa yoki «Namuna post» yoqilsa — namuna sifatida ketadi */
function Composer() {
  const qc = useQueryClient()
  const [text, setText] = useState('')
  const [images, setImages] = useState<File[]>([])
  const [previews, setPreviews] = useState<string[]>([])
  const [asSample, setAsSample] = useState(false)
  // Manba saqlanib qoladi — bir kanaldan ketma-ket bir nechta post yuboriladi
  const [own, setOwn] = useState(false)
  const [sourceName, setSourceName] = useState('')
  const [dragging, setDragging] = useState(false)
  const fileInput = useRef<HTMLInputElement>(null)
  const textarea = useRef<HTMLTextAreaElement>(null)
  const sample = asSample || images.length > 0

  useEffect(() => {
    const urls = images.map((f) => URL.createObjectURL(f))
    setPreviews(urls)
    return () => urls.forEach((u) => URL.revokeObjectURL(u))
  }, [images])

  // Matnga qarab balandligi o'sadi
  useEffect(() => {
    const el = textarea.current
    if (!el) return
    el.style.height = 'auto'
    el.style.height = `${Math.min(el.scrollHeight, 240)}px`
  }, [text])

  // Telegram albomi kabi: 10 tagacha, qo'shilgan tartibda
  const addImages = (files: File[]) => setImages((prev) => [...prev, ...files.filter((f) => f.type.startsWith('image/'))].slice(0, MAX_ALBUM))

  const send = useMutation({
    mutationFn: () => {
      const form = new FormData()
      form.append('text', text)
      form.append('sample', String(sample))
      form.append('source', own ? 'own' : 'other')
      form.append('source_name', own ? '' : sourceName)
      images.forEach((f) => form.append('images', f))
      return api.post<TrainMessage>('/content/chat/message', form)
    },
    onSuccess: () => {
      setText('')
      setImages([])
      setAsSample(false)
      qc.invalidateQueries({ queryKey: ['train-chat'] })
      qc.invalidateQueries({ queryKey: ['samples'] })
      textarea.current?.focus()
    },
  })
  const canSend = !send.isPending && (text.trim().length > 0 || images.length > 0)
  const submit = () => canSend && send.mutate()

  const onPaste = (e: ClipboardEvent) => {
    const files = [...e.clipboardData.files].filter((f) => f.type.startsWith('image/'))
    if (files.length) {
      e.preventDefault()
      addImages(files)
    }
  }

  return (
    <div className="sticky bottom-16 z-30 -mx-4 bg-gradient-to-t from-zinc-50 from-70% px-4 pt-3 pb-2 md:bottom-0 md:-mx-8 md:px-8 md:pb-6 dark:from-zinc-950">
      <ErrorBox error={send.error} />
      <div
        className={cx(
          'mt-2 rounded-2xl bg-white shadow-sm ring-1 ring-zinc-300 focus-within:ring-2 focus-within:ring-brand-500 dark:bg-zinc-900 dark:ring-zinc-700',
          dragging && 'ring-2 ring-brand-500',
        )}
        onDragOver={(e) => {
          e.preventDefault()
          setDragging(true)
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault()
          setDragging(false)
          addImages([...e.dataTransfer.files])
        }}
      >
        {previews.length > 0 && (
          <div className="flex gap-2 overflow-x-auto px-3 pt-3">
            {previews.map((url, k) => (
              <div key={url} className="relative h-16 w-16 shrink-0 overflow-hidden rounded-lg ring-1 ring-zinc-200 dark:ring-zinc-700">
                <img src={url} alt="" className="h-full w-full object-cover" />
                <span className="absolute top-0.5 left-0.5 rounded bg-black/60 px-1 text-[10px] text-white">{k + 1}</span>
                <button
                  type="button"
                  aria-label="Olib tashlash"
                  onClick={() => setImages(images.filter((_, i) => i !== k))}
                  className="absolute top-0.5 right-0.5 flex h-5 w-5 items-center justify-center rounded-full bg-black/60 text-xs text-white hover:bg-red-600"
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        )}
        {sample && (
          <div className="flex flex-wrap items-center gap-x-3 gap-y-1 border-b border-zinc-100 px-3 py-2 text-xs dark:border-zinc-800">
            <span className="font-medium text-brand-600">📎 Namuna post</span>
            <label className="flex items-center gap-1.5 text-zinc-600 dark:text-zinc-300">
              <input type="checkbox" checked={own} onChange={(e) => setOwn(e.target.checked)} className="accent-brand-500" />
              o'z kanalimizdan
            </label>
            {!own && (
              <input
                className="min-w-0 flex-1 rounded-md bg-zinc-100 px-2 py-1 placeholder:text-zinc-400 focus:outline-none dark:bg-zinc-800"
                placeholder="qaysi kanaldan (ixtiyoriy)"
                value={sourceName}
                onChange={(e) => setSourceName(e.target.value)}
                maxLength={255}
              />
            )}
          </div>
        )}
        <textarea
          ref={textarea}
          rows={1}
          maxLength={5000}
          className="block max-h-60 w-full resize-none bg-transparent px-4 pt-3 pb-1 text-sm placeholder:text-zinc-400 focus:outline-none"
          placeholder={sample ? 'Post matni (rasm tagidagi yozuv)…' : "Agentga yozing yoki 📎 bilan post yuboring…"}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onPaste={onPaste}
          onKeyDown={(e) => {
            // Kompyuterda Enter — yuborish, Shift+Enter — yangi qator; telefonda Enter — yangi qator
            if (e.key === 'Enter' && !e.shiftKey && !e.nativeEvent.isComposing && !isTouch()) {
              e.preventDefault()
              submit()
            }
          }}
        />
        <div className="flex items-center gap-1 px-2 pb-2">
          <button
            type="button"
            title="Rasm biriktirish (10 tagacha)"
            onClick={() => fileInput.current?.click()}
            disabled={images.length >= MAX_ALBUM}
            className="flex h-9 w-9 items-center justify-center rounded-full text-lg text-zinc-500 hover:bg-zinc-100 disabled:opacity-40 dark:hover:bg-zinc-800"
          >
            📎
          </button>
          <input
            ref={fileInput}
            type="file"
            accept="image/*"
            multiple
            className="hidden"
            onChange={(e) => {
              addImages([...(e.target.files ?? [])])
              e.target.value = ''
            }}
          />
          {images.length === 0 && (
            <button
              type="button"
              onClick={() => setAsSample(!asSample)}
              className={cx(
                'rounded-full px-3 py-1 text-xs',
                asSample ? 'bg-brand-50 font-medium text-brand-700 dark:bg-brand-700/30 dark:text-brand-100' : 'text-zinc-500 hover:bg-zinc-100 dark:hover:bg-zinc-800',
              )}
            >
              {asSample ? '✓ ' : ''}Rasmsiz post
            </button>
          )}
          <button
            type="button"
            aria-label="Yuborish"
            onClick={submit}
            disabled={!canSend}
            className="ml-auto flex h-9 w-9 items-center justify-center rounded-full bg-brand-500 text-white transition hover:bg-brand-600 disabled:bg-zinc-200 disabled:text-zinc-400 dark:disabled:bg-zinc-800"
          >
            {send.isPending ? '…' : '↑'}
          </button>
        </div>
      </div>
    </div>
  )
}

function SampleCard({ s, compact, onDelete }: { s: Sample; compact?: boolean; onDelete?: () => void }) {
  const [more, setMore] = useState(false)
  const source = s.source === 'own' ? "🏠 O'z kanalimiz" : `📣 ${s.source_name || 'Boshqa kanal'}`
  return (
    <Card className="overflow-hidden p-0">
      <Album images={s.images} compact={compact} />
      <div className="space-y-2 p-3 text-sm">
        <div className="flex items-center justify-between gap-2 text-xs text-zinc-500">
          <span className="truncate">{source}</span>
          {s.analysis === null ? <span className="shrink-0 text-amber-600">⏳ tahlil kutilmoqda</span> : <span className="shrink-0 text-green-700 dark:text-green-400">✓ o'rganildi</span>}
        </div>
        {s.text && <p className={cx('whitespace-pre-wrap', !more && 'line-clamp-5')}>{s.text}</p>}
        {s.image_note && <p className="text-xs text-zinc-500">🖼 {s.image_note}</p>}
        {more && s.analysis && (
          <div className="rounded-lg bg-zinc-50 p-2 text-xs text-zinc-600 dark:bg-zinc-800/60 dark:text-zinc-300">
            {s.image_desc && <p className="mb-1">🖼 {s.image_desc}</p>}
            <p>🤖 {s.analysis}</p>
          </div>
        )}
        <div className="flex items-center justify-between gap-2">
          {(s.text.length > 200 || s.analysis) ? (
            <button className="text-xs text-brand-600 hover:underline" onClick={() => setMore(!more)}>
              {more ? 'Yig\'ish' : s.analysis ? "To'liq va AI tahlili" : "To'liq"}
            </button>
          ) : <span />}
          {onDelete && (
            <ConfirmButton variant="ghost" question="Namunani o'chiramizmi? Agent allaqachon o'rgangan qoidalar qo'llanmada qoladi." onConfirm={onDelete}>
              O'chirish
            </ConfirmButton>
          )}
        </div>
      </div>
    </Card>
  )
}

/** Telegram albomidek: 1 ta — to'liq, ko'p bo'lsa to'r (4 tadan ortig'i «+N») */
function Album({ images, compact }: { images: string[]; compact?: boolean }) {
  if (!images.length) return null
  if (images.length === 1)
    return (
      <a href={images[0]} target="_blank" rel="noreferrer">
        <img src={images[0]} alt="" className={cx('w-full object-cover', compact ? 'max-h-56' : 'max-h-72')} loading="lazy" />
      </a>
    )
  const shown = images.slice(0, 4)
  return (
    <div className={cx('grid gap-0.5', shown.length === 3 ? 'grid-cols-3' : 'grid-cols-2')}>
      {shown.map((url, k) => (
        <a key={url} href={url} target="_blank" rel="noreferrer" className="relative block aspect-square">
          <img src={url} alt="" className="h-full w-full object-cover" loading="lazy" />
          {k === 3 && images.length > 4 && (
            <span className="absolute inset-0 flex items-center justify-center bg-black/50 text-xl font-semibold text-white">+{images.length - 4}</span>
          )}
        </a>
      ))}
    </div>
  )
}

// --- Uslub qo'llanma ---

function GuidePage() {
  const me = useMe()
  const qc = useQueryClient()
  const guide = useQuery({ queryKey: ['guide'], queryFn: () => api.get<{ current: GuideVersion | null; versions: GuideVersion[] }>('/content/guide') })
  const [editing, setEditing] = useState(false)
  const [text, setText] = useState('')
  const [note, setNote] = useState('')
  const [viewing, setViewing] = useState<GuideVersion | null>(null)
  const refresh = () => qc.invalidateQueries({ queryKey: ['guide'] })
  const save = useMutation({
    mutationFn: () => api.put('/content/guide', { text, note }),
    onSuccess: () => {
      setEditing(false)
      refresh()
    },
  })
  const restore = useMutation({ mutationFn: (id: number) => api.post(`/content/guide/${id}/restore`), onSuccess: refresh })

  if (guide.isPending) return <Loading />
  const current = guide.data?.current
  const versions = guide.data?.versions ?? []

  return (
    <div className="space-y-6">
      <ErrorBox error={guide.error ?? restore.error} />
      <Card>
        <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
          <div>
            <div className="font-medium">Joriy qo'llanma</div>
            {current && (
              <div className="text-xs text-zinc-500">
                {formatDate(current.created_at, me.timezone)} · {current.author}
                {current.note ? ` · ${current.note}` : ''}
              </div>
            )}
          </div>
          {!editing && (
            <Button
              variant="secondary"
              onClick={() => {
                setText(current?.text ?? '')
                setNote('')
                setEditing(true)
              }}
            >
              ✏️ {current ? 'Tahrirlash' : 'Qo\'lda yozish'}
            </Button>
          )}
        </div>
        {editing ? (
          <div className="space-y-3">
            <textarea className={cx(inputClass, 'text-sm')} rows={18} value={text} onChange={(e) => setText(e.target.value)} maxLength={20000} />
            <Field label="Nima o'zgardi (ixtiyoriy)">
              <input className={inputClass} value={note} onChange={(e) => setNote(e.target.value)} maxLength={500} />
            </Field>
            <ErrorBox error={save.error} />
            <div className="flex justify-end gap-2">
              <Button variant="secondary" onClick={() => setEditing(false)}>
                Bekor
              </Button>
              <Button onClick={() => save.mutate()} disabled={save.isPending || !text.trim()}>
                Saqlash
              </Button>
            </div>
          </div>
        ) : current ? (
          <div className="text-sm leading-relaxed whitespace-pre-wrap">{current.text}</div>
        ) : (
          <Empty>Hali bo'sh. «💬 O'qitish» bo'limida agentga namuna postlar bering — u qoidalarni o'zi taklif qiladi.</Empty>
        )}
      </Card>

      {versions.length > 1 && (
        <section>
          <h2 className="mb-2 text-sm font-medium text-zinc-500">Tarix</h2>
          <div className="divide-y divide-zinc-200 rounded-xl bg-white ring-1 ring-zinc-200 dark:divide-zinc-800 dark:bg-zinc-900 dark:ring-zinc-800">
            {versions.map((v, k) => (
              <div key={v.id} className="flex flex-wrap items-center justify-between gap-2 px-4 py-3 text-sm">
                <div className="min-w-0">
                  <div className="truncate">
                    #{v.id} · {v.note || "O'zgarish"} {k === 0 && <span className="text-xs text-green-700 dark:text-green-400">(joriy)</span>}
                  </div>
                  <div className="text-xs text-zinc-500">
                    {formatDate(v.created_at, me.timezone)} · {v.author}
                  </div>
                </div>
                <div className="flex gap-1">
                  <Button variant="ghost" onClick={() => setViewing(v)}>
                    Ko'rish
                  </Button>
                  {k > 0 && (
                    <ConfirmButton question={`Qo'llanmani #${v.id}-versiyaga qaytaramizmi? Joriysi tarixda qoladi.`} onConfirm={() => restore.mutate(v.id)} pending={restore.isPending}>
                      Qaytarish
                    </ConfirmButton>
                  )}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {viewing && (
        <Modal title={`Versiya #${viewing.id}`} onClose={() => setViewing(null)}>
          <p className="mb-2 text-xs text-zinc-500">Oldingi versiyaga nisbatan: yashil — qo'shilgan, qizil — olib tashlangan.</p>
          <LineDiff before={versions[versions.indexOf(viewing) + 1]?.text ?? ''} after={viewing.text} />
        </Modal>
      )}
    </div>
  )
}

// --- Namunalar ---

function SamplesPage() {
  const qc = useQueryClient()
  const samples = useQuery({ queryKey: ['samples'], queryFn: () => api.get<Sample[]>('/content/samples') })
  const remove = useMutation({
    mutationFn: (id: number) => api.del(`/content/samples/${id}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['samples'] })
      qc.invalidateQueries({ queryKey: ['train-chat'] })
    },
  })
  if (samples.isPending) return <Loading />
  const list = samples.data ?? []
  return (
    <>
      <ErrorBox error={samples.error ?? remove.error} />
      {list.length ? (
        <>
          <p className="mb-3 text-sm text-zinc-500">
            {list.length} ta namuna · {list.filter((s) => s.analysis !== null).length} tasi o'rganilgan
          </p>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {list.map((s) => (
              <SampleCard key={s.id} s={s} onDelete={() => remove.mutate(s.id)} />
            ))}
          </div>
        </>
      ) : (
        <Empty>Hali namuna yo'q. «💬 O'qitish» bo'limida «📎 Namuna post» orqali qo'shing.</Empty>
      )}
    </>
  )
}

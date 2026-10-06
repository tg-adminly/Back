import { useEffect, useRef, useState, type ClipboardEvent } from 'react'
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

// --- O'qitish chati ---

function TrainChat() {
  const qc = useQueryClient()
  const chat = useQuery({
    queryKey: ['train-chat'],
    queryFn: () => api.get<{ messages: TrainMessage[]; pending_samples: number }>('/content/chat'),
  })
  const send = useMutation({
    mutationFn: (text: string) => api.post<TrainMessage>('/content/chat/message', { text }),
    onSettled: () => {
      qc.invalidateQueries({ queryKey: ['train-chat'] })
      qc.invalidateQueries({ queryKey: ['ai-usage'] })
    },
  })
  const bottom = useRef<HTMLDivElement>(null)
  const count = chat.data?.messages.length ?? 0
  useEffect(() => {
    if (count) bottom.current?.scrollIntoView({ block: 'end' })
  }, [count, send.isPending])

  if (chat.isPending) return <Loading />
  const { messages, pending_samples } = chat.data ?? { messages: [], pending_samples: 0 }

  return (
    <div className="space-y-4">
      <ErrorBox error={chat.error} />
      {messages.length === 0 && (
        <Card className="text-sm text-zinc-600 dark:text-zinc-300">
          <p className="mb-2 font-medium">Agentni shu yerda o'qitamiz 👋</p>
          <ol className="list-decimal space-y-1 pl-5">
            <li>«📎 Namuna post» orqali yoqqan postlarni (rasmi va matni bilan) qo'shing — 10–20 ta yetadi.</li>
            <li>«🔍 Tahlil qilish» ni bosing: agent postlarni o'rganib, o'zi uchun uslub qoidalarini taklif qiladi.</li>
            <li>Taklifni ko'rib, qabul qiling yoki tuzating. Xohlagan payt yozib ko'rsatma bering: «emoji kamroq», «savol bilan tugat»…</li>
          </ol>
        </Card>
      )}
      {messages.map((m) => (
        <MessageRow key={m.id} m={m} />
      ))}
      {send.isPending && (
        <div className="flex">
          <div className="animate-pulse rounded-2xl rounded-bl-sm bg-white px-4 py-2 text-sm text-zinc-500 ring-1 ring-zinc-200 dark:bg-zinc-900 dark:ring-zinc-800">
            🤖 AI o'ylayapti… (30 soniyagacha)
          </div>
        </div>
      )}
      <ErrorBox error={send.error} />
      {pending_samples > 0 && !send.isPending && (
        <div className="flex flex-wrap items-center justify-between gap-2 rounded-xl bg-brand-50 px-4 py-3 text-sm dark:bg-brand-700/20">
          <span>📎 {pending_samples} ta yangi namuna tahlil kutmoqda</span>
          <Button onClick={() => send.mutate('')}>🔍 Tahlil qilish</Button>
        </div>
      )}
      <Composer sending={send.isPending} onSend={(t) => send.mutateAsync(t)} />
      <div ref={bottom} />
    </div>
  )
}

function MessageRow({ m }: { m: TrainMessage }) {
  const me = useMe()
  const mine = m.role === 'user'
  const time = formatDate(m.created_at, me.timezone).split(' ')[1]
  if (m.sample || m.sample_deleted) {
    return (
      <div className="flex justify-end">
        <div className="w-full max-w-md">
          {m.sample ? <SampleCard s={m.sample} compact /> : <div className="rounded-xl px-4 py-2 text-right text-xs text-zinc-400 italic">Namuna o'chirilgan</div>}
          <div className="mt-1 text-right text-xs text-zinc-400">
            {m.author} · {time}
          </div>
        </div>
      </div>
    )
  }
  return (
    <div className={cx('flex', mine && 'justify-end')}>
      <div className="max-w-[85%] sm:max-w-lg">
        <div
          className={cx(
            'rounded-2xl px-4 py-2 text-sm whitespace-pre-wrap',
            mine ? 'rounded-br-sm bg-brand-500 text-white' : 'rounded-bl-sm bg-white ring-1 ring-zinc-200 dark:bg-zinc-900 dark:ring-zinc-800',
          )}
        >
          {m.text}
        </div>
        {m.proposal && <ProposalBox m={m} />}
        <div className={cx('mt-1 text-xs text-zinc-400', mine && 'text-right')}>
          {mine ? m.author : '🤖 AI'} · {time}
        </div>
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

function Composer({ sending, onSend }: { sending: boolean; onSend: (text: string) => Promise<unknown> }) {
  const [mode, setMode] = useState<'message' | 'sample'>('sample')
  const [text, setText] = useState('')
  return (
    <Card className="space-y-3">
      <div className="flex gap-1">
        {(
          [
            ['sample', '📎 Namuna post'],
            ['message', '💬 Xabar'],
          ] as const
        ).map(([k, label]) => (
          <button
            key={k}
            onClick={() => setMode(k)}
            className={cx('rounded-full px-3 py-1 text-sm', mode === k ? 'bg-brand-50 font-medium text-brand-700 dark:bg-brand-700/20 dark:text-brand-100' : 'text-zinc-500 hover:bg-zinc-100 dark:hover:bg-zinc-800')}
          >
            {label}
          </button>
        ))}
      </div>
      {mode === 'sample' ? (
        <SampleForm />
      ) : (
        <form
          className="space-y-2"
          onSubmit={(e) => {
            e.preventDefault()
            if (text.trim()) onSend(text).then(() => setText(''), () => {})
          }}
        >
          <textarea
            className={inputClass}
            rows={3}
            maxLength={5000}
            placeholder="Masalan: «Emojini kamroq ishlat», «Har postni savol bilan tugat», «Bu postlarda nimasi yaxshi?»"
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) e.currentTarget.form?.requestSubmit()
            }}
          />
          <div className="flex justify-end">
            <Button type="submit" disabled={sending || !text.trim()}>
              Yuborish
            </Button>
          </div>
        </form>
      )}
    </Card>
  )
}

function SampleForm() {
  const qc = useQueryClient()
  const [text, setText] = useState('')
  const [images, setImages] = useState<File[]>([])
  const [previews, setPreviews] = useState<string[]>([])
  const [note, setNote] = useState('')
  const [own, setOwn] = useState(false)
  const [sourceName, setSourceName] = useState('')
  const fileInput = useRef<HTMLInputElement>(null)

  useEffect(() => {
    const urls = images.map((f) => URL.createObjectURL(f))
    setPreviews(urls)
    return () => urls.forEach((u) => URL.revokeObjectURL(u))
  }, [images])

  // Telegram albomi kabi: 10 tagacha, qo'shilgan tartibda
  const addImages = (files: File[]) => setImages((prev) => [...prev, ...files.filter((f) => f.type.startsWith('image/'))].slice(0, MAX_ALBUM))

  const add = useMutation({
    mutationFn: () => {
      const form = new FormData()
      form.append('text', text)
      form.append('source', own ? 'own' : 'other')
      form.append('source_name', own ? '' : sourceName)
      form.append('image_note', note)
      images.forEach((f) => form.append('images', f))
      return api.post<TrainMessage>('/content/chat/sample', form)
    },
    onSuccess: () => {
      // Manba qoladi — bir kanaldan ketma-ket bir nechta post qo'shiladi
      setText('')
      setImages([])
      setNote('')
      if (fileInput.current) fileInput.current.value = ''
      qc.invalidateQueries({ queryKey: ['train-chat'] })
      qc.invalidateQueries({ queryKey: ['samples'] })
    },
  })

  const onPaste = (e: ClipboardEvent) => {
    const files = [...e.clipboardData.files].filter((f) => f.type.startsWith('image/'))
    if (files.length) {
      e.preventDefault()
      addImages(files)
    }
  }

  return (
    <form
      className="space-y-3"
      onSubmit={(e) => {
        e.preventDefault()
        add.mutate()
      }}
    >
      <textarea
        className={inputClass}
        rows={4}
        maxLength={5000}
        placeholder="Post matni (rasmlarni shu yerga Ctrl+V bilan qo'yish ham mumkin)"
        value={text}
        onChange={(e) => setText(e.target.value)}
        onPaste={onPaste}
      />
      <div className="flex flex-wrap gap-2">
        {previews.map((url, k) => (
          <div key={url} className="relative h-20 w-20 overflow-hidden rounded-lg ring-1 ring-zinc-200 dark:ring-zinc-700">
            <img src={url} alt="" className="h-full w-full object-cover" />
            <span className="absolute top-1 left-1 rounded bg-black/60 px-1 text-[10px] text-white">{k + 1}</span>
            <button
              type="button"
              aria-label="Olib tashlash"
              onClick={() => setImages(images.filter((_, i) => i !== k))}
              className="absolute top-1 right-1 flex h-5 w-5 items-center justify-center rounded-full bg-black/60 text-xs text-white hover:bg-red-600"
            >
              ×
            </button>
          </div>
        ))}
        {images.length < MAX_ALBUM && (
          <button
            type="button"
            onClick={() => fileInput.current?.click()}
            className="flex h-20 w-20 flex-col items-center justify-center rounded-lg bg-zinc-100 text-xs text-zinc-500 ring-1 ring-zinc-200 hover:bg-zinc-200 dark:bg-zinc-800 dark:ring-zinc-700"
          >
            <span className="text-lg">🖼</span>
            {images.length ? '+ Yana' : 'Rasmlar'}
          </button>
        )}
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
      </div>
      {images.length > 0 && (
        <input
          className={inputClass}
          placeholder="Rasmlar tavsifi (ixtiyoriy) — masalan: «qizil fonda atir, gul barglari»"
          value={note}
          onChange={(e) => setNote(e.target.value)}
          maxLength={1000}
        />
      )}
      <div className="flex flex-wrap items-center gap-3">
        <label className="flex items-center gap-2 text-sm">
          <input type="checkbox" checked={own} onChange={(e) => setOwn(e.target.checked)} className="accent-brand-500" />
          O'z kanalimizdan
        </label>
        {!own && <input className={cx(inputClass, 'sm:max-w-60')} placeholder="Qaysi kanaldan (ixtiyoriy)" value={sourceName} onChange={(e) => setSourceName(e.target.value)} maxLength={255} />}
        <Button type="submit" className="ml-auto" disabled={add.isPending || (!text.trim() && !images.length)}>
          {add.isPending ? 'Qo\'shilmoqda…' : 'Qo\'shish'}
        </Button>
      </div>
      <ErrorBox error={add.error} />
    </form>
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

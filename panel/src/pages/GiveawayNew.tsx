import { useEffect, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { ApiError, api, type Prize, type Sponsor } from '../api'
import { Button, Card, DrawModePicker, ErrorBox, Field, Modal, PageHeader, endsAtLabel, inputClass } from '../ui'
import { SponsorAddForm } from './Sponsors'

interface Preview {
  errors: Record<string, string>
  prizes: (Prize | null)[]
  post_html: string | null
}

function defaultEndsAt() {
  const d = new Date(Date.now() + 24 * 3600 * 1000)
  d.setMinutes(0, 0, 0)
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:00`
}

export default function GiveawayNew() {
  const navigate = useNavigate()
  const qc = useQueryClient()
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [prizes, setPrizes] = useState<string[]>([''])
  const [endsAt, setEndsAt] = useState(defaultEndsAt)
  const [sponsorIds, setSponsorIds] = useState<number[]>([])
  const [autoDraw, setAutoDraw] = useState(false)
  const [addingSponsor, setAddingSponsor] = useState(false)
  const [preview, setPreview] = useState<Preview | null>(null)
  const [confirming, setConfirming] = useState(false)

  const sponsors = useQuery({ queryKey: ['sponsors'], queryFn: () => api.get<Sponsor[]>('/sponsors') })
  const body = { title, description, prizes, ends_at: endsAt, sponsor_ids: sponsorIds, auto_draw: autoDraw }
  const chosen = (sponsors.data ?? []).filter((s) => sponsorIds.includes(s.id))
  const bodyKey = JSON.stringify(body)

  // Yozish to'xtagach 400 ms o'tib post ko'rinishini yangilaymiz
  useEffect(() => {
    const t = setTimeout(() => {
      api.post<Preview>('/giveaways/preview', JSON.parse(bodyKey)).then(setPreview).catch(() => {})
    }, 400)
    return () => clearTimeout(t)
  }, [bodyKey])

  const publish = useMutation({
    mutationFn: () => api.post<{ id: number }>('/giveaways', body),
    onSuccess: (r) => {
      qc.invalidateQueries({ queryKey: ['giveaways'] })
      qc.invalidateQueries({ queryKey: ['stats'] })
      navigate(`/giveaways/${r.id}`)
    },
    onSettled: () => setConfirming(false),
  })

  const setCount = (n: number) => {
    const count = Math.max(1, Math.min(100, n || 1))
    setPrizes((p) => (count > p.length ? [...p, ...Array(count - p.length).fill(p[p.length - 1] ?? '')] : p.slice(0, count)))
  }
  const setPrize = (i: number, v: string) => setPrizes((p) => p.map((x, j) => (j === i ? v : x)))
  const fillRest = (i: number) => setPrizes((p) => p.map((x, j) => (j > i ? p[i] : x)))

  // Serverdan kelgan xatolar: bo'sh maydonlarni yozilmaguncha xato demaymiz
  const serverErrors = publish.error instanceof ApiError ? publish.error.fields : {}
  const err = (key: string, value: string) => serverErrors[key] ?? (value.trim() ? preview?.errors[key] : undefined)
  const ready = preview !== null && Object.keys(preview.errors).length === 0

  return (
    <>
      <PageHeader title="Yangi rozigrish" />
      <div className="grid gap-6 lg:grid-cols-[1fr_380px]">
        <div className="space-y-5">
          <Card className="space-y-4">
            <Field label="Nomi" error={err('title', title)}>
              <input className={inputClass} value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Kuzgi rozigrish" maxLength={255} />
            </Field>
            <Field label="Post matni" hint="Qisqa ta'rif, qo'shimcha shartlar" error={err('description', description)}>
              <textarea className={inputClass} rows={4} value={description} onChange={(e) => setDescription(e.target.value)} maxLength={3000} />
            </Field>
            <div>
              <div className="mb-1 text-sm font-medium">G'olibni kim aniqlaydi</div>
              <DrawModePicker value={autoDraw} onChange={setAutoDraw} />
            </div>
            <Field label={endsAtLabel(autoDraw)} error={serverErrors.ends_at ?? preview?.errors.ends_at}>
              <input type="datetime-local" className={inputClass} value={endsAt} onChange={(e) => setEndsAt(e.target.value)} />
            </Field>
          </Card>

          <Card className="space-y-3">
            <div className="flex items-center justify-between gap-3">
              <div>
                <div className="text-sm font-medium">Sovrinlar</div>
                <div className="text-xs text-zinc-500">Summa: 500000, 500 ming, 1.5 mln · yoki sovg'a nomi: iPhone 15</div>
              </div>
              <label className="flex items-center gap-2 text-sm">
                O'rinlar:
                <input
                  type="number"
                  min={1}
                  max={100}
                  className={inputClass + ' w-20'}
                  value={prizes.length}
                  onChange={(e) => setCount(parseInt(e.target.value))}
                />
              </label>
            </div>
            {prizes.map((p, i) => (
              <div key={i}>
                <div className="flex items-center gap-2">
                  <span className="w-14 shrink-0 text-sm text-zinc-500">{i + 1}-o'rin</span>
                  <input className={inputClass} value={p} onChange={(e) => setPrize(i, e.target.value)} placeholder={i === 0 ? 'iPhone 15' : '500 ming'} />
                  {i < prizes.length - 1 && p.trim() && (
                    <button type="button" onClick={() => fillRest(i)} className="shrink-0 rounded-md px-2 py-1 text-xs text-brand-600 hover:bg-brand-50 dark:hover:bg-zinc-800" title="Keyingi o'rinlarga ham shu sovrin">
                      ↓ Qolganlariga
                    </button>
                  )}
                </div>
                <div className="ml-16 text-xs">
                  {err(`prizes.${i}`, p) ? (
                    <span className="text-red-600">{err(`prizes.${i}`, p)}</span>
                  ) : preview?.prizes[i] && p.trim() ? (
                    <span className="text-zinc-500">
                      {preview.prizes[i]!.type === 'money' ? '💵' : '🎁'} {preview.prizes[i]!.label}
                    </span>
                  ) : null}
                </div>
              </div>
            ))}
          </Card>

          <Card className="space-y-3">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm font-medium">Homiy kanallar</div>
                <div className="text-xs text-zinc-500">Bizning kanal avtomatik shart. Bot har bir homiy kanalda admin bo'lishi kerak.</div>
              </div>
              <Button variant="ghost" onClick={() => setAddingSponsor(true)}>
                + Qo'shish
              </Button>
            </div>
            {chosen.length ? (
              <div className="space-y-1">
                {chosen.map((s) => (
                  <div key={s.id} className="flex items-center gap-3 rounded-lg px-2 py-1.5">
                    <div className="min-w-0 flex-1">
                      <div className="truncate text-sm">{s.title}</div>
                      <div className="truncate text-xs text-zinc-400">{s.link}</div>
                    </div>
                    <button
                      type="button"
                      className="text-lg leading-none text-zinc-400 hover:text-red-600"
                      aria-label="Olib tashlash"
                      onClick={() => setSponsorIds((ids) => ids.filter((x) => x !== s.id))}
                    >
                      ×
                    </button>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-sm text-zinc-500">Homiysiz ham bo'ladi.</div>
            )}
          </Card>
        </div>

        <div className="lg:sticky lg:top-8 lg:self-start">
          <div className="mb-2 text-sm font-medium">Kanalda shunday ko'rinadi</div>
          <PostPreview html={preview?.post_html ?? null} sponsors={chosen} />
          <div className="mt-4 space-y-3">
            <ErrorBox error={publish.error} />
            <Button className="w-full" disabled={!ready || publish.isPending} onClick={() => setConfirming(true)}>
              📢 Kanalga e'lon qilish
            </Button>
          </div>
        </div>
      </div>

      {addingSponsor && (
        <Modal title="Homiy kanal qo'shish" onClose={() => setAddingSponsor(false)}>
          <SponsorModalBody
            sponsors={(sponsors.data ?? []).filter((s) => !sponsorIds.includes(s.id))}
            onChoose={(ids) => {
              setSponsorIds((cur) => [...cur, ...ids.filter((id) => !cur.includes(id))])
              setAddingSponsor(false)
            }}
          />
        </Modal>
      )}
      {confirming && (
        <Modal title="E'lon qilaymi?" onClose={() => setConfirming(false)}>
          <p className="mb-5 text-sm">Post darhol kanalga chiqadi. Keyin sovrin va shartlarni o'zgartirib bo'lmaydi (vaqt va g'olibni aniqlash usulini — mumkin).</p>
          <div className="flex justify-end gap-2">
            <Button variant="secondary" onClick={() => setConfirming(false)}>
              Orqaga
            </Button>
            <Button disabled={publish.isPending} onClick={() => publish.mutate()}>
              {publish.isPending ? 'Chiqarilmoqda…' : "Ha, e'lon qilish"}
            </Button>
          </div>
        </Modal>
      )}
    </>
  )
}

export function PostPreview({ html, sponsors, count = 0 }: { html: string | null; sponsors: Sponsor[]; count?: number }) {
  return (
    <div className="rounded-2xl bg-sky-100/60 p-3 dark:bg-sky-950/40">
      <div className="rounded-xl bg-white p-3 text-sm leading-relaxed shadow-sm dark:bg-zinc-900">
        {html ? (
          // Matn serverda html.escape qilingan, faqat Telegram teglari qoladi
          <div className="break-words whitespace-pre-wrap [&_a]:text-sky-600 [&_code]:rounded [&_code]:bg-zinc-100 [&_code]:px-1 [&_code]:text-xs [&_code]:break-all dark:[&_code]:bg-zinc-800" dangerouslySetInnerHTML={{ __html: html }} />
        ) : (
          <div className="py-8 text-center text-zinc-400">Maydonlarni to'ldiring — post shu yerda ko'rinadi</div>
        )}
      </div>
      <div className="mt-1 space-y-1">
        {sponsors.map((s) => (
          <div key={s.id} className="rounded-lg bg-white/70 py-1.5 text-center text-xs font-medium text-sky-700 dark:bg-zinc-800/70 dark:text-sky-300">
            ➕ {s.title}
          </div>
        ))}
        <div className="rounded-lg bg-white/70 py-1.5 text-center text-xs font-medium text-sky-700 dark:bg-zinc-800/70 dark:text-sky-300">
          🎁 Qatnashish{count ? ` (${count})` : ''}
        </div>
      </div>
    </div>
  )
}

/** Homiy qo'shish oynasi: eski homiylardan tanlash yoki yangisini qo'shish */
function SponsorModalBody({ sponsors, onChoose }: { sponsors: Sponsor[]; onChoose: (ids: number[]) => void }) {
  const [picking, setPicking] = useState(false)

  if (picking) return <OldSponsorPicker sponsors={sponsors} onChoose={onChoose} onBack={() => setPicking(false)} />
  return (
    <div className="space-y-4">
      {sponsors.length > 0 && (
        <>
          <Button variant="secondary" className="w-full" onClick={() => setPicking(true)}>
            📋 Eski homiylardan tanlash ({sponsors.length})
          </Button>
          <div className="flex items-center gap-3 text-xs text-zinc-400">
            <div className="h-px flex-1 bg-zinc-200 dark:bg-zinc-700" />
            yoki yangi homiy qo'shing
            <div className="h-px flex-1 bg-zinc-200 dark:bg-zinc-700" />
          </div>
        </>
      )}
      <SponsorAddForm onAdded={(s) => onChoose([s.id])} />
    </div>
  )
}

function OldSponsorPicker({ sponsors, onChoose, onBack }: { sponsors: Sponsor[]; onChoose: (ids: number[]) => void; onBack: () => void }) {
  const [q, setQ] = useState('')
  const [ids, setIds] = useState<number[]>([])
  const needle = q.trim().toLowerCase().replace(/^@/, '')
  const found = sponsors.filter((s) => !needle || s.title.toLowerCase().includes(needle) || s.link.toLowerCase().includes(needle))

  return (
    <div className="space-y-3">
      <input
        className={inputClass}
        value={q}
        onChange={(e) => setQ(e.target.value)}
        onKeyDown={(e) => e.key === 'Escape' && onBack()}
        placeholder="Homiy nomi bo'yicha qidirish…"
        autoFocus
      />
      {found.length ? (
        <div className="max-h-72 space-y-0.5 overflow-y-auto">
          {found.map((s) => (
            <label key={s.id} className="flex items-center gap-3 rounded-lg px-2 py-1.5 hover:bg-zinc-50 dark:hover:bg-zinc-800">
              <input
                type="checkbox"
                className="accent-brand-500"
                checked={ids.includes(s.id)}
                onChange={(e) => setIds((cur) => (e.target.checked ? [...cur, s.id] : cur.filter((x) => x !== s.id)))}
              />
              <div className="min-w-0 flex-1">
                <div className="truncate text-sm">{s.title}</div>
                <div className="truncate text-xs text-zinc-400">{s.link}</div>
              </div>
            </label>
          ))}
        </div>
      ) : (
        <p className="py-2 text-sm text-zinc-500">Hech narsa topilmadi.</p>
      )}
      <div className="flex gap-2">
        <Button variant="ghost" onClick={onBack}>
          ← Orqaga
        </Button>
        <Button className="flex-1" disabled={!ids.length} onClick={() => onChoose(ids)}>
          Qo'shish{ids.length ? ` (${ids.length})` : ''}
        </Button>
      </div>
    </div>
  )
}

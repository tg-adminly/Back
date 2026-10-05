import { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api, type BotChat, type Sponsor } from '../api'
import { Button, Card, ConfirmButton, Empty, ErrorBox, Field, Loading, PageHeader, inputClass } from '../ui'

export default function Sponsors() {
  const qc = useQueryClient()
  const list = useQuery({ queryKey: ['sponsors'], queryFn: () => api.get<Sponsor[]>('/sponsors') })
  const remove = useMutation({
    mutationFn: (id: number) => api.del(`/sponsors/${id}`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['sponsors'] }),
  })

  return (
    <>
      <PageHeader title="Homiy kanallar" />
      <div className="grid gap-6 lg:grid-cols-[1fr_360px]">
        <div>
          <ErrorBox error={list.error ?? remove.error} />
          {list.isPending ? (
            <Loading />
          ) : list.data?.length ? (
            <Card className="divide-y divide-zinc-100 p-0 dark:divide-zinc-800">
              {list.data.map((s) => (
                <div key={s.id} className="flex items-center gap-3 px-4 py-3">
                  <div className="min-w-0 flex-1">
                    <div className="truncate font-medium">{s.title}</div>
                    <a href={s.link} target="_blank" rel="noopener" className="block truncate text-xs text-brand-600 hover:underline">
                      {s.link}
                    </a>
                  </div>
                  <ConfirmButton variant="danger" question={`«${s.title}» ni homiylar ro'yxatidan o'chiraymi?`} onConfirm={() => remove.mutate(s.id)}>
                    O'chirish
                  </ConfirmButton>
                </div>
              ))}
            </Card>
          ) : (
            <Empty>Hali homiy kanal qo'shilmagan.</Empty>
          )}
        </div>
        <Card>
          <h2 className="mb-3 font-semibold">Yangi homiy</h2>
          <SponsorAddForm />
        </Card>
      </div>
    </>
  )
}

type Kind = 'public' | 'private'

export function SponsorAddForm({ onAdded }: { onAdded?: (s: Sponsor) => void }) {
  const qc = useQueryClient()
  const [kind, setKind] = useState<Kind>('public')
  const [ref, setRef] = useState('')
  const [link, setLink] = useState('')
  const [manualId, setManualId] = useState(false)
  const [picking, setPicking] = useState(false)
  const [picked, setPicked] = useState<BotChat | null>(null)
  const add = useMutation({
    mutationFn: () => api.post<Sponsor>('/sponsors', { ref, link: kind === 'private' ? link : null }),
    onSuccess: (s) => {
      qc.invalidateQueries({ queryKey: ['sponsors'] })
      qc.invalidateQueries({ queryKey: ['bot-chats'] })
      setRef('')
      setLink('')
      setPicked(null)
      onAdded?.(s)
    },
  })

  const switchKind = (k: Kind) => {
    setKind(k)
    setRef('')
    setLink('')
    setManualId(false)
    setPicking(false)
    setPicked(null)
    add.reset()
  }
  const isInvite = /t\.me\/(\+|joinchat\/)/.test(ref)
  const ready = kind === 'public' ? ref.trim() && !isInvite : ref.trim() && link.trim()

  return (
    <form
      className="space-y-3"
      onSubmit={(e) => {
        e.preventDefault()
        add.mutate()
      }}
    >
      <div className="grid grid-cols-2 gap-1 rounded-lg bg-zinc-100 p-1 text-sm dark:bg-zinc-800">
        {(['public', 'private'] as const).map((k) => (
          <button
            key={k}
            type="button"
            onClick={() => switchKind(k)}
            className={`rounded-md px-3 py-1.5 font-medium transition ${kind === k ? 'bg-white shadow-sm dark:bg-zinc-900' : 'text-zinc-500'}`}
          >
            {k === 'public' ? 'Ochiq kanal' : 'Yopiq kanal'}
          </button>
        ))}
      </div>

      {kind === 'public' ? (
        <>
          <ol className="list-decimal space-y-1 pl-5 text-xs text-zinc-500">
            <li>Botni homiy kanalga <b>admin</b> qilib qo'shing (obunani tekshirish uchun).</li>
            <li>Kanal @username'ini yoki linkini yozing.</li>
          </ol>
          <Field
            label="Kanal"
            error={isInvite ? "Bu yopiq kanal linki — yuqorida «Yopiq kanal» ni tanlang." : undefined}
          >
            <input className={inputClass} value={ref} onChange={(e) => setRef(e.target.value)} placeholder="@homiy_kanal yoki https://t.me/homiy_kanal" required />
          </Field>
        </>
      ) : (
        <>
          <div>
            <div className="mb-1 text-sm font-medium">1. Botni kanalga admin qiling</div>
            <p className="text-xs text-zinc-500">
              Kanal → Tahrirlash → Administratorlar → Admin qo'shish → botni toping. Shundan so'ng kanal pastdagi ro'yxatda o'zi paydo bo'ladi.
            </p>
          </div>

          <div>
            <div className="mb-1 text-sm font-medium">2. Kanal</div>
            {manualId ? (
              <input className={inputClass} value={ref} onChange={(e) => setRef(e.target.value)} placeholder="-1001234567890" autoFocus />
            ) : picking ? (
              <ChatPicker
                onPick={(c) => {
                  setPicked(c)
                  setRef(String(c.chat_id))
                  setPicking(false)
                }}
                onClose={() => setPicking(false)}
              />
            ) : picked ? (
              <div className="flex items-center gap-2 rounded-lg px-3 py-2 ring-1 ring-zinc-300 dark:ring-zinc-700">
                <span className="min-w-0 flex-1 truncate text-sm font-medium">{picked.title}</span>
                <button type="button" className="text-xs text-brand-600 hover:underline" onClick={() => setPicking(true)}>
                  O'zgartirish
                </button>
              </div>
            ) : (
              <Button type="button" variant="ghost" className="w-full ring-1 ring-zinc-300 dark:ring-zinc-700" onClick={() => setPicking(true)}>
                🔍 Kanalni tanlash
              </Button>
            )}
            {!picking && (
              <button
                type="button"
                className="mt-1 text-xs text-zinc-500 underline hover:text-zinc-700"
                onClick={() => {
                  setManualId((v) => !v)
                  setRef('')
                  setPicked(null)
                }}
              >
                {manualId ? "Ro'yxatdan tanlash" : "yoki kanal ID'sini yozish"}
              </button>
            )}
          </div>

          <Field label="3. Taklif havolasi" hint="Kanal → Tahrirlash → Taklif havolalari (Invite links) → havolani nusxalang.">
            <input className={inputClass} value={link} onChange={(e) => setLink(e.target.value)} placeholder="https://t.me/+AbCdEf..." required />
          </Field>
        </>
      )}

      <ErrorBox error={add.error} />
      <Button type="submit" className="w-full" disabled={!ready || add.isPending}>
        {add.isPending ? 'Tekshirilmoqda…' : "Tekshirib qo'shish"}
      </Button>
    </form>
  )
}

function ChatPicker({ onPick, onClose }: { onPick: (c: BotChat) => void; onClose: () => void }) {
  const [q, setQ] = useState('')
  const chats = useQuery({ queryKey: ['bot-chats'], queryFn: () => api.get<BotChat[]>('/bot-chats'), refetchInterval: 5_000 })
  const needle = q.trim().toLowerCase().replace(/^@/, '')
  const found = (chats.data ?? []).filter(
    (c) => !needle || c.title.toLowerCase().includes(needle) || c.username?.toLowerCase().includes(needle),
  )

  return (
    <div className="space-y-2 rounded-lg p-2 ring-1 ring-zinc-300 dark:ring-zinc-700">
      <input
        className={inputClass}
        value={q}
        onChange={(e) => setQ(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === 'Escape') onClose()
          if (e.key === 'Enter') {
            e.preventDefault() // formani yubormasin
            if (found[0]) onPick(found[0])
          }
        }}
        placeholder="Kanal nomi bo'yicha qidirish…"
        autoFocus
      />
      {chats.isPending ? (
        <Loading />
      ) : found.length ? (
        <div className="max-h-56 space-y-0.5 overflow-y-auto">
          {found.map((c) => (
            <button
              key={c.chat_id}
              type="button"
              onClick={() => onPick(c)}
              className="flex w-full items-center gap-3 rounded-md px-2 py-1.5 text-left hover:bg-zinc-100 dark:hover:bg-zinc-800"
            >
              <span className="min-w-0 flex-1 truncate text-sm">{c.title}</span>
              {c.username && <span className="text-xs text-zinc-400">@{c.username}</span>}
            </button>
          ))}
        </div>
      ) : (
        <p className="px-1 py-2 text-xs text-zinc-500">
          {chats.data?.length
            ? 'Hech narsa topilmadi.'
            : "Bot admin bo'lgan kanal hali yo'q. Botni admin qilganingizdan keyin bir necha soniyada shu yerda chiqadi. Bot oldindan admin bo'lsa — adminlikdan olib, qaytadan admin qiling."}
        </p>
      )}
      <div className="text-right">
        <button type="button" className="text-xs text-zinc-500 hover:underline" onClick={onClose}>
          Yopish
        </button>
      </div>
    </div>
  )
}

import { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { api, type PayoutDetails, type Winner } from '../api'
import { Button, Card, CopyButton, Empty, ErrorBox, Field, Loading, Modal, PageHeader, WinnerBadge, cx, formatDate, inputClass, useMe, userLabel } from '../ui'

const STEP: Record<string, string> = {
  card: 'karta raqami',
  card_holder: 'karta egasi ismi',
  full_name: 'ism-familiya',
  phone: 'telefon',
  address: 'manzil',
}

export default function Payouts() {
  const [tab, setTab] = useState<'open' | 'done'>('open')
  const list = useQuery({
    queryKey: ['payouts', tab],
    queryFn: () => api.get<Winner[]>(`/payouts?status=${tab}`),
    refetchInterval: tab === 'open' ? 15_000 : false,
  })

  return (
    <>
      <PageHeader title="To'lovlar va sovg'alar" />
      <div className="mb-4 flex gap-1">
        {(['open', 'done'] as const).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={cx(
              'rounded-full px-3 py-1 text-sm',
              tab === t ? 'bg-zinc-900 text-white dark:bg-white dark:text-zinc-900' : 'text-zinc-600 hover:bg-zinc-100 dark:text-zinc-300 dark:hover:bg-zinc-800',
            )}
          >
            {t === 'open' ? 'Ochiq' : 'Topshirilgan'}
          </button>
        ))}
      </div>
      <ErrorBox error={list.error} />
      {list.isPending ? (
        <Loading />
      ) : list.data?.length ? (
        <div className="space-y-8">
          {byGiveaway(list.data).map((group) => (
            <GiveawayGroup key={group[0].giveaway_id} winners={group} open={tab === 'open'} />
          ))}
        </div>
      ) : (
        <Empty>{tab === 'open' ? "Ochiq to'lov yo'q ✅" : "Hali hech narsa topshirilmagan."}</Empty>
      )}
    </>
  )
}

/** Rozigrishlar bo'yicha guruhlaydi: yangisi tepada, ichida o'rin tartibida */
function byGiveaway(winners: Winner[]): Winner[][] {
  const groups = new Map<number, Winner[]>()
  for (const w of winners) groups.set(w.giveaway_id, [...(groups.get(w.giveaway_id) ?? []), w])
  return [...groups.values()].sort((a, b) => b[0].giveaway_id - a[0].giveaway_id).map((g) => g.sort((a, b) => a.place - b.place))
}

const sum = (n: number) => `${String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ' ')} so'm`

function GiveawayGroup({ winners, open }: { winners: Winner[]; open: boolean }) {
  const first = winners[0]
  const waiting = winners.filter((w) => w.status === 'awaiting_info').length
  const ready = winners.filter((w) => w.status === 'info_received').length
  const money = winners.reduce((acc, w) => acc + (w.prize.type === 'money' ? (w.prize.amount ?? 0) : 0), 0)
  return (
    <section>
      <div className="mb-3 flex flex-wrap items-baseline gap-x-3 gap-y-1 border-b border-zinc-200 pb-2 dark:border-zinc-800">
        <Link to={`/giveaways/${first.giveaway_id}`} className="min-w-0 truncate text-lg font-semibold hover:text-brand-600">
          🎁 {first.giveaway_title} <span className="text-sm font-normal text-zinc-400">#{first.giveaway_id}</span>
        </Link>
        <div className="flex flex-wrap gap-x-3 gap-y-1 text-sm text-zinc-500">
          {open ? (
            <>
              {ready > 0 && <span className="text-brand-600">💳 {ready} ta to'lashga tayyor</span>}
              {waiting > 0 && <span>⏳ {waiting} ta ma'lumot kutilmoqda</span>}
            </>
          ) : (
            <span>✅ {winners.length} ta topshirilgan</span>
          )}
          {money > 0 && <span>💵 jami {sum(money)}</span>}
        </div>
      </div>
      <div className="grid gap-3 md:grid-cols-2">
        {winners.map((w) => (
          <PayoutCard key={w.id} w={w} />
        ))}
      </div>
    </section>
  )
}

function PayoutCard({ w }: { w: Winner }) {
  const me = useMe()
  const [details, setDetails] = useState<PayoutDetails | null>(null)
  const [delivering, setDelivering] = useState(false)
  const reveal = useMutation({
    mutationFn: () => api.get<PayoutDetails>(`/payouts/${w.id}/details`),
    onSuccess: setDetails,
  })
  const money = w.prize.type === 'money'

  return (
    <Card>
      <div className="mb-2 flex items-start justify-between gap-2">
        <div className="min-w-0">
          <div className="text-xs text-zinc-500">
            {w.place}-o'rin · #{w.number}
          </div>
          <div className="truncate font-medium">
            <a href={`tg://user?id=${w.user_id}`} className="hover:text-brand-600">
              {userLabel(w.name, w.username)}
            </a>
          </div>
        </div>
        <WinnerBadge status={w.status} />
      </div>
      <div className="mb-3 text-lg font-semibold">
        {money ? '💵' : '🎁'} {w.prize.label}
      </div>

      {w.status === 'awaiting_info' && (
        <p className="text-sm text-zinc-500">⏳ G'olib hali ma'lumot yubormagan{w.claim_step ? ` (kutilmoqda: ${STEP[w.claim_step] ?? w.claim_step})` : ''}.</p>
      )}

      {w.status === 'info_received' && (
        <>
          {details ? (
            <dl className="mb-3 space-y-1 rounded-lg bg-zinc-50 p-3 text-sm dark:bg-zinc-800/60">
              {money ? (
                <>
                  <Row label="Karta" value={details.card} mono />
                  <Row label="Egasi" value={details.card_holder} />
                </>
              ) : (
                <>
                  <Row label="Ism" value={details.full_name} />
                  <Row label="Telefon" value={details.phone} mono />
                  <Row label="Manzil" value={details.address} />
                </>
              )}
            </dl>
          ) : (
            <div className="mb-3 flex items-center justify-between text-sm">
              <span className="text-zinc-500">{money ? `Karta: ${w.card_masked}` : "Manzil ma'lumotlari tayyor"}</span>
              <Button variant="ghost" onClick={() => reveal.mutate()} disabled={reveal.isPending}>
                👁 Ko'rsatish
              </Button>
            </div>
          )}
          <ErrorBox error={reveal.error} />
          <Button className="w-full" onClick={() => setDelivering(true)}>
            {money ? "✅ To'landi" : '✅ Yuborildi'}
          </Button>
        </>
      )}

      {w.status === 'done' && w.done_at && <p className="text-sm text-zinc-500">✅ {formatDate(w.done_at, me.timezone)} da topshirildi</p>}

      {delivering && <DeliverModal w={w} onClose={() => setDelivering(false)} />}
    </Card>
  )
}

function Row({ label, value, mono }: { label: string; value?: string; mono?: boolean }) {
  return (
    <div className="flex items-start gap-2">
      <dt className="w-16 shrink-0 text-zinc-500">{label}</dt>
      <dd className={cx('min-w-0 flex-1 break-words', mono && 'font-mono')}>{value}</dd>
      {value && <CopyButton value={value} />}
    </div>
  )
}

function DeliverModal({ w, onClose }: { w: Winner; onClose: () => void }) {
  const qc = useQueryClient()
  const [file, setFile] = useState<File | null>(null)
  const [note, setNote] = useState('')
  const money = w.prize.type === 'money'
  const deliver = useMutation({
    mutationFn: () => {
      const form = new FormData()
      if (file) form.append('proof', file)
      form.append('note', note)
      return api.post<{ delivered: boolean }>(`/payouts/${w.id}/deliver`, form)
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['payouts'] })
      qc.invalidateQueries({ queryKey: ['stats'] })
    },
  })

  if (deliver.data) {
    return (
      <Modal title="Tayyor" onClose={onClose}>
        <p className="mb-5 text-sm">
          {deliver.data.delivered
            ? "✅ G'olibga chek va tabrik yuborildi. Shaxsiy ma'lumotlari o'chirildi."
            : "⚠️ Holat yopildi, lekin g'olibga yuborib bo'lmadi (botni bloklagan bo'lishi mumkin). Unga o'zingiz yozing."}
        </p>
        <div className="text-right">
          <Button onClick={onClose}>Yopish</Button>
        </div>
      </Modal>
    )
  }

  return (
    <Modal title={money ? "To'lov cheki" : "Yuborilganini tasdiqlash"} onClose={onClose}>
      <div className="space-y-4">
        <p className="text-sm text-zinc-600 dark:text-zinc-400">
          {userLabel(w.name, w.username)} — {w.prize.label}. {money ? 'Chek' : 'Kvitansiya'} va izoh g'olibga bot orqali yuboriladi, shaxsiy ma'lumotlari o'chiriladi.
        </p>
        <Field label={money ? 'Chek skrinshoti' : 'Kvitansiya rasmi (ixtiyoriy)'}>
          <input
            type="file"
            accept="image/*,application/pdf"
            className="block w-full text-sm file:mr-3 file:rounded-lg file:border-0 file:bg-brand-50 file:px-3 file:py-2 file:text-brand-700"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
          />
        </Field>
        <Field label="Izoh" hint={money ? '' : 'Masalan: BTS trek raqami'}>
          <textarea className={inputClass} rows={2} value={note} onChange={(e) => setNote(e.target.value)} maxLength={1000} />
        </Field>
        <ErrorBox error={deliver.error} />
        <div className="flex justify-end gap-2">
          <Button variant="secondary" onClick={onClose}>
            Bekor
          </Button>
          <Button disabled={(!file && !note.trim()) || deliver.isPending} onClick={() => deliver.mutate()}>
            {deliver.isPending ? 'Yuborilmoqda…' : "G'olibga yuborish"}
          </Button>
        </div>
      </div>
    </Modal>
  )
}

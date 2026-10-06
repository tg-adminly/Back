import { useState } from 'react'
import { useInfiniteQuery, useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Link, useParams } from 'react-router-dom'
import { ApiError, api, type GiveawayDetail, type Participant } from '../api'
import {
  Button,
  Card,
  ConfirmButton,
  CopyButton,
  DrawModePicker,
  Empty,
  ErrorBox,
  Field,
  GiveawayBadge,
  Loading,
  Modal,
  WinnerBadge,
  endsAtLabel,
  formatDate,
  inputClass,
  toLocalInput,
  useMe,
  userLabel,
} from '../ui'

export default function GiveawayView() {
  const { id } = useParams()
  const me = useMe()
  const qc = useQueryClient()
  const [editing, setEditing] = useState(false)
  const g = useQuery({
    queryKey: ['giveaway', id],
    queryFn: () => api.get<GiveawayDetail>(`/giveaways/${id}`),
    // Qatnashish yopilishini kutib turamiz
    refetchInterval: (q) => (q.state.data?.status === 'active' ? 10_000 : false),
  })
  const action = useMutation({
    mutationFn: (what: 'finish' | 'cancel') => api.post(`/giveaways/${id}/${what}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['giveaway', id] })
      qc.invalidateQueries({ queryKey: ['giveaways'] })
      qc.invalidateQueries({ queryKey: ['stats'] })
    },
  })

  if (g.isPending) return <Loading />
  if (g.error) return <ErrorBox error={g.error} />
  const d = g.data
  const publicUrl = `${window.location.origin}/p/${d.id}`
  const isOwner = me.role === 'owner'

  return (
    <>
      <Link to="/giveaways" className="mb-3 inline-block text-sm text-zinc-500 hover:text-brand-600">
        ← Rozigrishlar
      </Link>
      <div className="mb-5 flex flex-wrap items-start justify-between gap-3">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl font-semibold">{d.title}</h1>
            <GiveawayBadge status={d.status} />
          </div>
          <div className="text-sm text-zinc-500">
            #{d.id} · yaratilgan {formatDate(d.created_at, me.timezone)}
          </div>
        </div>
        <div className="flex flex-wrap gap-2">
          {(d.status === 'drawing' || d.status === 'finished') && d.participants > 0 && (
            <Link to={`/giveaways/${d.id}/live`}>
              <Button variant={d.status === 'drawing' ? 'primary' : 'secondary'}>🎥 Jonli o'yin</Button>
            </Link>
          )}
          {d.post_url && (
            <a href={d.post_url} target="_blank" rel="noopener">
              <Button variant="secondary">Postni ochish ↗</Button>
            </a>
          )}
          {d.status === 'active' && (
            <>
              {isOwner && (
                <Button variant="secondary" onClick={() => setEditing(true)}>
                  ✏️ O'zgartirish
                </Button>
              )}
              <ConfirmButton
                question={
                  d.auto_draw
                    ? "Qatnashishni hozir yopaymi? 1 daqiqa ichida bot g'oliblarni o'zi aniqlab, kanalga e'lon qiladi."
                    : "Qatnashishni hozir yopaymi? 1 daqiqa ichida yopiladi, keyin g'oliblarni jonli o'yinda aniqlaysiz."
                }
                onConfirm={() => action.mutate('finish')}
                pending={action.isPending}
              >
                ⏹ Qatnashishni yopish
              </ConfirmButton>
              {isOwner && (
                <ConfirmButton variant="danger" question="Rozigrishni bekor qilaymi? G'olib aniqlanmaydi." onConfirm={() => action.mutate('cancel')} pending={action.isPending}>
                  Bekor qilish
                </ConfirmButton>
              )}
            </>
          )}
        </div>
      </div>
      <ErrorBox error={action.error} />
      {editing && <EditModal d={d} onClose={() => setEditing(false)} />}

      <div className="mb-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
        <Card>
          <div className="text-2xl font-semibold">{d.participants}</div>
          <div className="text-xs text-zinc-500">ishtirokchi</div>
        </Card>
        <Card>
          <div className="text-2xl font-semibold">{d.winners_count}</div>
          <div className="text-xs text-zinc-500">o'rin</div>
        </Card>
        <Card>
          <div className="text-base font-semibold">{formatDate(d.ends_at, me.timezone)}</div>
          <div className="text-xs text-zinc-500">{d.auto_draw ? (d.status === 'active' ? 'yakunlanadi' : 'yakun vaqti') : "o'yin vaqti"}</div>
        </Card>
        <Card>
          <div className="text-base font-semibold">{d.auto_draw ? '🤖 Avtomatik' : "🎥 Jonli o'yin"}</div>
          <div className="text-xs text-zinc-500">g'olibni aniqlash</div>
        </Card>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <h2 className="mb-3 font-semibold">🏆 {d.winners.length ? "G'oliblar" : 'Sovrinlar'}</h2>
          {d.winners.length ? (
            <div className="divide-y divide-zinc-100 dark:divide-zinc-800">
              {d.winners.map((w) => (
                <div key={w.id} className="flex items-center gap-3 py-2 text-sm">
                  <span className="w-8 text-zinc-500">{w.place}.</span>
                  <div className="min-w-0 flex-1">
                    <div className="truncate">
                      <a href={`tg://user?id=${w.user_id}`} className="hover:text-brand-600">
                        {userLabel(w.name, w.username)}
                      </a>{' '}
                      <span className="text-zinc-400">#{w.number}</span>
                    </div>
                    <div className="text-xs text-zinc-500">{w.prize.label}</div>
                  </div>
                  <WinnerBadge status={w.status} />
                </div>
              ))}
            </div>
          ) : (
            <ol className="space-y-1 text-sm">
              {d.prizes.map((p, i) => (
                <li key={i} className="flex gap-3">
                  <span className="w-8 text-zinc-500">{i + 1}.</span>
                  {p.type === 'money' ? '💵' : '🎁'} {p.label}
                </li>
              ))}
            </ol>
          )}
          {d.status === 'finished' && d.winners.length === 0 && <p className="mt-3 text-sm text-zinc-500">Shartlarni bajargan ishtirokchi bo'lmadi.</p>}
        </Card>

        <div className="space-y-6">
          <Card>
            <h2 className="mb-2 font-semibold">📝 Post matni</h2>
            <p className="text-sm whitespace-pre-wrap text-zinc-700 dark:text-zinc-300">{d.description}</p>
            <h3 className="mt-4 mb-1 text-sm font-medium">Homiylar</h3>
            {d.sponsors.length ? (
              <ul className="space-y-0.5 text-sm">
                {d.sponsors.map((s) => (
                  <li key={s.id}>
                    <a href={s.link} target="_blank" rel="noopener" className="text-brand-600 hover:underline">
                      {s.title}
                    </a>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="text-sm text-zinc-500">Yo'q</div>
            )}
          </Card>
          <Card>
            <h2 className="mb-2 font-semibold">👥 Ochiq ro'yxat</h2>
            <p className="mb-2 text-xs text-zinc-500">
              Hamma ko'ra oladigan sahifa: ishtirokchilar (ism va raqam), yakunlangach — g'oliblar. Domen ulangach, kanal postida tugma bo'lib chiqadi.
            </p>
            <div className="flex items-center gap-2">
              <code className="min-w-0 flex-1 truncate rounded bg-zinc-100 px-2 py-1 text-xs dark:bg-zinc-800">{publicUrl}</code>
              <CopyButton value={publicUrl} />
              <a href={publicUrl} target="_blank" rel="noopener" className="text-xs text-brand-600 hover:underline">
                Ochish ↗
              </a>
            </div>
          </Card>
        </div>
      </div>

      <Participants giveawayId={d.id} total={d.participants} />
    </>
  )
}

/** Faol rozigrish: vaqt va g'olibni aniqlash usuli (kanal posti ham yangilanadi) */
function EditModal({ d, onClose }: { d: GiveawayDetail; onClose: () => void }) {
  const me = useMe()
  const qc = useQueryClient()
  const [autoDraw, setAutoDraw] = useState(d.auto_draw)
  const initialEndsAt = toLocalInput(d.ends_at, me.timezone)
  const [endsAt, setEndsAt] = useState(initialEndsAt)
  const save = useMutation({
    // Vaqt o'zgarmagan bo'lsa yubormaymiz (tekshiruv faqat yangi vaqt uchun)
    mutationFn: () =>
      api.patch<{ warning: string | null }>(`/giveaways/${d.id}`, { auto_draw: autoDraw, ends_at: endsAt === initialEndsAt ? null : endsAt }),
    onSuccess: (r) => {
      qc.invalidateQueries({ queryKey: ['giveaway', String(d.id)] })
      qc.invalidateQueries({ queryKey: ['giveaways'] })
      if (!r.warning) onClose()
    },
  })
  const fieldErrors = save.error instanceof ApiError ? save.error.fields : {}

  return (
    <Modal title="Rozigrishni o'zgartirish" onClose={onClose}>
      {save.data?.warning ? (
        <>
          <p className="mb-5 text-sm">⚠️ {save.data.warning}</p>
          <div className="text-right">
            <Button onClick={onClose}>Yopish</Button>
          </div>
        </>
      ) : (
        <div className="space-y-4">
          <div>
            <div className="mb-1 text-sm font-medium">G'olibni kim aniqlaydi</div>
            <DrawModePicker value={autoDraw} onChange={setAutoDraw} />
          </div>
          <Field label={endsAtLabel(autoDraw)} error={fieldErrors.ends_at}>
            <input type="datetime-local" className={inputClass} value={endsAt} onChange={(e) => setEndsAt(e.target.value)} />
          </Field>
          <p className="text-xs text-zinc-500">Kanaldagi post ham yangilanadi.</p>
          {!fieldErrors.ends_at && <ErrorBox error={save.error} />}
          <div className="flex justify-end gap-2">
            <Button variant="secondary" onClick={onClose}>
              Bekor
            </Button>
            <Button disabled={save.isPending} onClick={() => save.mutate()}>
              {save.isPending ? 'Saqlanmoqda…' : 'Saqlash'}
            </Button>
          </div>
        </div>
      )}
    </Modal>
  )
}

function Participants({ giveawayId, total }: { giveawayId: number; total: number }) {
  const me = useMe()
  const [q, setQ] = useState('')
  const [search, setSearch] = useState('')
  const list = useInfiniteQuery({
    queryKey: ['participants', giveawayId, search],
    initialPageParam: 0,
    queryFn: ({ pageParam }) =>
      api.get<{ items: Participant[]; has_more: boolean }>(
        `/giveaways/${giveawayId}/participants?offset=${pageParam}&q=${encodeURIComponent(search)}`,
      ),
    getNextPageParam: (last, pages) => (last.has_more ? pages.reduce((n, p) => n + p.items.length, 0) : undefined),
  })
  const items = list.data?.pages.flatMap((p) => p.items) ?? []

  return (
    <Card className="mt-6">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
        <h2 className="font-semibold">👥 Ishtirokchilar ({total})</h2>
        <form
          onSubmit={(e) => {
            e.preventDefault()
            setSearch(q)
          }}
          className="flex gap-2"
        >
          <input className={inputClass + ' w-56'} placeholder="Ism yoki @username" value={q} onChange={(e) => setQ(e.target.value)} />
          <Button variant="secondary" type="submit">
            Qidirish
          </Button>
        </form>
      </div>
      {list.isPending ? (
        <Loading />
      ) : items.length ? (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="text-left text-xs text-zinc-500">
              <tr>
                <th className="py-2 pr-3 font-medium">#</th>
                <th className="py-2 pr-3 font-medium">Ism</th>
                <th className="py-2 font-medium">Qo'shilgan</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-100 dark:divide-zinc-800">
              {items.map((p) => (
                <tr key={p.number}>
                  <td className="py-1.5 pr-3 text-zinc-500">{p.number}</td>
                  <td className="py-1.5 pr-3">
                    <a href={`tg://user?id=${p.user_id}`} className="hover:text-brand-600">
                      {userLabel(p.name, p.username)}
                    </a>
                  </td>
                  <td className="py-1.5 whitespace-nowrap text-zinc-500">{formatDate(p.joined_at, me.timezone)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <Empty>{search ? 'Topilmadi.' : "Hali hech kim qatnashmagan."}</Empty>
      )}
      {list.hasNextPage && (
        <div className="mt-3 text-center">
          <Button variant="ghost" onClick={() => list.fetchNextPage()} disabled={list.isFetchingNextPage}>
            Yana ko'rsatish
          </Button>
        </div>
      )}
    </Card>
  )
}

import { useState } from 'react'
import { useInfiniteQuery, useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Link, useParams } from 'react-router-dom'
import { api, type GiveawayDetail, type Participant } from '../api'
import {
  Button,
  Card,
  ConfirmButton,
  CopyButton,
  Empty,
  ErrorBox,
  GiveawayBadge,
  Loading,
  WinnerBadge,
  formatDate,
  inputClass,
  useMe,
  userLabel,
} from '../ui'

export default function GiveawayView() {
  const { id } = useParams()
  const me = useMe()
  const qc = useQueryClient()
  const g = useQuery({
    queryKey: ['giveaway', id],
    queryFn: () => api.get<GiveawayDetail>(`/giveaways/${id}`),
    // Yakunlanayotganda natijani kutib turamiz
    refetchInterval: (q) => (q.state.data?.status === 'active' || q.state.data?.status === 'drawing' ? 10_000 : false),
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
          {d.post_url && (
            <a href={d.post_url} target="_blank" rel="noopener">
              <Button variant="secondary">Postni ochish ↗</Button>
            </a>
          )}
          {d.status === 'active' && (
            <>
              <ConfirmButton question="Rozigrishni hozir yakunlab, g'oliblarni aniqlaymi? Natija 1 daqiqa ichida kanalga chiqadi." onConfirm={() => action.mutate('finish')} pending={action.isPending}>
                ⏹ Hozir yakunlash
              </ConfirmButton>
              <ConfirmButton variant="danger" question="Rozigrishni bekor qilaymi? G'olib aniqlanmaydi." onConfirm={() => action.mutate('cancel')} pending={action.isPending}>
                Bekor qilish
              </ConfirmButton>
            </>
          )}
        </div>
      </div>
      <ErrorBox error={action.error} />

      <div className="mb-6 grid grid-cols-3 gap-3">
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
          <div className="text-xs text-zinc-500">{d.status === 'active' ? 'yakunlanadi' : 'yakun vaqti'}</div>
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
            <h2 className="mb-2 font-semibold">🔐 Adolatli random</h2>
            <Hash label="E'londagi kod (sha256(seed))" value={d.commit_hash} />
            {d.seed ? (
              <>
                <Hash label="Seed" value={d.seed} />
                <Hash label="Ro'yxat hash" value={d.list_hash ?? ''} />
              </>
            ) : (
              <p className="text-xs text-zinc-500">Seed rozigrish yakunlanganda ochiladi — undan oldin hech kim (siz ham) natijani bilmaydi.</p>
            )}
          </Card>
        </div>
      </div>

      <Participants giveawayId={d.id} total={d.participants} />
    </>
  )
}

function Hash({ label, value }: { label: string; value: string }) {
  return (
    <div className="mb-2">
      <div className="flex items-center justify-between text-xs text-zinc-500">
        {label} <CopyButton value={value} />
      </div>
      <code className="block rounded bg-zinc-100 px-2 py-1 text-[11px] break-all dark:bg-zinc-800">{value}</code>
    </div>
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

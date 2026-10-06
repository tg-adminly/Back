import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { api, type Giveaway, type GiveawayStatus } from '../api'
import { Button, Card, Empty, ErrorBox, GiveawayBadge, Loading, PageHeader, cx, formatDate, useMe } from '../ui'

const TABS: { value: GiveawayStatus | ''; label: string }[] = [
  { value: '', label: 'Hammasi' },
  { value: 'active', label: 'Faol' },
  { value: 'finished', label: 'Yakunlangan' },
  { value: 'cancelled', label: 'Bekor qilingan' },
]

export default function Giveaways() {
  const me = useMe()
  const [status, setStatus] = useState<GiveawayStatus | ''>('')
  const list = useQuery({
    queryKey: ['giveaways', status],
    queryFn: () => api.get<Giveaway[]>(`/giveaways${status ? `?status=${status}` : ''}`),
  })

  return (
    <>
      <PageHeader
        title="Rozigrishlar"
        action={
          me.role === 'owner' && (
            <Link to="/giveaways/new">
              <Button>+ Yangi rozigrish</Button>
            </Link>
          )
        }
      />
      <div className="mb-4 flex gap-1 overflow-x-auto">
        {TABS.map((t) => (
          <button
            key={t.value}
            onClick={() => setStatus(t.value)}
            className={cx(
              'rounded-full px-3 py-1 text-sm whitespace-nowrap',
              status === t.value ? 'bg-zinc-900 text-white dark:bg-white dark:text-zinc-900' : 'text-zinc-600 hover:bg-zinc-100 dark:text-zinc-300 dark:hover:bg-zinc-800',
            )}
          >
            {t.label}
          </button>
        ))}
      </div>
      <ErrorBox error={list.error} />
      {list.isPending ? (
        <Loading />
      ) : list.data?.length ? (
        <Card className="divide-y divide-zinc-100 p-0 dark:divide-zinc-800">
          {list.data.map((g) => (
            <Link key={g.id} to={`/giveaways/${g.id}`} className="flex items-center gap-3 px-4 py-3 hover:bg-zinc-50 dark:hover:bg-zinc-800/50">
              <div className="min-w-0 flex-1">
                <div className="truncate font-medium">
                  <span className="text-zinc-400">#{g.id}</span> {g.title}
                </div>
                <div className="text-xs text-zinc-500">
                  {g.winners_count} o'rin · 👥 {g.participants} · {g.auto_draw ? '🤖' : '🎥'} {formatDate(g.ends_at, me.timezone)}
                </div>
              </div>
              <GiveawayBadge status={g.status} />
            </Link>
          ))}
        </Card>
      ) : (
        <Empty>Rozigrish yo'q.</Empty>
      )}
    </>
  )
}

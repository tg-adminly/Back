import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { api, type Giveaway, type Stats } from '../api'
import { Button, Card, Empty, ErrorBox, Loading, PageHeader, formatDate, useMe } from '../ui'

export default function Dashboard() {
  const me = useMe()
  const stats = useQuery({ queryKey: ['stats'], queryFn: () => api.get<Stats>('/stats'), refetchInterval: 15_000 })
  const active = useQuery({
    queryKey: ['giveaways', 'active'],
    queryFn: () => api.get<Giveaway[]>('/giveaways?status=active'),
    refetchInterval: 15_000,
  })

  return (
    <>
      <PageHeader
        title={`Salom, ${me.name.split(' ')[0]}!`}
        action={
          <Link to="/giveaways/new">
            <Button>+ Yangi rozigrish</Button>
          </Link>
        }
      />
      <ErrorBox error={stats.error} />
      {stats.data && (
        <div className="mb-8 grid grid-cols-2 gap-3 lg:grid-cols-4">
          <Stat label="Faol rozigrishlar" value={stats.data.active_giveaways} to="/giveaways" />
          <Stat label="Ularda ishtirokchilar" value={stats.data.active_participants} />
          <Stat label="To'lash kerak" value={stats.data.ready_to_pay} to="/payouts" highlight={stats.data.ready_to_pay > 0} />
          <Stat label="G'olibdan ma'lumot kutilmoqda" value={stats.data.awaiting_info} to="/payouts" />
        </div>
      )}

      <h2 className="mb-3 text-base font-semibold">Faol rozigrishlar</h2>
      {active.isPending ? (
        <Loading />
      ) : active.data?.length ? (
        <div className="grid gap-3 sm:grid-cols-2">
          {active.data.map((g) => (
            <Link key={g.id} to={`/giveaways/${g.id}`}>
              <Card className="transition hover:ring-brand-500">
                <div className="mb-1 text-xs text-zinc-500">#{g.id}</div>
                <div className="mb-3 font-medium">{g.title}</div>
                <div className="flex justify-between text-sm text-zinc-600 dark:text-zinc-400">
                  <span>👥 {g.participants} ishtirokchi</span>
                  <span>⏰ {formatDate(g.ends_at, me.timezone)}</span>
                </div>
              </Card>
            </Link>
          ))}
        </div>
      ) : (
        <Empty>Hozir faol rozigrish yo'q.</Empty>
      )}
    </>
  )
}

function Stat({ label, value, to, highlight }: { label: string; value: number; to?: string; highlight?: boolean }) {
  const body = (
    <Card className={highlight ? 'ring-2 ring-brand-500! dark:ring-brand-500!' : ''}>
      <div className="text-2xl font-semibold">{value}</div>
      <div className="text-xs text-zinc-500">{label}</div>
    </Card>
  )
  return to ? <Link to={to}>{body}</Link> : body
}

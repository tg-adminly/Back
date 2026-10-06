// Kichik umumiy komponentlar va formatlash

import type { ButtonHTMLAttributes, ReactNode } from 'react'
import { createContext, useContext, useState } from 'react'
import type { GiveawayStatus, Me, WinnerStatus } from './api'

export const MeContext = createContext<Me | null>(null)
export const useMe = () => useContext(MeContext)!

export function formatDate(iso: string, tz: string) {
  // Botdagidek: 15.10.2026 20:00
  const parts = Object.fromEntries(
    new Intl.DateTimeFormat('en-GB', {
      timeZone: tz,
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hourCycle: 'h23',
    })
      .formatToParts(new Date(iso))
      .map((p) => [p.type, p.value]),
  )
  return `${parts.day}.${parts.month}.${parts.year} ${parts.hour}:${parts.minute}`
}

/** ISO vaqt → datetime-local maydoni uchun mahalliy qiymat ("2026-10-15T20:00") */
export function toLocalInput(iso: string, tz: string) {
  const [date, time] = formatDate(iso, tz).split(' ')
  const [day, month, year] = date.split('.')
  return `${year}-${month}-${day}T${time}`
}

export function cx(...parts: (string | false | null | undefined)[]) {
  return parts.filter(Boolean).join(' ')
}

type Variant = 'primary' | 'secondary' | 'danger' | 'ghost'
const VARIANTS: Record<Variant, string> = {
  primary: 'bg-brand-500 text-white hover:bg-brand-600 disabled:bg-brand-500/50',
  secondary:
    'bg-white text-zinc-800 ring-1 ring-zinc-200 hover:bg-zinc-50 dark:bg-zinc-900 dark:text-zinc-100 dark:ring-zinc-700 dark:hover:bg-zinc-800',
  danger: 'bg-red-600 text-white hover:bg-red-700 disabled:bg-red-600/50',
  ghost: 'text-zinc-600 hover:bg-zinc-100 dark:text-zinc-300 dark:hover:bg-zinc-800',
}

export function Button({
  variant = 'primary',
  className,
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: Variant }) {
  return (
    <button
      {...props}
      className={cx(
        'inline-flex items-center justify-center gap-2 rounded-lg px-4 py-2 text-sm font-medium whitespace-nowrap transition disabled:cursor-not-allowed',
        VARIANTS[variant],
        className,
      )}
    />
  )
}

export function Card({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <div className={cx('rounded-xl bg-white p-4 ring-1 ring-zinc-200 dark:bg-zinc-900 dark:ring-zinc-800', className)}>
      {children}
    </div>
  )
}

export function PageHeader({ title, action }: { title: string; action?: ReactNode }) {
  return (
    <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
      <h1 className="text-xl font-semibold">{title}</h1>
      {action}
    </div>
  )
}

export const inputClass =
  'w-full rounded-lg border-0 bg-white px-3 py-2 text-sm ring-1 ring-zinc-300 placeholder:text-zinc-400 focus:ring-2 focus:ring-brand-500 focus:outline-none dark:bg-zinc-900 dark:ring-zinc-700'

export function Field({ label, error, hint, children }: { label: string; error?: string; hint?: string; children: ReactNode }) {
  return (
    <label className="block">
      <span className="mb-1 block text-sm font-medium">{label}</span>
      {children}
      {error ? (
        <span className="mt-1 block text-xs text-red-600">{error}</span>
      ) : hint ? (
        <span className="mt-1 block text-xs text-zinc-500">{hint}</span>
      ) : null}
    </label>
  )
}

export function ErrorBox({ error }: { error: unknown }) {
  if (!error) return null
  return (
    <div className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700 dark:bg-red-950 dark:text-red-300">
      {error instanceof Error ? error.message : String(error)}
    </div>
  )
}

export function Loading() {
  return <div className="py-10 text-center text-sm text-zinc-500">Yuklanmoqda…</div>
}

export function Empty({ children }: { children: ReactNode }) {
  return <div className="py-10 text-center text-sm text-zinc-500">{children}</div>
}

const GIVEAWAY_STATUS: Record<GiveawayStatus, [string, string]> = {
  active: ['Faol', 'bg-green-100 text-green-800 dark:bg-green-950 dark:text-green-300'],
  drawing: ["Jonli o'yin kutilmoqda", 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300'],
  finished: ['Yakunlangan', 'bg-zinc-100 text-zinc-700 dark:bg-zinc-800 dark:text-zinc-300'],
  cancelled: ['Bekor qilingan', 'bg-red-100 text-red-700 dark:bg-red-950 dark:text-red-300'],
}

const WINNER_STATUS: Record<WinnerStatus, [string, string]> = {
  awaiting_info: ["Ma'lumot kutilmoqda", 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300'],
  info_received: ["To'lash kerak", 'bg-brand-100 text-brand-700 dark:bg-brand-700/30 dark:text-brand-100'],
  done: ['Topshirildi', 'bg-green-100 text-green-800 dark:bg-green-950 dark:text-green-300'],
}

function Badge({ label, className }: { label: string; className: string }) {
  return <span className={cx('inline-block rounded-full px-2 py-0.5 text-xs font-medium whitespace-nowrap', className)}>{label}</span>
}

export const GiveawayBadge = ({ status }: { status: GiveawayStatus }) => (
  <Badge label={GIVEAWAY_STATUS[status][0]} className={GIVEAWAY_STATUS[status][1]} />
)
export const WinnerBadge = ({ status }: { status: WinnerStatus }) => (
  <Badge label={WINNER_STATUS[status][0]} className={WINNER_STATUS[status][1]} />
)

export function Modal({ title, onClose, children }: { title: string; onClose: () => void; children: ReactNode }) {
  return (
    <div className="fixed inset-0 z-50 flex items-end justify-center bg-black/40 p-0 sm:items-center sm:p-4" onClick={onClose}>
      <div
        className="max-h-[90vh] w-full max-w-lg overflow-y-auto rounded-t-2xl bg-white p-5 sm:rounded-2xl dark:bg-zinc-900"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold">{title}</h2>
          <button onClick={onClose} className="text-2xl leading-none text-zinc-400 hover:text-zinc-600" aria-label="Yopish">
            ×
          </button>
        </div>
        {children}
      </div>
    </div>
  )
}

/** «Rostdan ham?» tasdig'i bilan tugma */
export function ConfirmButton({
  question,
  onConfirm,
  children,
  variant = 'secondary',
  pending,
}: {
  question: string
  onConfirm: () => void
  children: ReactNode
  variant?: Variant
  pending?: boolean
}) {
  const [open, setOpen] = useState(false)
  return (
    <>
      <Button variant={variant} onClick={() => setOpen(true)} disabled={pending}>
        {children}
      </Button>
      {open && (
        <Modal title="Tasdiqlang" onClose={() => setOpen(false)}>
          <p className="mb-5 text-sm">{question}</p>
          <div className="flex justify-end gap-2">
            <Button variant="secondary" onClick={() => setOpen(false)}>
              Yo'q
            </Button>
            <Button
              variant={variant === 'danger' ? 'danger' : 'primary'}
              onClick={() => {
                setOpen(false)
                onConfirm()
              }}
            >
              Ha, tasdiqlayman
            </Button>
          </div>
        </Modal>
      )}
    </>
  )
}

export function CopyButton({ value }: { value: string }) {
  const [done, setDone] = useState(false)
  return (
    <button
      type="button"
      className="rounded-md px-2 py-0.5 text-xs text-brand-600 hover:bg-brand-50 dark:hover:bg-zinc-800"
      onClick={() => {
        navigator.clipboard.writeText(value).then(() => {
          setDone(true)
          setTimeout(() => setDone(false), 1500)
        })
      }}
    >
      {done ? '✓ Nusxalandi' : 'Nusxalash'}
    </button>
  )
}

export function userLabel(name: string, username: string | null) {
  return username ? `${name} (@${username})` : name
}

const DRAW_MODES = [
  {
    auto: false,
    title: "🎥 Jonli o'yin",
    text: "Vaqt — eslatma. O'yinni siz yoki muharrir istalgan paytda (oldinroq yoki keyinroq) efirda boshlaysiz, shungacha qatnashish ochiq.",
  },
  {
    auto: true,
    title: '🤖 Avtomatik',
    text: "Vaqti kelganda bot g'oliblarni o'zi aniqlab, kanalga e'lon qiladi.",
  },
]

/** G'olibni aniqlash usuli: jonli o'yin yoki bot avtomatik */
export function DrawModePicker({ value, onChange }: { value: boolean; onChange: (auto: boolean) => void }) {
  return (
    <div className="grid gap-2 sm:grid-cols-2" role="radiogroup">
      {DRAW_MODES.map((m) => (
        <button
          key={m.title}
          type="button"
          role="radio"
          aria-checked={value === m.auto}
          onClick={() => onChange(m.auto)}
          className={cx(
            'rounded-xl p-3 text-left ring-1 transition',
            value === m.auto
              ? 'bg-brand-50 ring-2 ring-brand-500 dark:bg-brand-700/20'
              : 'ring-zinc-200 hover:bg-zinc-50 dark:ring-zinc-700 dark:hover:bg-zinc-800',
          )}
        >
          <div className="text-sm font-medium">{m.title}</div>
          <div className="mt-0.5 text-xs text-zinc-500">{m.text}</div>
        </button>
      ))}
    </div>
  )
}

export const endsAtLabel = (auto: boolean) => (auto ? 'Yakunlanish vaqti (Toshkent vaqti)' : "O'yin vaqti (Toshkent vaqti)")

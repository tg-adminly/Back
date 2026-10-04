// Backend (src/tgagent/panel/api.py) bilan aloqa

export class ApiError extends Error {
  status: number
  fields: Record<string, string>
  constructor(status: number, message: string, fields: Record<string, string> = {}) {
    super(message)
    this.status = status
    this.fields = fields
  }
}

async function request<T>(method: string, path: string, body?: unknown): Promise<T> {
  const init: RequestInit = { method, credentials: 'same-origin', headers: { 'x-panel': '1' } }
  if (body instanceof FormData) {
    init.body = body
  } else if (body !== undefined) {
    init.body = JSON.stringify(body)
    ;(init.headers as Record<string, string>)['content-type'] = 'application/json'
  }
  const res = await fetch('/api' + path, init)
  const data = await res.json().catch(() => null)
  if (!res.ok) {
    const detail = data?.detail
    if (detail && typeof detail === 'object' && 'errors' in detail) {
      throw new ApiError(res.status, "Formada xato bor — qizil maydonlarni tekshiring.", detail.errors)
    }
    throw new ApiError(res.status, typeof detail === 'string' ? detail : `Xato (${res.status})`)
  }
  return data as T
}

export const api = {
  get: <T>(path: string) => request<T>('GET', path),
  post: <T>(path: string, body?: unknown) => request<T>('POST', path, body),
  del: <T>(path: string) => request<T>('DELETE', path),
}

// --- Turlar ---

export type Role = 'owner' | 'editor'
export interface Me {
  user_id: number
  name: string
  role: Role
  channel: { title: string; link: string }
  timezone: string
}

export type PrizeType = 'money' | 'item'
export interface Prize {
  type: PrizeType
  amount: number | null
  name: string | null
  label: string
}

export interface Sponsor {
  id: number
  title: string
  link: string
  chat_id: number
}

export type GiveawayStatus = 'active' | 'drawing' | 'finished' | 'cancelled'
export interface Giveaway {
  id: number
  title: string
  description: string
  status: GiveawayStatus
  prizes: Prize[]
  winners_count: number
  participants: number
  ends_at: string
  created_at: string
  sponsors: Sponsor[]
  post_url: string | null
  commit_hash: string
  seed: string | null
  list_hash: string | null
}

export type WinnerStatus = 'awaiting_info' | 'info_received' | 'done'
export interface Winner {
  id: number
  giveaway_id: number
  giveaway_title: string
  place: number
  prize: Prize
  user_id: number
  name: string
  username: string | null
  number: number
  status: WinnerStatus
  claim_step: string | null
  card_masked: string | null
  done_at: string | null
}

export interface GiveawayDetail extends Giveaway {
  winners: Winner[]
}

export interface Participant {
  number: number
  user_id: number
  name: string
  username: string | null
  joined_at: string
}

export interface Stats {
  active_giveaways: number
  active_participants: number
  awaiting_info: number
  ready_to_pay: number
}

export interface PayoutDetails {
  card?: string
  card_holder?: string
  full_name?: string
  phone?: string
  address?: string
}

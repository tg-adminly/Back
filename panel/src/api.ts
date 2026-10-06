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
  patch: <T>(path: string, body?: unknown) => request<T>('PATCH', path, body),
  put: <T>(path: string, body?: unknown) => request<T>('PUT', path, body),
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

export interface BotChat {
  chat_id: number
  title: string
  username: string | null
}

export type GiveawayStatus = 'active' | 'drawing' | 'finished' | 'cancelled'
export interface Giveaway {
  id: number
  title: string
  description: string
  status: GiveawayStatus
  auto_draw: boolean // true — vaqtida bot o'zi aniqlaydi; false — jonli o'yin (vaqt — eslatma)
  prizes: Prize[]
  winners_count: number
  participants: number
  ends_at: string
  created_at: string
  sponsors: Sponsor[]
  post_url: string | null
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
  not_subscribed: number // oxirgi tekshiruv bo'yicha biror kanalga obuna bo'lmaganlar
  check: { total: number; done: number } | null // obuna tekshiruvi ketyapti
  check_error: string | null
  last_checked: string | null // oxirgi tekshiruv (server qayta ishga tushgach — null)
}

export interface Participant {
  number: number
  user_id: number
  name: string
  username: string | null
  joined_at: string
  missing: string[] // obuna bo'lmagan kanallar
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

// --- Jonli o'yin ---

export interface LivePick {
  number: number
  name: string
  place: number | null // null — kanaldan chiqib ketgani uchun o'tkazib yuborilgan
  missing: string[] // obuna bo'lmagan kanallar
}

export interface LiveState extends Giveaway {
  names: { number: number; name: string }[]
  picks: LivePick[]
  excluded: { number: number; name: string; missing: string[] }[] // o'yindan oldingi tekshiruvda chiqib ketganlar
  check: { total: number; done: number } | null // obuna tekshiruvi ketyapti
  check_error: string | null
  exhausted: boolean
}

// --- Ochiq sahifa (login shart emas) ---

export interface PublicGiveaway {
  id: number
  title: string
  status: GiveawayStatus
  auto_draw: boolean
  prizes: Prize[]
  ends_at: string
  timezone: string
  channel: { title: string; link: string }
  post_url: string | null
  participants: { number: number; name: string; missing: string[] }[]
  winners: { place: number; number: number; name: string; prize: Prize }[]
}

// --- Kontent agenti ---

export interface AiUsage {
  enabled: boolean
  model: string
  limit: number
  month_cost: number
}

export interface Sample {
  id: number
  source: 'own' | 'other'
  source_name: string | null
  text: string
  image: string | null // /api/content/media/...
  image_note: string | null
  image_desc: string | null // agent rasmda nimani ko'rdi
  analysis: string | null // null — hali tahlil qilinmagan
  added_by: string
  created_at: string
}

export type ProposalStatus = 'pending' | 'accepted' | 'rejected' | 'superseded'
export interface TrainMessage {
  id: number
  role: 'user' | 'assistant'
  author: string
  text: string
  sample: Sample | null
  sample_deleted: boolean
  proposal: string | null // qo'llanmaning taklif qilingan to'liq matni
  proposal_note: string | null
  proposal_status: ProposalStatus | null
  created_at: string
}

export interface GuideVersion {
  id: number
  text: string
  note: string | null
  author: string
  created_at: string
}

import { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api, type Sponsor } from '../api'
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

export function SponsorAddForm({ onAdded }: { onAdded?: (s: Sponsor) => void }) {
  const qc = useQueryClient()
  const [ref, setRef] = useState('')
  const [link, setLink] = useState('')
  const add = useMutation({
    mutationFn: () => api.post<Sponsor>('/sponsors', { ref, link: link || null }),
    onSuccess: (s) => {
      qc.invalidateQueries({ queryKey: ['sponsors'] })
      setRef('')
      setLink('')
      onAdded?.(s)
    },
  })

  return (
    <form
      className="space-y-3"
      onSubmit={(e) => {
        e.preventDefault()
        add.mutate()
      }}
    >
      <ol className="list-decimal space-y-1 pl-5 text-xs text-zinc-500">
        <li>Botni homiy kanalga <b>admin</b> qilib qo'shing (obunani tekshirish uchun).</li>
        <li>Kanal @username'ini yoki ID'sini (-100…) yozing.</li>
      </ol>
      <Field label="Kanal">
        <input className={inputClass} value={ref} onChange={(e) => setRef(e.target.value)} placeholder="@homiy_kanal yoki https://t.me/homiy_kanal" required />
      </Field>
      <Field label="Taklif havolasi (faqat yopiq kanal uchun)" hint="Ochiq kanalda bo'sh qoldiring">
        <input className={inputClass} value={link} onChange={(e) => setLink(e.target.value)} placeholder="https://t.me/+AbCdEf..." />
      </Field>
      <ErrorBox error={add.error} />
      <Button type="submit" className="w-full" disabled={!ref.trim() || add.isPending}>
        {add.isPending ? 'Tekshirilmoqda…' : "Tekshirib qo'shish"}
      </Button>
    </form>
  )
}

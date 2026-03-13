import type { FC } from 'react'

type Recommendation = {
  id: string
  name: string
  category: string
  reason: string
  isMain: boolean
}

type RecommendationCardProps = {
  recommendation: Recommendation
  onSelect?: (recommendation: Recommendation) => void
}

export const RecommendationCard: FC<RecommendationCardProps> = ({
  recommendation,
  onSelect,
}) => {
  const { name, category, reason, isMain } = recommendation

  return (
    <article className="flex flex-col gap-3 rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <header className="flex items-start justify-between gap-2">
        <div>
          <h2 className="text-base font-semibold text-slate-900">{name}</h2>
          <p className="text-sm text-slate-600">{category}</p>
        </div>
        <span
          className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-medium ${
            isMain
              ? 'bg-emerald-50 text-emerald-800'
              : 'bg-slate-50 text-slate-700'
          }`}
        >
          {isMain ? 'Recomendación principal' : 'Alternativa'}
        </span>
      </header>

      <p className="text-sm text-slate-700">{reason}</p>

      {onSelect ? (
        <div className="mt-2 flex justify-end">
          <button
            type="button"
            className="rounded-md bg-sky-600 px-3 py-1.5 text-sm font-medium text-white shadow-sm transition hover:bg-sky-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 focus-visible:ring-offset-2"
            onClick={() => onSelect(recommendation)}
          >
            Ver detalle
          </button>
        </div>
      ) : null}
    </article>
  )
}


import type { FC } from 'react'
import type { ProductRecommendation } from '../../../shared/types'

type RecommendationCardProps = {
  product: ProductRecommendation
  onSelect?: (product: ProductRecommendation) => void
}

export const RecommendationCard: FC<RecommendationCardProps> = ({
  product,
  onSelect,
}) => {
  const { name, category, reason, badge, price, stock, format } = product
  const isMain = badge === 'main'
  const stockIsEnStock = stock?.toLowerCase().includes('en stock')

  return (
    <article
      className="rounded-xl border-2 border-gray-200 bg-white p-6 transition-colors hover:border-emerald-300"
    >
      <header className="flex items-start justify-between gap-2">
        <h2 className="text-lg font-semibold text-gray-900">{name}</h2>
        <span
          className={`inline-flex shrink-0 rounded-full px-3 py-1 text-xs font-medium ${
            isMain
              ? 'bg-emerald-100 text-emerald-800'
              : 'bg-sky-100 text-sky-800'
          }`}
        >
          {isMain ? 'Recomendación principal' : 'Alternativa'}
        </span>
      </header>

      <p className="mt-1 text-sm font-medium text-emerald-700">{category}</p>
      <p className="mt-2 text-sm text-gray-700">{reason}</p>

      {(price != null || stock != null || format != null) && (
        <div className="mt-4 flex flex-wrap gap-x-4 gap-y-1 border-t border-gray-100 pt-4 text-sm text-gray-600">
          {price != null && <span>{price}</span>}
          {stock != null && (
            <span
              className={
                stockIsEnStock ? 'text-emerald-600' : 'text-amber-600'
              }
            >
              {stock}
            </span>
          )}
          {format != null && <span>{format}</span>}
        </div>
      )}

      {onSelect != null && (
        <div className="mt-4 flex justify-end">
          <button
            type="button"
            onClick={() => onSelect(product)}
            className="rounded-lg bg-sky-600 px-3 py-2 text-sm font-medium text-white transition hover:bg-sky-700 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:ring-offset-2"
          >
            Ver detalle
          </button>
        </div>
      )}
    </article>
  )
}

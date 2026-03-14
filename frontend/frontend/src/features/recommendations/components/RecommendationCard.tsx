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
      className="border-2 border-gray-200 rounded-xl p-6 hover:border-emerald-300 transition-colors"
    >
      <header className="flex items-start justify-between gap-2 mb-3">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-1">
            <h2 className="text-gray-800">{name}</h2>
            <span
              className={`px-3 py-1 rounded-full text-xs ${
                isMain
                  ? 'bg-emerald-500 text-white'
                  : 'bg-blue-100 text-blue-700'
              }`}
            >
              {isMain ? 'Recomendación principal' : 'Alternativa'}
            </span>
          </div>
          <p className="text-sm text-emerald-600 mb-2">{category}</p>
        </div>
      </header>

      <p className="text-gray-700 mb-4">{reason}</p>

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

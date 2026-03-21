import type { FC } from 'react'
import type { ProductRecommendation } from '../../../shared/types'

type RecommendationCardProps = {
  product: ProductRecommendation
  onSelect?: (product: ProductRecommendation) => void
}

function stockStatusClass(status: string | undefined): string {
  if (status == null || status === '') {
    return 'text-gray-700'
  }
  const s = status.toLowerCase()
  if (s.includes('sin stock')) {
    return 'text-red-600'
  }
  if (s.includes('pocas')) {
    return 'text-amber-600'
  }
  if (s.includes('en stock')) {
    return 'text-emerald-600'
  }
  return 'text-gray-700'
}

export const RecommendationCard: FC<RecommendationCardProps> = ({
  product,
  onSelect,
}) => {
  const {
    name,
    category,
    reason,
    badge,
    price,
    stock,
    format,
    recommendedFor,
    commercialMargin,
    stockUnits,
  } = product
  const isMain = badge === 'main'

  const showMetaFooter =
    price != null ||
    stock != null ||
    format != null ||
    commercialMargin != null ||
    stockUnits != null

  return (
    <article
      className="border-2 border-gray-200 rounded-xl p-6 hover:border-emerald-300 transition-colors"
    >
      <header className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between mb-3">
        <div className="flex-1 min-w-0">
          <div className="flex flex-wrap items-center gap-3 mb-1">
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
          <p className="text-sm text-emerald-600 mb-0">{category}</p>
        </div>
        {recommendedFor != null && recommendedFor.trim() !== '' && (
          <div className="text-right sm:max-w-[min(100%,20rem)] sm:shrink-0">
            <p className="text-xs font-medium text-gray-500 mb-0.5">
              Recomendado para
            </p>
            <p className="text-sm font-medium text-emerald-700 leading-snug">
              {recommendedFor}
            </p>
          </div>
        )}
      </header>

      <p className="text-gray-700 mb-4">{reason}</p>

      {showMetaFooter && (
        <dl className="mt-4 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-x-4 gap-y-3 border-t border-gray-100 pt-4 text-sm">
          {price != null && (
            <div>
              <dt className="text-gray-500">Precio</dt>
              <dd className="font-medium text-gray-900 mt-0.5">{price}</dd>
            </div>
          )}
          {commercialMargin != null && (
            <div>
              <dt className="text-gray-500">Margen</dt>
              <dd className="font-medium text-gray-900 mt-0.5">
                {commercialMargin}
              </dd>
            </div>
          )}
          {stock != null && (
            <div>
              <dt className="text-gray-500">Stock</dt>
              <dd
                className={`font-medium mt-0.5 ${stockStatusClass(stock)}`}
              >
                {stock}
              </dd>
            </div>
          )}
          {stockUnits != null && (
            <div>
              <dt className="text-gray-500">Unidades</dt>
              <dd className="font-medium text-gray-900 mt-0.5">
                {stockUnits}
              </dd>
            </div>
          )}
          {format != null && (
            <div className="col-span-2 sm:col-span-1">
              <dt className="text-gray-500">Formato</dt>
              <dd className="font-medium text-gray-900 mt-0.5">{format}</dd>
            </div>
          )}
        </dl>
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

import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { RecommendationCard } from './RecommendationCard'
import type { ProductRecommendation } from '../../../shared/types'

describe('RecommendationCard', () => {
  const baseProduct: ProductRecommendation = {
    id: 'rec-1',
    name: 'Paracetamol 1g',
    category: 'Analgésico',
    reason: 'Indicado para dolor leve y fiebre.',
    badge: 'main',
  }

  it('renders product name', () => {
    render(<RecommendationCard product={baseProduct} />)
    expect(screen.getByText('Paracetamol 1g')).toBeInTheDocument()
  })

  it('renders category', () => {
    render(<RecommendationCard product={baseProduct} />)
    expect(screen.getByText('Analgésico')).toBeInTheDocument()
  })

  it('renders reason', () => {
    render(<RecommendationCard product={baseProduct} />)
    expect(
      screen.getByText('Indicado para dolor leve y fiebre.')
    ).toBeInTheDocument()
  })

  it('shows badge "Recomendación principal" when badge is main', () => {
    render(<RecommendationCard product={baseProduct} />)
    expect(
      screen.getByText('Recomendación principal')
    ).toBeInTheDocument()
  })

  it('shows badge "Alternativa" when badge is alternative', () => {
    const alt: ProductRecommendation = { ...baseProduct, badge: 'alternative' }
    render(<RecommendationCard product={alt} />)
    expect(screen.getByText('Alternativa')).toBeInTheDocument()
  })

  it('renders price, stock and format when provided', () => {
    const withMeta: ProductRecommendation = {
      ...baseProduct,
      price: '5.99€',
      stock: 'En stock',
      format: '20 comprimidos',
    }
    render(<RecommendationCard product={withMeta} />)
    expect(screen.getByText('5.99€')).toBeInTheDocument()
    expect(screen.getByText('En stock')).toBeInTheDocument()
    expect(screen.getByText('20 comprimidos')).toBeInTheDocument()
  })

  it('does not render price/stock/format when omitted', () => {
    render(<RecommendationCard product={baseProduct} />)
    expect(screen.queryByText(/€/)).not.toBeInTheDocument()
    expect(screen.queryByText('En stock')).not.toBeInTheDocument()
  })

  it('applies distinct stock style for "En stock" vs "Pocas unidades"', () => {
    const enStock: ProductRecommendation = {
      ...baseProduct,
      stock: 'En stock',
    }
    const { unmount } = render(<RecommendationCard product={enStock} />)
    const enStockEl = screen.getByText('En stock')
    expect(enStockEl).toHaveClass('text-emerald-600')

    unmount()
    const pocas: ProductRecommendation = {
      ...baseProduct,
      stock: 'Pocas unidades',
    }
    render(<RecommendationCard product={pocas} />)
    const pocasEl = screen.getByText('Pocas unidades')
    expect(pocasEl).toHaveClass('text-amber-600')
  })

  it('calls onSelect with product when "Ver detalle" is clicked', async () => {
    const onSelect = vi.fn()
    render(<RecommendationCard product={baseProduct} onSelect={onSelect} />)
    const button = screen.getByRole('button', { name: /ver detalle/i })
    await userEvent.setup().click(button)
    expect(onSelect).toHaveBeenCalledWith(baseProduct)
  })
})
